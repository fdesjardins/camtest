#!/bin/bash

sudo apt install -y libpng-dev libjpeg-dev libtiff5-dev
sudo apt install -y libepoxy-dev
sudo apt install -y python3-pip git python3-jinja2

sudo apt install -y libboost-dev
sudo apt install -y libgnutls28-dev openssl libtiff5-dev pybind11-dev
sudo apt install -y qtbase5-dev libqt5core5a libqt5gui5 libqt5widgets5
sudo apt install -y meson cmake
sudo apt install -y python3-yaml python3-ply

sudo apt install -y libglib2.0-dev libgstreamer-plugins-base1.0-dev

cd
git clone https://github.com/raspberrypi/libcamera.git
cd libcamera

meson setup build \
    --buildtype=release \
    -Dpipelines=rpi/vc4,rpi/pisp \
    -Dipas=rpi/vc4,rpi/pisp \
    -Dv4l2=true \
    -Dgstreamer=enabled \
    -Dtest=false \
    -Dlc-compliance=disabled \
    -Dcam=disabled \
    -Dqcam=disabled \
    -Ddocumentation=disabled \
    -Dpycamera=enabled

ninja -C build
sudo ninja -C build install

sudo apt install -y cmake libboost-program-options-dev libdrm-dev libexif-dev
sudo apt install -y meson ninja-build

cd
git clone https://github.com/raspberrypi/rpicam-apps.git
cd rpicam-apps

meson setup build -Denable_libav=false -Denable_drm=true -Denable_egl=false -Denable_qt=false -Denable_opencv=false -Denable_tflite=false
meson compile -C build
sudo meson install -C build
sudo ldconfig