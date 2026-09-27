#!/bin/bash

echo "AClangをトランスパイルしています."
python3 AClang.py

# Pythonの実行が失敗した場合はここで終了
if [ $? -ne 0 ]; then
    echo "トランスパイルに失敗しました."
    exit 1
fi

echo "C++をコンパイルしています."
g++ -std=c++17 -O2 AClang.cpp -o a.out

# C++のコンパイルが失敗した場合はここで終了
if [ $? -ne 0 ]; then
    echo "C++のコンパイルに失敗しました."
    exit 1
fi

echo "正常に終了しました."
./a.out < in.txt > out.txt