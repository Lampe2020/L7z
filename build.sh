#!/bin/bash

cd locales
source compile_locales.sh
cd ..

main_script='l7z.py'
tmpdir_name="/tmp/$(echo $main_script | md5sum | awk '{ print $1 }')"
echo "tmpdir_name='${tmpdir_name}_*'"
rm -rvf "*.spec" "dist_*" "${tmpdir_name}_*"    # Remove files that may get in the way if they're there FIXME: Does nothing?

cd ./locales
if [ $? == 0 ]
then
    ./move_transl.sh
    cd ..
fi

pip3 install -r requirements.txt
pip3 install --upgrade PyInstaller PyCrypto
#TODO: Add all resources to the package!
python3 -m PyInstaller --workpath="${tmpdir_name}_build_linux" --distpath=./dist_linux --icon=lampe2020_logo.png --onefile $main_script

# This part is kinda unecessary as there already is a GUI on Window$. I still include it here in case anyone wants to use this on Window$.
#
#wine --version > /dev/null
#if [ ! -z $? ]
#then
#    wine python --version > /dev/null
#    if [ ! -z $? ]
#    then
#        wine python -m pip install -r requirements.txt
#        wine python -m pip install --upgrade PyInstaller PyCrypto
#        wine python -m PyInstaller --workpath="Z:${tmpdir_name}_build_win" --distpath=.\\dist_win --icon=lampe2020_logo.png --onefile $main_script
#    else
#        echo "Did not pack for win, install Python in default WINE prefix first!"
#    fi
#fi

#TODO: Add MacOS build support (if even necessary)!

rm -rvf "*.spec" "${tmpdir_name}_*" #FIXME: Does nothing?
