all: zip upload test

zip:
	mkdir -p build
	cp -r src/* build
	cd build &&	zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbookPy --zip-file fileb://build/skill.zip
