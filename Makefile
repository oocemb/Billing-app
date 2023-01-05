deps:    ## Install dependencies
	python -m pip install --upgrade pip
	pip install -r lint-requirements.txt
	pip install -r billing_app/requirements.txt
create-dir:
	mkdir -p reports/wemake-python-styleguide/
	mkdir -p reports/mypy/

lint: create-dir ## Lint and static-check
	black --check .
	flake8 . --exit-zero --config=setup.cfg  --htmldir=reports/wemake-python-styleguide/
	mypy billing_app --config-file=setup.cfg --html-report reports/mypy/
