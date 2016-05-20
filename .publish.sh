#!/bin/bash -e

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  docker login -e="$DOCKER_EMAIL" -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Deploying image to docker hub for master (latest)"
    docker tag depiltech_odoo camptocamp/depiltech_odoo:latest
    docker push "camptocamp/depiltech_odoo:latest"
  elif [ ! -z "$TRAVIS_TAG" ]; then
    echo "Deploying image to docker hub for tag ${TRAVIS_TAG}"
    docker tag depiltech_odoo camptocamp/depiltech_odoo:${TRAVIS_TAG}
    docker push "camptocamp/depiltech_odoo:${TRAVIS_TAG}"
  elif [ ! -z "$TRAVIS_BRANCH" ]; then
    echo "Deploying image to docker hub for branch ${TRAVIS_BRANCH}"
    docker tag depiltech_odoo camptocamp/depiltech_odoo:${TRAVIS_BRANCH}
    docker push "camptocamp/depiltech_odoo:${TRAVIS_BRANCH}"
  else
    echo "Not deploying image"
  fi
fi
