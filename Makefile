all: zip upload test

zip:
	mkdir -p build
	cp -r src/node_modules build
	cp src/*.js build
	cp src/package.json build
	cd build && zip -q -r skill.zip node_modules *.js package.json

upload:
	aws lambda update-function-code --function-name MyCookbook --zip-file fileb://build/skill.zip

FILE=test/payload.json
PAYLOAD := $(shell cat ${FILE})

.PHONY: test
test:
	@aws lambda invoke --invocation-type RequestResponse --function-name MyCookbook --log-type Tail \
		--payload '$(PAYLOAD)' ./build/output.log > ./build/encoded_tail.json
	@cat ./build/output.log | python -m json.tool
	@./tail_helper.py ./build/encoded_tail.json

