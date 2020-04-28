#!/bin/bash

if [[ "$1" == "test" ]]; then
  pipenv run python3 -m unittest
else
  echo "Passing following to app.py: $@"
  pipenv run python3 app.py $@
fi