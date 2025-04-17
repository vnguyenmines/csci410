#!/bin/bash

params=("test/StackArithmetic/SimpleAdd/SimpleAdd.vm" "test/StackArithmetic/StackTest/StackTest.vm" "test/MemoryAccess/BasicTest/BasicTest.vm" "test/MemoryAccess/PointerTest/PointerTest.vm" "test/MemoryAccess/StaticTest/StaticTest.vm")

for p in "${params[@]}"; do
    ./VMTranslator "$p"
done

mkdir -p asmtest

find . -type f -name "*.asm" -exec cp {} ./asmtest/ \;