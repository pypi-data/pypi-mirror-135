#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:${PWD}/src
cd src

# Compute Current version
pp3dv=`python3 -c "import pypos3d; print(pypos3d.__version__)"`
viewer3dv=`python3 -c "import pypos3dv; print(pypos3dv.__version__)"`

# Prepare the delivery of the 'embedded' version for LibreOffice
zip -r pypos3d.ooo/pypos3d.zip langutil pypos3d pypos3dv
cd ..

# Generate the Setup file
sv=s/pypos3d.__version__/${pp3dv}/g


# Use the same REAMDE file for both library and viewer
cp README-lib.md README.md

# Prepare library distrib
sed $sv setup_gen.py > setup.py
rm -f MANIFEST.in
python3 setup.py sdist
rm -f setup.py

# Prepare viewer distrib
sed s/pypos3dv.__version__/${viewer3dv}/g setup-viewer_gen.py > setup.py
python3 setup.py sdist
rm -f setup.py

# Prepare Unit Tests package distrib
cp README-devtu.md README.md
sed $sv setup-tu_gen.py > setup.py
cp MANIFEST-tu.lst  MANIFEST.in
python3 setup.py sdist
rm -f MANIFEST.in README.md


if [ $1 == "test" ]; then
  echo "Test delivery"
  python3 -m twine upload --repository testpypi dist/pypos3d-${pp3dv}.tar.gz
  python3 -m twine upload --repository testpypi dist/pypos3dv-${viewer3dv}.tar.gz
  python3 -m twine upload --repository testpypi dist/pypos3dtu-${pp3dv}.tar.gz
else
  python3 -m twine upload --repository pypi dist/pypos3d-${pp3dv}.tar.gz
  python3 -m twine upload --repository pypi dist/pypos3dv-${viewer3dv}.tar.gz
  python3 -m twine upload --repository pypi dist/pypos3dtu-${pp3dv}.tar.gz
fi


if [ $1 == "test" ]; then
  echo "Test done"
else
  #sh ./deliver-LO.sh ${pp3dv}
  echo "Niet"
fi

