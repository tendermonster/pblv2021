import sys
import os
pathTo = os.getcwd()+"/app"
os.chdir("..")
artiDir = os.path.abspath(os.curdir)+"/arti"
martenDir = os.path.abspath(os.curdir)+"/marten"
sys.path.insert(0, pathTo)
sys.path.insert(0, artiDir)
sys.path.insert(0, martenDir)
print(sys.path)

from app import app
