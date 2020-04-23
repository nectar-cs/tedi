#!/bin/bash
docker build . -t interp
kubectl delete pod -l app=interp -n moz
kubectl apply -f pod.yaml