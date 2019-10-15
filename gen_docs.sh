#!/bin/bash

readonly THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

trap exit SIGINT

pdoc3 --config show_inherited_members=True --html --force pacai
