# Grade Mage

Auto grader for online quiz.

Use the following command to ensure all the tests are passed:

```
pytest
```

Then execute the following command t generate the wheel:

```
python3 setup.py sdist bdist_wheel
```

Upload the distribution archives to test server:

```
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

