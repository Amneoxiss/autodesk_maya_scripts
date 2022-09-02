import maya.cmds as cmds
import random

def randomMesh():

    sel = cmds.ls(selection=True)
    sel2 = random.sample(sel, len(sel)/6)

    for s in sel2:
        sel.remove(s)
    
    sel3 = random.sample(sel, len(sel)/5)

    for s in sel3:
        sel.remove(s)

    sel4 =  random.sample(sel, len(sel)/4)
    
    for s in sel4:
        sel.remove(s)

    sel5 =  random.sample(sel, len(sel)/3)

    for s in sel5:
        sel.remove(s)

    sel6 =  random.sample(sel, len(sel)/2)

    for s in sel6:
        sel.remove(s)

    cmds.select(sel)
    cmds.polyUnite(sel)
    cmds.delete(constructionHistory = True)
    cmds.polyUnite(sel2)
    cmds.delete(constructionHistory = True)
    cmds.polyUnite(sel3)
    cmds.delete(constructionHistory = True)
    cmds.polyUnite(sel4)
    cmds.delete(constructionHistory = True)
    cmds.polyUnite(sel5)
    cmds.delete(constructionHistory = True)
    cmds.polyUnite(sel6)
    cmds.delete(constructionHistory = True)
        
if __name__ == "__main__":
    randomMesh()