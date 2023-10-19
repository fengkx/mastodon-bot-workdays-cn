all: code-gen lint test
.PHONY: all

code-gen = src/mastodon_bot/holidays/model.py

$(code-gen):
	pdm run datamodel-codegen --url 'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/schema.json' --input-file-type jsonschema --output src/mastodon_bot/holidays/model.py --class-name HolidayData

.PHONY: code-gen
code-gen: $(code-gen)

.PHONY: mypy
mypy:
	pdm run mypy src

.PHONY: black
black:
	pdm run black src tests

.PHONY: ruff
ruff:
	pdm run ruff src --fix

.PHONY: lint
lint: mypy black ruff

.PHONY: test
test:
	pdm run pytest tests -s --cov=mastodon_bot --cov-fail-under=80 --cov-report term-missing
