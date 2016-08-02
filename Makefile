all: zip upload test

zip:
	cd src &&	zip -q -r skill.zip state_handlers node_modules *.js package.json

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://src/skill.zip
	rm src/skill.zip
