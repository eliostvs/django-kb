VERBOSITY := 1
LOCALPATH := $(CURDIR)/knowledge/

.PHONY: clean test coverage report lint

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@find . -name "__pycache__" -print0 | xargs -0 rm -rf
	@rm -rf .coverage
	@rm -rf whoosh_index/*

test: clean
	@python runtests.py test -v $(VERBOSITY) $(APP) --failfast

coverage: clean
	@coverage run runtests.py test --failfast

report:
	@coverage report -m

lint:
	@flake8 $(LOCALPATH)
