#!/usr/bin/env bash

set -e

# Change directory to the script directory
cd "$(dirname $0)/.."
BUILDDIR=$(pwd)

function heading() {
  local width=$(tput cols 2> /dev/null)
  [ -z $width ] && width=50

  local text=$1
  # prints '#' for a whole line
  python3 -c "print('#' * ${width})"

  # centers the text
  python3 -c "print(' ' * ((${width} - ${#text}) // 2), end='')"
  echo "$text"

  # prints '#' for a whole line
  python3 -c "print('#' * ${width})"
}

VERSION=$(python3 -c "print(__import__('release').VERSION)")
cat << EOF
     _____      _        _
    |  __ \    | |      | |
    | |__) |__ | | _____| |_ ___
    |  ___/ _ \| |/ / _ \ __/ _ \\
    | |  | (_) |   <  __/ ||  __/
    |_|   \___/|_|\_\___|\__\___|

       debian-package builder

Pokete Version: $VERSION
Project url: https://github.com/lxgr-linux/pokete

This software is licensed under the GPLv3.
You should have gotten an copy of the GPLv3 license anlonside this software.
If not, the license text is available at https://www.gnu.org/licenses/gpl-3.0.txt

EOF

if [ "$1" = "-h" -o "$1" = "--help" ];then
  heading "Help"
  cat << EOF

Use this script if packaging the debian package.
It is a complete automated installation process, after the first run.
This script tries the following things:

  * Installs build dependencies with apt-get
  * Downloads the latest version of the scrap engine
  * Builds the source tar ball with python-setuptools
  * Prepares and builds the actual debian package

A useful routine, when developing this script or the debian package might look
like this:

    $ git restore pyproject.toml setup.py
    $ rm -rf build dist pokete pokete.egg-info scrap_engine
    $ tools/debbuild.sh

If you need more help about this script, please contact
MaFeLP <mafelp@proton.me>.

EOF
fi

if [ -d 'build' ];then
  heading "ERROR"
  echo "Please clean and remove the 'build' directory before running this script!"
  exit 1
fi

heading "Installing prerequirements..."
sudo apt-get install -y \
  build-essential \
  devscripts \
  debhelper \
  debmake \
  golang \
  pkg-config \
  pulseaudio \
  libasound2-dev \
  python3-pip \
  dh-python \
  python3-all

#heading "Installing python setuptools>=61..."
#pip3 install 'setuptools>=61'

heading "Preparing pokete build..."
patch "playsound/__init__.py" < "packages/deb/playsound_lib.patch"
rm -v playsound/libplaysound*
python3 -c "__import__('setup').main()"
cp -v packages/deb/setup.py ./setup.py
rm -v pyproject.toml

heading "Downloading scrap_engine..."
mkdir scrap_engine
curl -o "scrap_engine/__init__.py" "https://raw.githubusercontent.com/lxgr-linux/scrap_engine/master/scrap_engine.py"

heading "Building sdist of pokete with setuptools..."
python3 setup.py sdist

heading "Preparing debian build environment..."

mkdir build
mv "dist/pokete-${VERSION}.tar.gz" build
cd build
tar xmvf "pokete-${VERSION}.tar.gz"
cd "pokete-${VERSION}"

heading "Preparing the debian source package..."
mkdir debian
cp -vr ../../packages/deb/assets/* .
debmake -b":python3"

heading "Building actual debian package..."
debuild -uc

heading "Finished"
cd "${BUILDDIR}"
echo "Built debian package at $(pwd)/$(ls build/pokete_${VERSION}-*.deb)"
