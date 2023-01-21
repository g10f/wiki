#!/bin/bash
tag=$(python apps/version.py)
DOCKER_BUILDKIT=1
docker buildx build --platform linux/amd64,linux/arm64 -t g10f/wiki:$tag -t g10f/wiki:latest . --push
