#!/bin/sh
export KIVY_UNITTEST="true"
py.test -v --tb=short _tests/end_to_end/test.py
