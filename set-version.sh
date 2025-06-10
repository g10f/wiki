#!/bin/bash
VERSION=1.0.19
APP=server

sed -i "s/__version__ =.*/__version__ = '${VERSION}'/" apps/${APP}/__init__.py

sed -i "s/__version__ =.*/__version__ = '${VERSION}'/" ../afd-wiki/apps/${APP}/__init__.py
sed -i "s/FROM ghcr\.io\/g10f\/wiki:.*/FROM ghcr\.io\/g10f\/wiki:${VERSION}/" ../afd-wiki/Dockerfile

sed -i "s/__version__ =.*/__version__ = '${VERSION}'/" ../dwbn-wiki/apps/${APP}/__init__.py
sed -i "s/FROM ghcr\.io\/g10f\/wiki:.*/FROM ghcr\.io\/g10f\/wiki:${VERSION}/" ../dwbn-wiki/Dockerfile
