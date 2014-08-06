VERBOSITY := 1
NAME = 'kb'
LOCALPATH := $(CURDIR)/$($NAME)/
SCRIPT := manage.py

.PHONY: clean test coverage report lint build register

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@find . -name "__pycache__" -print0 | xargs -0 rm -rf
	@rm -rf .coverage
	@rm -rf whoosh_index/*

test: clean
	@python $(SCRIPT) test -v $(VERBOSITY) $(APP) --failfast

test.integration: clean
	@python $(SCRIPT) test --pattern="integration_*.py" -v $(VERBOSITY) $(APP) --failfast

test.all: test test.integration

coverage: clean
	@coverage run $(SCRIPT) test --failfast

report:
	@coverage report -m

lint:
	@flake8 $(LOCALPATH)

build:
	@rm -rf build
	@rm -rf dist
	@rm -rf django_kb.egg-info
	python setup.py sdist
	python setup.py bdist_wheel

register.test: build
	python setup.py register -r test
	python setup.py sdist upload -r test --identity="Elio Esteves Duarte" --sign
	python setup.py bdist_wheel upload -r test --identity="Elio Esteves Duarte" --sign

register: build
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi --identity="Elio Esteves Duarte" --sign
	python setup.py bdist_wheel upload -r pypi --identity="Elio Esteves Duarte" --sign
