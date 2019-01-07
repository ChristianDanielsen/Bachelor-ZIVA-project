import maya.mel as mm
import maya.cmds as mc
import maya.OpenMaya as om

def createClustersOnCurve(sel=[]):
    if not sel:
        cmds.error("You didn't supply a curve")
    
    clList = []
    for i in sel:
        shape = cmds.listRelatives(i, shapes=True)
        if shape:
            if cmds.objectType(shape[0]) == "nurbsCurve":
                clA = cmds.cluster("{0}.{1}".format(i, "cv[0]"), n=i+"A_cls")
                clB = cmds.cluster("{0}.{1}".format(i, "cv[1]"), n=i+"B_cls")
                
                clList= clList + [clA[1], clB[1]]
    return clList
            

def get_mdagpath_from_object_name( object_name ):
    '''
    Returns the corresponding MDagPath object based on the objectName as a string. 
    
    Accepts:
      objectName - string
      
    Returns: 
      MDagPath object
      
    '''
    selList = om.MSelectionList()
    selList.add( object_name )  
    
    dagPath = om.MDagPath()
    it = om.MItSelectionList( selList )
    it.getDagPath(dagPath)
    
    return dagPath

def auto_rivet_transforms_to_meshes( everything_list ): 
    '''
    TO DO: This script assumes you have rivet.mel in your scripts directory
    '''
    '''      
    Description: 
    Given a list containing transforms and meshes, find the closest point on mesh from all 
    given meshes (so the closest of all closest points) And build a rivet on that mesh at 
    that point. Parent the transform under the rivet locator. 
        
    Accepts: 
     A list of tauto_rivet_transforms_to_meshesransforms and meshes. 
     
    Returns: None
        
    '''
    
    lookupMeshes_dict = dict()
    transforms_list = list()
    
    for item in everything_list: 
        shapes = mc.listRelatives( item, shapes=True )
        if shapes != None: 
            if mc.objectType( shapes[0] ) == 'mesh': 
                mesh_mfnMesh = om.MFnMesh( get_mdagpath_from_object_name( shapes[0] ) )
                lookupMeshes_dict[item] = mesh_mfnMesh
    
            else: 
                transforms_list.append(item)
    
    for transform in transforms_list: 
        closestDistance = 10e10
        closestMesh = None
        closestPolygon = None
    
    p = mc.xform( transform, q=True, rp=True, ws=True, a=True )
    lookup_mPoint = om.MPoint( p[0], p[1], p[2] )
    lookup_mFloatPoint = om.MFloatPoint( lookup_mPoint.x, lookup_mPoint.y, lookup_mPoint.z )
    
    closestPolygon_mScriptUtil = om.MScriptUtil()
    
    for lookupMesh in lookupMeshes_dict.keys(): 
        currMesh_mfnMesh = lookupMeshes_dict[ lookupMesh ]
          
        closest_mPoint = om.MPoint()
        closest_mScriptUtil = om.MScriptUtil()
        closestPolygon_ptr = closest_mScriptUtil.asIntPtr()
        
        currMesh_mfnMesh.getClosestPoint( lookup_mPoint, closest_mPoint, om.MSpace.kWorld, closestPolygon_ptr )
        
        closestPolygon_currIndex = closest_mScriptUtil.getInt(closestPolygon_ptr)
        
        closest_mFloatPoint = om.MFloatPoint( closest_mPoint.x, closest_mPoint.y, closest_mPoint.z )
    
        d = closest_mFloatPoint.distanceTo( lookup_mFloatPoint )
        if d < closestDistance: 
            closestDistance = d
            closestMesh = lookupMesh
            closestPolygon = closestPolygon_currIndex
    
    prevIndex_util = om.MScriptUtil()
    
    meshName_mItMeshPolygon = om.MItMeshPolygon( get_mdagpath_from_object_name( closestMesh ) )
    meshName_mItMeshPolygon.setIndex( closestPolygon, prevIndex_util.asIntPtr() )
    
    edges_mIntArray = om.MIntArray()
    meshName_mItMeshPolygon.getEdges( edges_mIntArray )
    
    mc.select( closestMesh+'.e[%i]' % edges_mIntArray[0], r=True )
    mc.select( closestMesh+'.e[%i]' % edges_mIntArray[2], add=True )
    
    rivetLocator_str = mm.eval('rivet;')
    
    rivetLocator_str = mc.rename( rivetLocator_str, transform+'_rivet' )
    mc.select(rivetLocator_str)
    
    renameRivetObject(transform,rivetLocator_str,closestMesh) 
    mc.parent( transform, rivetLocator_str ) 

    
def renameRivetObject(transform="",rivetLocator_str="",closestMesh=""):
    mc.select(hi = True)
    hiSel = mc.ls(sl=True)
    print hiSel
    for obj in hiSel:
        if mc.objExists(obj):
            if not transform in obj:
                    if not closestMesh in obj:
                        newName = mc.rename(obj,transform + obj)
                        obj = newName
            renameRivetConnections(obj,transform,closestMesh)


def renameRivetConnections(obj="", transform="",closestMesh=""):
    connections = mc.listConnections(obj,scn=True,s=True,d=False,sh=False)

    try:
        len(connections)
        for con in connections :
            if mc.objExists(con):
                if not transform in con:
                    if not closestMesh in con:
                        renameRivetConnections(con, transform,closestMesh)
                        newConName = mc.rename(con,transform + con)
                
    except :
        print ""

def attachLOA(sel=[]):
    if not sel:
        cmds.error("Nothing was specified!")
    curveList = []
    boneList = []
    for i in sel:
        shape = cmds.listRelatives(i, shapes=True)
        if shape:
            if cmds.objectType(shape[0]) == "nurbsCurve":
                print shape[0]
                curveList = curveList + [i]
            elif cmds.objectType(shape[0]) == "mesh":
                boneList = boneList + [i]
    
    for i in curveList:
        cls = createClustersOnCurve([i])

        auto_rivet_transforms_to_meshes([cls[0]] + boneList)
        auto_rivet_transforms_to_meshes([cls[1]] + boneList)
        
"""
How to:
    Run everything once, select all the bones and curves you want to attach, then run the example code below
EXAMPLE:
attachLOA(cmds.ls(sl=True))
"""
 