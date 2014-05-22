#!/bin/bash

## Not for use, a template for mtbf command line input

MTBF_TIME=10h MTBF_CONF=conf/local.json mtbf --address=localhost:2828 --testvars=testvars.json tests/test_dummy_case.py
