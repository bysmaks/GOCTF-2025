#!/bin/bash
set -e

go build -o checker_go checker_go.go
g++ checker_cpp.cpp -o checker_cpp -lssl -lcrypto
upx -o checker_cpp_upx checker_cpp

exec python3 bot.py
