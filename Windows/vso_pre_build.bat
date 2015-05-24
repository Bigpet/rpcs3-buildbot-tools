@echo off
REM setup the submodules for VSO

cd ..
cd ..
echo on
git submodule init 
git submodule deinit llvm
git submodule update
