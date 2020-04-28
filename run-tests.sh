#!/bin/bash
docker build . -t teds
docker run teds test