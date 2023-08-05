#!/bin/bash

# To be executed before SVN commit
tulist="tuPaveList.py tuPlaneCut.py tuGeomGroup.py tuWaveGeom.py tuPoserMeshed.py tuFigure.py tuPoserFile.py tuQSlim.py tuWFBasic.py"

tuPyVM="python3.9 python3.6"

# Compute Current version
pp3dv=`(export PYTHONPATH=${PYTHONPATH}:${PWD}/src ; python3 -c "import pypos3d; print(pypos3d.__version__)" )`

for PYTHON in ${tuPyVM}
  do
  export RESCOV=${PWD}/coverage_results-${PYTHON}.txt
  export RESTU=${PWD}/tu_results-${PYTHON}.txt

  echo "Unit Tests of pypos3d version" $pp3dv "on" `date` " env:" ${PYTHON}
  echo "Unit Tests of pypos3d version" $pp3dv "on" `date` " env:" ${PYTHON} > $RESTU
  
  # Launch all Unitests
  
  cd src/pypos3dtu 
  PYTHONPATH=${PWD}/..
  export PYTHONPATH
  
  # Check results dirs (for distributed packages)
  [[ -d tures ]] || mkdir tures
  [[ -d tulog ]] || mkdir tulog
  
  for tumod in $tulist
    do
    ${PYTHON} -m unittest -v ${tumod} > tulog/${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Success" >> $RESTU  &
    done
  wait $(jobs -p)
  grep "^Ran " tulog/*.log >> $RESTU
  
  # Clean Coverage DB
  rm -f .coverage*
  for tumod in $tulist
    do
    # coverage run --append --source=../src/pypos3d -m unittest ${tumod} > tures/${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Cov Success" 2>&1 $RESCOV
    ${PYTHON} -m coverage run --parallel-mode --source=../pypos3d -m unittest ${tumod} > tulog/cov-${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Cov Success" 2>&1 >> $RESTU &
    done
  wait $(jobs -p) 
  grep "^Ran " tulog/cov-*.log >> $RESTU
  
  # Combine the various .coverage* files into one .coverage
  ${PYTHON} -m coverage combine --append
  
  # Generate Coverage Report
  # cd ../.metadata/.plugins/org.python.pydev.debug/coverage/
  ${PYTHON} -m coverage report  > ${RESCOV}
  cd -
  
  # Clean tures
  rm -f src/pypos3dtu/tures/*
  done
