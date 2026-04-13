#!/bin/bash

# Hay que definir la VENV "RELEASE_BUILD_DIR" y "DEBUG_BUILD_DIR"
# Hay que definir la VENV "ZED_WORKTREE_ROOT" si no se esta ejecutando desde Zed
# Hay que tener configurado en qtchooser un qt6

set -e

CLEAN=false
DEBUG=false
RELOAD=false

# Parseo de argumentos
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -d|--debug)
            DEBUG=true
            shift
            ;;
        -r|--reload)
            RELOAD=true
            shift
            ;;
        *)
            echo "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

if [ "$DEBUG" = true ]; then
    BUILD_PATH="$DEBUG_BUILD_DIR"
    echo "Usando build de DEBUG: $BUILD_PATH"
else
    BUILD_PATH="$RELEASE_BUILD_DIR"
    echo "Usando build normal: $BUILD_PATH"
fi

if [ -z "$BUILD_PATH" ]; then
    echo "Error: el directorio de build no está definido"
    exit 1
fi

mkdir -p $BUILD_PATH
cd $BUILD_PATH
QT_SELECT=qt6 qmake $ZED_WORKTREE_ROOT -spec linux-g++ CONFIG+=qtquickcompiler

if [ "$CLEAN" = true ]; then
    echo "Ejecutando clean build..."
    make clean -j"$(nproc)"
fi

if [ "$RELOAD" = true ]; then
    echo "Creando archivo compile_commands.json..."
    make clean -j"$(nproc)"
    bear -- make -j$(nproc)
    mv $BUILD_PATH/compile_commands.json $ZED_WORKTREE_ROOT/
else
    make -j$(nproc)
fi

