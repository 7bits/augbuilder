all: lint 

run:
	streamlit run augbuilder/aug_run.py

lint:
	python -m isort -y
	python -m flake8 .

install:
	pip3 install --upgrade setuptools pip
	pip3 install -r requirements.txt
	make install-dev

install-dev:
	pip3 install -r requirements_lint.txt

.PHONY: dist
dist:
	python setup.py sdist

.PHONY: deploy
deploy:
	twine upload dist/*