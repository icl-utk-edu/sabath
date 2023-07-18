OA######################################################################
# PYPI
######################################################################


twine:
	pip install -U twine

release:
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository pypi dist/*

