#!/bin/bash
set -ex

curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain stable -y
export PATH="$HOME/.cargo/bin:$PATH"

for PYBIN in /opt/python/cp{36,37,38,39}*/bin; do
    "${PYBIN}/pip" install -U setuptools wheel setuptools-rust
    "${PYBIN}/python" setup.py bdist_wheel
done

for whl in dist/*.whl; do
    auditwheel repair "$whl" -w dist/
done

# Keep only manylinux wheels
rm dist/*-linux_*

# Upload wheels
/opt/python/cp37-cp37m/bin/pip install -U awscli
export DIST_DIR=$(/opt/python/cp37-cp37m/bin/python setup.py -V)
/opt/python/cp37-cp37m/bin/python -m awscli s3 sync --exact-timestamps ./dist "s3://pierogis/dist/$DIST_DIR"