#!/bin/bash
BUILD_DIR="/home/acollado/Documentos/Proyectos/Trolley/QT_BUILDS/Desktop_Qt_6_10_1-Debug"
QT_EXECUTABLE="/home/acollado/Qt/6.10.1/gcc_64/bin/"

mkdir -p $BUILD_DIR
cd $BUILD_DIR
$QT_EXECUTABLE/qmake $ZED_WORKTREE_ROOT/SmartTrolley.pro -spec linux-g++ CONFIG+=qtquickcompiler
bear -- make -j$(nproc)
mv $BUILD_DIR/compile_commands.json $ZED_WORKTREE_ROOT
