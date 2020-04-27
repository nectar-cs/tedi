#!/bin/bash

docker build . -f RunTestsDockerfile -t ted:tests
docker run ted:tests