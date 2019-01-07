import maya.cmds as cmds
print "UI"

def ZRIGARM(*args):
	print "ZIVA_ARM_RIG"

mymenu = cmds.menu('ZMENU', label='ZMENU', to=True, p='MayaWindow')
cmds.menuItem(label='ZARM_RIG', p=mymenu, command=ZRIGARM)


	