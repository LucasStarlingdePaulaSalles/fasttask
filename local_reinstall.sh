pip uninstall fasttask -y
python setup.py sdist bdist_wheel
pip install -e .