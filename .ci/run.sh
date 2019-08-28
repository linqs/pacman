#!/bin/bash

readonly THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

trap exit SIGINT

exitStatus=0

# Check style.
echo "Checking style ..."

python3 -m flake8 "${THIS_DIR}/../pacai" --config="${THIS_DIR}/flake8.cfg"
if [[ $? -eq 0 ]]; then
    echo "Style passed!"
else
    echo "Style failed. :("
    exitStatus=1
fi

# Run tests.
echo "Running tests ..."

"${THIS_DIR}/../run_tests.py"
if [[ $? -eq 0 ]]; then
    echo "Tests passed!"
else
    echo "Tests failed. :("
    exitStatus=1
fi

exit ${exitStatus}
