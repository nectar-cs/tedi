#!/bin/bash

if [[ "$1" == "test" ]]; then
  gem list | grep kerbi
  gem install kerbi
  gem update kerbi
  gem list | grep kerbi
  pipenv run coverage run -m unittest
  if [[ -n "${CODECOV_TOKEN}" ]]; then
    pipenv run coverage report -m
    bash <(curl -s https://codecov.io/bash); exit 0
  else
    echo "No CodeCov token found"
  fi
elif [[ "$1" == "sleep" ]]; then
  echo "Going to sleep..."
  while true; do sleep 30; done;
else
  pipenv run python3 app.py "$@"
fi