#!/bin/bash

ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

pip install ${ROOT_PATH} --upgrade --force --ignore-installed
