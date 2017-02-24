#!/usr/bin/env python
import os
import ctypes
from ctypes.util import find_library


if os.getenv('COGITO_PATH') is None:
    _path = find_library('cogito')
else:
    _path = os.environ['COGITO_PATH']

if _path is None:
    message = "libcogito is missing from your system. " \
        "Please install by running the following steps:\n"
    if os.popen('uname').read().strip() == 'Darwin':
        message += """
    $ brew tap localytics/formulae git@github.com:localytics/homebrew-formulae
    $ brew install cogito
"""
    else:
        message += """
    $ FILE=$(mktemp)
    $ wget 'https://s3.amazonaws.com/public.localytics/artifacts/libcogito_0.0.1-1_amd64.deb' -qO $FILE
    $ sudo dpkg -i $FILE && rm $FILE
"""  # noqa
    raise NameError(message)
_mod = ctypes.cdll.LoadLibrary(_path)


class CgBuf(ctypes.Structure):
    """
    typedef struct cg_buf {
      size_t length;
      size_t capacity;
      char *content;
    } cg_buf_t;
    """
    _fields_ = [('length', ctypes.c_size_t),
                ('capacity', ctypes.c_size_t),
                ('content', ctypes.c_char_p), ]

# int cg_to_json
cg_to_json = _mod.cg_to_json
cg_to_json.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
cg_to_json.restype = ctypes.c_int

# int cg_to_iam
cg_to_iam = _mod.cg_to_iam
cg_to_iam.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
cg_to_iam.restype = ctypes.c_int

# cg_buf_t* cg_buf_build(void);
cg_buf_build = _mod.cg_buf_build
cg_buf_build.argtypes = None
cg_buf_build.restype = ctypes.POINTER(CgBuf)

# void cg_buf_free(cg_buf_t *buffer);
cg_buf_free = _mod.cg_buf_free
cg_buf_free.argtypes = (ctypes.POINTER(CgBuf), )
cg_buf_free.restype = None


def to_iam(args):
    buf = cg_buf_build()
    if cg_to_iam(buf, args) != 0:
        raise CogitoError("IAM conversion failed")
    response = buf.contents.content
    cg_buf_free(buf)
    return response


def to_json(args, subs=None):
    for key, value in (subs or {}).items():
        args = args.replace("${{{}}}".format(key), value)

    buf = cg_buf_build()
    if cg_to_json(buf, args) != 0:
        raise CogitoError("JSON conversion failed")
    response = buf.contents.content
    cg_buf_free(buf)
    return response


class CogitoError(Exception):
    pass
