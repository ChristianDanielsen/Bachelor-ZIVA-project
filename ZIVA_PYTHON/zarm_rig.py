import maya.cmds
import maya.cmds as cmds
#Arm chain list rig
#create a list to store name and position of joints.
#jntlist stores 4 other lists the names are the first in the list [0], and the position is the secound in the list [1].
BNjntlist = [['BN_shoulder_jnt', [0.0, 0.0, 0.0]], ['BN_elbow_jnt', [2.0, 0.0, 2.0]], ['BN_Wrist_jnt', [0.0, 0.0, 0.0]], ['BN_wristEnd_jnt', [0.0, 0.0, 2.0]]]
IKjntlist = [['BN_shoulder_jnt', [0.0, 0.0, 0.0]], ['BN_elbow_jnt', [2.0, 0.0, 2.0]], ['BN_Wrist_jnt', [0.0, 0.0, 0.0]], ['BN_wristEnd_jnt', [0.0, 0.0, 2.0]]]
FKjntlist = [['BN_shoulder_jnt', [0.0, 0.0, 0.0]], ['BN_elbow_jnt', [2.0, 0.0, 2.0]], ['BN_Wrist_jnt', [0.0, 0.0, 0.0]], ['BN_wristEnd_jnt', [0.0, 0.0, 2.0]]]
	
def createJoint(jntinfo):
	#create a for loop for each item in the list do the following
	for item in jntinfo:
	#create a joint with the name equal to the first lists in jntlist
	#make the translate equal to the position of the secound lists 
	cmds.joint( n=item[0], p=item[1] )

#create BN joints
createJoint(BNjntlist)
cmds.select(d=True)
#create IK joints
createJoint(IKjntlist)
cmds.select(d=True)
#create FK joints
createJoint(FKjntlist)
cmds.select(d=True)
#Arm chain rig

#create Bind Joints
cmds.joint ( n= "BN_shoulder_jnt", p= [-8, 0, 0])
cmds.joint ( n= "BN_elbow_jnt", p= [-6, 0, -2])
cmds.joint ( n= "BN_wrist_jnt", p= [-3, 0, 0])
cmds.joint ( n= "BN_wristEnd_jnt", p= [-1, 0, 0])
cmds.select(d=True)

#create FK joints

cmds.joint ( n= "FK_shoulder_jnt", p= [-8, 0, 0])
cmds.joint ( n= "FK_elbow_jnt",p= [-6, 0, -2])
cmds.joint ( n= "FK_wrist_jnt", p= [-3, 0, 0])
cmds.joint ( n= "FK_wristEnd_jnt", p= [-1, 0, 0])
cmds.select(d=True)

#create IK joints

cmds.joint ( n= "IK_shoulder_jnt", p= [-8, 0, 0])
cmds.joint ( n= "IK_elbow_jnt",p= [-6, 0, -2])
cmds.joint ( n= "IK_wrist_jnt", p= [-3, 0, 0])
cmds.joint ( n= "IK_wristEnd_jnt", p= [-1, 0, 0])
cmds.select(d=True)

#create FK rig

#create IK rig

#create IK handle
cmds.ikHandle(n='ikh_arm', sj='IK_shoulder_jnt', ee='IK_wrist_jnt', sol='ikRPsolver', p=2, w=1)

#create ik control

#get world space position of Ik wrist joint
pos = cmds.xform('IK_wrist_jnt', q=True, t=True, ws=True)

#create an empty group
cmds.group(em=True, name='grp_ctrl_ikWrist')

#create cricle control object
cmds.circle( n='ctrl_ikWrist', nr=(0, 0, 1), c=(0, 0, 0) )

#lock and hide unnesesary attributes

#lock and hide scale
cmds.setAttr('ctrl_ikWrist.scaleX', lock=True)
cmds.setAttr('ctrl_ikWrist.scaleY', lock=True)
cmds.setAttr('ctrl_ikWrist.scaleZ', lock=True, )

#lock and hide rotate
cmds.setAttr('ctrl_ikWrist.rotateX', lock=True)
cmds.setAttr('ctrl_ikWrist.rotateY', lock=True)
cmds.setAttr('ctrl_ikWrist.rotateZ', lock=True)

#lock the visibility
cmds.setAttr('ctrl_ikWrist.v', lock=True)

#parent control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

#move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)

#parent constraint ikh to ctrl
cmds.parentConstraint('ikh_arm', 'ctrl_ikWrist')

#connect FK and IK to Bind joints