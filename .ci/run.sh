#!/bin/bash

readonly THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

trap exit SIGINT

# Check style.
echo "Checking style ..."

python3 -m flake8 "${THIS_DIR}/../pacai" --config="${THIS_DIR}/flake8.cfg"
if [[ $? -eq 0 ]]; then
    echo "Style passed!"
else
    echo "Style failed. :("
fi

# Run tests.
echo "Running tests ..."

"${THIS_DIR}/../run_tests.py"
