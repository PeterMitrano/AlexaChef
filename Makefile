all: zip upload

zip:
	mkdir -p build
	cp -r src/node_modules build
	cp src/index.js build
	cp src/package.json build
	cd build && zip -r skill.zip node_modules index.js package.json

upload:
	aws lambda update-function-code --function-name ColorExpert --zip-file fileb://build/skill.zip
