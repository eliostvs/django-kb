VERBOSITY := 1
LOCALPATH := $(CURDIR)/knowledge/
SCRIPT := manage.py

.PHONY: clean test coverage report lint

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@find . -name "__pycache__" -print0 | xargs -0 rm -rf
	@rm -rf .coverage
	@rm -rf whoosh_index/*

test: clean
	@python $(SCRIPT) test -v $(VERBOSITY) $(APP) --failfast

coverage: clean
	@coverage run $(SCRIPT) test --failfast

report:
	@coverage report -m

lint:
	@flake8 $(LOCALPATH)
