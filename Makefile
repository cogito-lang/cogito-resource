# upload: clean output.zip
# 	aws lambda update-function-code --function-name cogito --zip-file fileb://output.zip

output.zip: clean libcogito.so
	zip output.zip cogito.py handler.py libcogito.so

clean:
	rm -f output.zip
	rm -f *.pyc

libcogito.so:
	curl https://s3.amazonaws.com/public.localytics/artifacts/cogito/amazon/libcogito.so -o libcogito.so
