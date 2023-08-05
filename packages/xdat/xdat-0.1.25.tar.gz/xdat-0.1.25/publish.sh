rm -rf dist xdat.egg-info
python setup.py sdist
twine upload dist/*
rm -rf dist xdat.egg-info
