#!/bin/sh
export KIVY_UNITTEST="true"
py.test -v --tb=short _tests/end_to_end/tests.py
py.test -v _tests/unit/tokenizer_tests.py
py.test -v _tests/unit/word_predictor_tests.py
