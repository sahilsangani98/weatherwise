#!/bin/bash -x

coverage run -m pytest
coverage report -m
coverage html