TEST_PATH=./

build:
	sudo apt-get install postgresql postgis binutils libproj-dev gdal-bin
	# TODO: Criar banco, criar usuário e dar grant
	pip install -U pip
	pip install -r requirements.txt
	python manage.py migrate

build-dev: build
	pip install -r dev-requirements.txt

clean-pyc:
	find . -type f -name "*.py[co]" 2> /dev/null -delete; true
	find . -type d -name "__pycache__" 2> /dev/null -delete; true

lint:
	flake8

test: clean-pyc
	py.test --verbose --color=yes -s $(TEST_PATH)
	coverage report -m

run:
	python manage.py runserver
