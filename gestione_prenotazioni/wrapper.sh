#!/bin/bash
srcPath=/usr/src/app
currDir=$(pwd)
tstPath="$srcPath/test"
cd $tstPath
python "$tstPath/run_all_tests.py"
if [[ $? -eq 0 ]]
then
  cd $currDir
	python "$srcPath/app.py"
else
	echo "wrapper.sh: app start aborted because some tests didn't pass"
fi
