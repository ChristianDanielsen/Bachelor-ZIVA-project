import os
import sys
import maya.cmds as cmds

print 'In User ZIVA Setup'

sys.path.append('C:/Users/Christian/Documents/GitHub/ZIVA_PYTHON')
cmds.evalDeferred('import startup')