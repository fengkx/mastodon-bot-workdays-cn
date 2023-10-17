code-gen:
	datamodel-codegen --url 'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/schema.json' --input-file-type jsonschema --output src/mastodon_bot/holidays/model.py --class-name HolidayData

all: code-gen

.PHONY: all