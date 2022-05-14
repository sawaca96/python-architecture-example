#!/bin/bash

set -e

pre-commit install
docker-compose up --build
