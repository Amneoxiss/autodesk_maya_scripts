import maya.cmds as cmds

def customCylinder():
    cmds.polyCylinder(name="customCylinder",r=1, h=2, sx=8, sy=1, sz=1, cuv=3)
    s = cmds.ls(selection=True)

    cmds.select(clear=True)
    cmds.select('{0}.e[24]'.format(s[0]), '{0}.e[26]'.format(s[0]), '{0}.e[28]'.format(s[0]), '{0}.e[30]'.format(s[0]), '{0}.e[32]'.format(s[0]), '{0}.e[34]'.format(s[0]), '{0}.e[36]'.format(s[0]), '{0}.e[38]'.format(s[0]))
    cmds.polyDelEdge(cv=True)
    cmds.setAttr('{0}.translateY'.format(s[0]), 1)
    cmds.makeIdentity(s, apply=True, t=1, r=1, s=1, n=2 )
    cmds.delete(s, constructionHistory=True)
    
if __name__ == "__main__":
    customCylinder()
