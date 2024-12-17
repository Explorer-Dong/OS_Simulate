@echo off
g++ %1 -o solution.exe && solution.exe %2 %3 && python main.py