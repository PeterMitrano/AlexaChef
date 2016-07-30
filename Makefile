all: zip upload test

zip:
	mkdir -p build
	cp -r src/node_modules build
	cp src/*.js build
	cp src/package.json build
	cd build && zip -q -r skill.zip node_modules *.js package.json

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip

.PHONY: test
test:
	./test/runner.py

