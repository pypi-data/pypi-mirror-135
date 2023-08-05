#!/bin/bash
#
# deliver-LO.sh VERSION
#
lstfic="../src/pypos3d.ooo/PyPos3D-App-Installer.ods ../src/pypos3d.ooo/PyPos3DLO.ods ../src/pypos3d.ooo/PyPos3DLO-Example.ods ../src/pypos3d.ooo/PyPos3DLO-RyanClothes.ods ../src/pypos3d.ooo/PyPos3DLO-mechanical.ods ../src/pypos3d.ooo/PyPos3d-manual-en.pdf ../CHANGELOG.md ../README-devtu.md ../README-lib.md ../LICENSE ../src/pypos3dapp.py ../src/pypos3dappext.py ../src/pypos3dinstaller.py"
# Build the sourceforge package with its examples
cd dist
mkdir PyPos3DLO
for f in $lstfic
    do
    cp $f PyPos3DLO/
    done

# Create the zip of examples
(cd ../src/pypos3dtu ; zip -r ../../dist/PyPos3DLO/examples.zip srcdata/)

# Create the versioned deliveray zip
zip -r PyPos3DLO-${1}.zip PyPos3DLO
rm -rf PyPos3DLO
cd ..

