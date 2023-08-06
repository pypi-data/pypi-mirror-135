# cloudomate-pypi-package-files
## Prepare and uploading the package
You will need the PyPi user-id and password on twine upload
```
sudo apt install python-minimal
python get-pip.py
pip install twine
python setup.py sdist
twine upload dist/*
```
