all: zip upload

zip:
	mkdir -p build
	cp -r ./venv/lib/python2.7/site-packages/* build
	cp -r ./my_cookbook/* build
	find build -name *.swp | xargs rm -f
	cd build &&	zip -q -r skill.zip *

upload: zip
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip
