# pyenv-checker
 


# Publishing


```bash
twine upload --repository testpypi dist/*
```

Updating the package

To extend the functionality, create another branch and make updates to it. After that:

1. Create tests for it
2. Bump the version in setup.py
3. Bump the version of the whl file in the CircleCI config file
4. Update the ChangeLog
5. Push to GitHub
