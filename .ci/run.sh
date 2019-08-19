#!/bin/bash

trap exit SIGINT

python3 -m flake8 ../pacai --config=./flake8.cfg
if [[ $? -eq 0 ]]; then
    echo "Style passed!"
else
    echo "Style failed. :("
fi
