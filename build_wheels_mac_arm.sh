#!/bin/bash
#set -ex

# only 3.9 on arm with pyenv
for PYBIN in ~/.pyenv/versions/{3.8,3.9}*/bin; do
    "${PYBIN}/pip" install -U setuptools wheel setuptools-rust
    "${PYBIN}/python" setup.py bdist_wheel
done

# upload wheels
~/.pyenv/versions/3.9.1/bin/pip install -U awscli
export DIST_DIR=$(~/.pyenv/versions/3.9.1/bin/python setup.py -V)
~/.pyenv/versions/3.9.1/bin/python -m awscli s3 sync --exact-timestamps ./dist "s3://pierogis/dist/$DIST_DIR"