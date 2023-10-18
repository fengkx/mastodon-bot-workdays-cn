code-gen:
	pdm run datamodel-codegen --url 'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/schema.json' --input-file-type jsonschema --output src/mastodon_bot/holidays/model.py --class-name HolidayData

all: code-gen lint

mypy:
	pdm run mypy src

black:
	pdm run black src
ruff:
	pdm run ruff src --fix

lint: mypy black ruff

.PHONY: all
