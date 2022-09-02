import maya.cmds as cmds

def shapesCurves():

    crvs = cmds.ls(selection=True)

    for crv in crvs:
        
        baseCrv = crv.split('|')[-1]
        baseCrv = baseCrv.split('_')
        baseCrv = baseCrv[1]
        shapes = cmds.listRelatives(crv, c=1, type="shape")
        i = 0
        finalCrvs = []

        for shape in shapes:
            i = int(i)
            i+=1
            i = str(i)
            i = i.rjust(4, '0')
            shape = cmds.rename(shape, 'barb_{0}_{1}_crvShape'.format(baseCrv, i))
            newTrans = cmds.group(em=True, name='barb_{0}_{1}_crv'.format(baseCrv, i))
            finalCrvs.append(newTrans)
            cmds.parent(shape, newTrans, r=1, s=1)
            print('done barb {0}'.format(i))
            
        cmds.parent(finalCrvs, crv)
        print('done feather {0}'.format(crv))

if __name__ == "__main__":
    shapesCurves()