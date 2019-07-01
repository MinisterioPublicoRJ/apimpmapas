TEST_PATH=./

clean-pyc:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	flake8

test: clean-pyc
	py.test --verbose --color=yes -s $(TEST_PATH)

run:
	python manage.py runserver
