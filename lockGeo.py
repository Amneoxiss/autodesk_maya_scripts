import maya.cmds as cmds

def lockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

def unlockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

def lockAll():

	cmds.select("*:*_geo", replace=True)
	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

	cmds.select(clear=True)

def unlockAll():

	cmds.select("*:*_geo", replace=True)
	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

	cmds.select(clear=True)

if __name__ == '__main__':
    lockAll()