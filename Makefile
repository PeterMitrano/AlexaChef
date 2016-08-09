all: zip upload

zip:
	mkdir -p build
	cp -r src/* build
	find build -name *.swp | xargs rm
	cd build &&	zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip
