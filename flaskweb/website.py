import sys
import os
pathTo = os.getcwd()+"/app"
print(pathTo)
sys.path.insert(0, pathTo)
print(sys.path)
from app import app
