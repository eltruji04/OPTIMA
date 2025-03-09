#!/usr/bin/env bash
set -euo pipefail

python3 -m venv venv
source venv/bin/activate
cd ./OPTIMA-main
pip install -U pip
pip install -U -e .