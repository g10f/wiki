#!/bin/bash
VERSION=1.0.11
APP=server

sed -i "s/__version__ =.*/__version__ = '${VERSION}'/" apps/${APP}/__init__.py