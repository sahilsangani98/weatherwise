#!/bin/bash -x

# To remove cache files
find . -type d -name "__pycache__" -exec test -d {} \; -exec rm -r {} +

# To remove htmlcov
if [ -d "htmlcov" ]; then
    rm -r htmlcov
fi

# To remove coverage
if [ -f ".coverage" ]; then
    rm .coverage
fi

# To rpytest_cache
if [ -d ".pytest_cache" ]; then
    rm -r ".pytest_cache"
fi

