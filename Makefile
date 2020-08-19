all: lint 

run:
	streamlit run aug_run.py

lint:
	python -m isort -y
	python -m flake8 .

install:
	pip3 install --upgrade setuptools pip
	pip3 install -r requirements.txt
	make install-dev

install-dev:
	pip3 install -r requirements_lint.txt


