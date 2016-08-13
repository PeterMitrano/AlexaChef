all: zip upload

zip:
	mkdir -p build
	rm -f ./build/skill.zip
	cp -r ./venv/lib/python2.7/site-packages/requests build
	cp -r ./lambda_function.py ./my_cookbook build
	find build -name "*.swp" | xargs rm -f
	cd build &&	zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip
