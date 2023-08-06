# Develop AIbro_lib

1. git clone the repo to local computer
2. `python3 -m venv venv; .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `pre-commit install`
5. Create a `.env` file to contain environment variables:

```
SERVER_HOST="localhost"
IS_LOCAL=true
```

5. Run the function of your choice to debug

# Code Commit Formatter

Please double check pre-commit is working before pushing code to github:

1. git add (the file you want)
2. git commit -m (your message here)
3. git push

# Code review

All new changes should be reviewed before merged.

# Update dependencies

DO NOT directly run `pip install` or `pip freeze`. Instead, add the library to `requirements.in` then run `pip-compile` for better dependency management (need to run `pip install pip-tools` first)

# Update library versions

1. Your change is reviewed and merged
2. Pump version number in `setup.py`
3. run `rm -r dist; python3 setup.py sdist; twine upload dist/*`
4. Check that your version has been updated

# Deploy library

Deploy on https://aipaca.ai:

- set SERVER_HOST to "https://aipaca.ai"; set IS_LOCAL to false.
  Deploy on other non-local servers:
- set SERVER_HOST to {target_server_ip}.
