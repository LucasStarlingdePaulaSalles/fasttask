echo "Did you recall updating the version on setup.py?"
sleep 3
rm -rf dist
rm -rf fasttask.egg-info
python -m build
python -m twine check dist/*
python -m twine upload dist/* --verbose