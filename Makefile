all: zip upload test

zip:
	mkdir -p build
	cp -r src/* build
	cp -r node_modules build
	cp package.json build
	cd build &&	zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip
