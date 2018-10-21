#!/usr/bin/env sh

set -e


echo "Logging in to docker hub..."
docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
echo "Logged in Docker hub successfully"

echo "Building docker image and tagging with ${CIRCLE_SHA1}"
docker build . -t nicolastrres/backmeup:${CIRCLE_SHA1}
echo "Built successfully"

echo "Pushing it..."
docker push nicolastrres/backmeup
echo "Pushed successfully :)"
