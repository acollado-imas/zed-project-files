#!/bin/bash

# Hay que definir la VENV "BUILD_DIR"
# Hay que tener configurado en qtchooser un qt6

mkdir -p $BUILD_DIR
cd $BUILD_DIR
QT_SELECT=qt6 qmake $ZED_WORKTREE_ROOT -spec linux-g++ CONFIG+=qtquickcompiler
make -j$(nproc)
