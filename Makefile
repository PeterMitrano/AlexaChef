all: zip upload

zip:
	mkdir -p build
	cp src/index.js build
	cp src/AlexaSkill.js build
	cd build &&	zip skill.zip index.js AlexaSkill.js

upload:
	aws lambda update-function-code --function-name ColorExpert --zip-file fileb://build/skill.zip
