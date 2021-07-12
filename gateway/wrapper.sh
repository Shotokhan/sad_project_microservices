#!/bin/bash
srcPath=/usr/src/app
python "$srcPath/test/run_all_tests.py"
if [[ $? -eq 0 ]]
then
	python "$srcPath/app.py"
else
	echo "wrapper.sh: app start aborted because some tests didn't pass"
fi
