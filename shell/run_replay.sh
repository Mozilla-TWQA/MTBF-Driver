#!/bin/bash

export MTBF_REPLAY=replay
mtbf --testvars=testvars.json --address=localhost:2828 test_dummy_case.py
