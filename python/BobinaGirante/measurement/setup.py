import sys
from cx_Freeze import setup, Executable

files = ["imagens/"]
includes = ["sip","re","atexit"]
excludes = ["scipy"]
exe = Executable(script="Bobina Girante v1.py", base="Win32GUI", icon = "C:/Users/labimas/Desktop/bobina girante/imagens/quadrupolo.ico")
 
setup(options = {"build_exe": {"includes":includes, "include_files":files, "excludes":excludes}}, executables = [exe])
