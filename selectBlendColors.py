import maya.cmds as cmds

def selBC():
	bc = cmds.ls(type="blendColors")
	cmds.select(bc, replace=True)

if __name__ == "__main__":
	selBC()