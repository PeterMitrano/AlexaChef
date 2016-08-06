#!/bin/bash
find . -name "*.py" -exec pylint -E '{}' +
find . -name "*.py" -exec yapf -i '{}' +
