docker build . -t adlinear
docker tag adlinear eu.gcr.io/second-capsule-253207/adlinear:latest
docker push eu.gcr.io/second-capsule-253207/adlinear:latest