abcList = cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, typ="transform")
abcList = [x for x in abcList if "_bone" in x]

geoList = cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, typ="transform")
geoList = [x for x in geoList if "_bone" in x]

for geo in geoList:
    for abc in abcList:
        if geo in abc:
            bs = cmds.blendShape(abc, geo, n=geo+"_bs", o="world")
            cmds.setAttr(bs[0]+"."+geo, 1)