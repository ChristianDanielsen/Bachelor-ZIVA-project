import maya.cmds as cmds
#Arm chain list rig
#create a list to store name and position of joints.
#jntlist stores 4 other lists the names are the first in the list [0], and the position is the secound in the list [1].
DRVjntlist = [['DRV_shoulder_jnt', [0.0, 0.0, 0.0]], ['DRV_elbow_jnt', [2.0, 0.0, 2.0]], ['DRV_Wrist_jnt', [0.0, 0.0, 0.0]], ['DRV_wristEnd_jnt', [0.0, 0.0, 2.0]]]
IKjntlist = [['IK_shoulder_jnt', [0.0, 0.0, 0.0]], ['IK_elbow_jnt', [2.0, 0.0, 2.0]], ['IK_Wrist_jnt', [0.0, 0.0, 0.0]], ['IK_wristEnd_jnt', [0.0, 0.0, 2.0]]]
FKjntlist = [['FK_shoulder_jnt', [0.0, 0.0, 0.0]], ['FK_elbow_jnt', [2.0, 0.0, 2.0]], ['FK_Wrist_jnt', [0.0, 0.0, 0.0]], ['FK_wristEnd_jnt', [0.0, 0.0, 2.0]]]

rig_data = {}	
rig_data['IKjnts'] = ['IK_shoulder_jnt', 'IK_elbow_jnt', 'IK_Wrist_jnt', 'IK_wristEnd_jnt']
rig_data['FKjnts'] = ['FK_shoulder_jnt', 'FK_elbow_jnt', 'FK_Wrist_jnt', 'FK_wristEnd_jnt']
rig_data['DRVjnts'] = ['DRV_shoulder_jnt', 'DRV_elbow_jnt', 'DRV_Wrist_jnt', 'DRV_wristEnd_jnt']
rig_data['BNjnts'] = ['BN_shoulder_jnt', 'BN_elbow_jnt', 'BN_Wrist_jnt', 'BN_wristEnd_jnt']
rig_data['IKcontrols'] = ['ctrl_ik_arm',' ikh_arm','ctrl_pv_arm']
rig_data['FKcontrols'] = ['ctrl_fk_shoulder', 'ctrl_fk_elbow', 'ctrl_fk_wrist']
rig_data['positions'] = [[0.0, 0.0, 0.0], [2.0, 0.0, 2.0], [0.0, 0.0, 0.0], [0.0, 0.0, 2.0]] 

class Rig_Arm:
	def rig_arm(self):
		#create DRV joints
	self.createJoint(DRVjntlist)
	cmds.select(d=True)
	#create IK joints
	self.createJoint(IKjntlist)
	cmds.select(d=True)
	#create FK joints
	self.createJoint(FKjntlist)
	cmds.select(d=True)	
	
	#create IK rig
	#create IK handle
	ikh = cmds.ikHandle(n='ikh_arm', sj='IK_shoulder_jnt', ee='IK_wrist_jnt', sol='ikRPsolver', p=2, w=1)

	ikctrlinfo = [[IKjntlist[2][1], 'ctrl_ik_arm', 'grp_ctrl_ik_arm']]
	self.createControl(ikctrlinfo)

	pvpos = calculatePVPosition([IKjntlist[0][0], IKjntlist[1][0], IKjntlist[2][0]])
	pvctrlinfo = [[pvpos, 'ctrl_pv_arm', 'grp_ctrl_pv_arm']]
	self.createControl(pvctrlinfo)

	#parent ikh to ctrl

	cmds.parent('ikh_arm', 'ctrl_ik_arm')

	# PV constraint

	cmds.poleVectorConstraint(pvctrlinfo[0][1], ikh[0])

	#orient contraint arm ik_wrist to ctrl_arm

	cmds.orientConstraint(ikctrlinfo[0][1], IKjntlist[2][0], mo=True)

	#create fk rig

	fkctrlinfo = [[FKjntlist[0][1], 'ctrl_fk_shoulder', 'grp_ctrl_fk_shoulder'], 
	[FKjntlist[1][1], 'ctrl_fk_elbow', 'grp_ctrl_fk_elbow'],
	[FKjntlist[2][1], 'ctrl_fk_wrist', 'grp_ctrl_fk_wrist']]

	self.createControl(fkctrlinfo)

	# Parent fk controls
	cmds.parent(fkctrlinfo[1][2], fkctrlinfo[0][1])
	cmds.parent(fkctrlinfo[2][2], fkctrlinfo[1][1])	


	def createJoint(self, jntinfo):
		#create a for loop for each item in the list do the following
		for item in jntinfo:
		#create a joint with the name equal to the first lists in jntlist
		#make the translate equal to the position of the secound lists 
		cmds.joint( n=item[0], p=item[1] )


	def createControl(self, ctrlinfo):
		for info in ctrlinfo:
			
			#create ik control
			#get posistion of wrist joint 
			pos = info[0]
			#make an empty group
			ctrlgrp = cmds.grp( em=True, name=info[2] )
			#create the circle object
			ctrl = cmds.circle( n=info[1], nr=(0, 0, 1), c=(0, 0, 0) )
			#parent control to control group
			cmds.parent(ctrl, ctrlgrp)
			#move the group the the position of the joint
			cmds.xform(ctrlgrp, t=pos, ws=True)

	def calculatePVPosition(self, jnts):
		from maya import cmds , OpenMaya
		#feed it 3 joints
		start = cmds.xform(jnts[0] ,q=True ,ws=True, t=True)
		mid = cmds.xform(jnts[1] ,q=True ,ws=True, t=True)
		end = cmds.xform(jnts[2] ,q=True ,ws=True, t=True)
		#make vector positions
		startV = OpenMaya.MVector(start[0] ,start[1],start[2])
		midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
		endV = OpenMaya.MVector(end[0] ,end[1],end[2])
		#minus the vectors
		startEnd = endV - startV
		startMid = midV - startV
		#make a dotProdukt to get a vector posistion and transfer that
		#information to use to control
		dotP = startMid * startEnd
		proj = float(dotP) / float(startEnd.length)
		#make a normal position
		startEndN = startEnd.normal()
		projV = startEndN * proj

		arrowV = startMid - projV
		arrowV* = 0.5

		finalV = arrowV + midV
		#retturn all the positions to apply to polevector control
		return([finalV.x , finalV.y ,finalV.z])		
	
	#Arm chain rig


	