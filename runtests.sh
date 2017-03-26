#!/bin/bash
coverage run --source=ej,. --omit=tests/* -m unittest discover -s ./tests -v
coverage report
