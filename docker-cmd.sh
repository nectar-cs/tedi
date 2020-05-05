#!/bin/bash

if [[ "$1" == "test" ]]; then
  pipenv run coverage run -m unittest
  if [[ ! -z "${CODECOV_TOKEN}" ]]; then
    pipenv run coverage report -m
    bash <(curl -s https://codecov.io/bash); exit 0
  else
    echo "No CodeCov token found"
  fi
else
  pipenv run python3 app.py "$@"
fi