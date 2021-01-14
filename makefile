SRC=snap_tam/

.PHONY: remove-previous-build build pypi-push-test pypi-push dist pypi-test \
pip-test pypi pip run

# Run
run:
	python3 -m snap_tam

# Package Management
remove-previous-build:
	rm -rf ./dist;
	rm -rf ./build;
	rm -rf ./*.egg-info
build: remove-previous-build
	python3 setup.py sdist bdist_wheel
pypi-push-test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pypi-push:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*; \
	make remove-previous-build

# Aliases
dist: build
pypi-test: pypi-push-test
pip-test: pypi-push-test
pypi: pypi-push
pip: pypi-push
