#!/bin/bash

mkdir -p yocto/sources

cd yocto/sources
git clone git://git.yoctoproject.org/poky -b kirkstone
git clone git://git.yoctoproject.org/meta-raspberrypi -b kirkstone
git clone git://git.openembedded.org/meta-openembedded -b kirkstone
git clone git://git.yoctoproject.org/meta-virtualization -b kirkstone

cd -
