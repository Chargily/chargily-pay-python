.PHONY: test

test:
	python -m unittest discover -s tests -p 'test_*.py'

build:
	python -m build

publish:
	python -m twine upload dist/*