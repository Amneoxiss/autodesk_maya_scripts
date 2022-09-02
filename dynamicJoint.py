import maya.cmds as cmds
import maya.mel as mel

def dynamic():
	
	locs = cmds.ls(selection=True)
	joints=[]
	curveP=[]

	for loc in locs:
		i = locs.index(loc)
		i += 1
		i = str(i)
		i = i.rjust(4, '0')
		cmds.select(loc, replace=True)
		cmds.joint()
		cmds.rename("base_ik_{0}_jnt".format(i))
		j = cmds.ls(selection=True)
		cmds.parent(j, world=True)
		joints.append(j[0])

	n = 0

	for joint in joints:
		n += 1
		i = joints.index(joint)
		p = i-1

		if p < 0:
			baseJoint = joint
			print("World joint :", joint)
		else:
			print(joint)
			cmds.parent(joint, joints[p])

	#orient joint
	cmds.joint(joints[0], edit=True, oj='xyz', sao='yup', children=True, zso=True)

	#orient last joint
	cmds.joint(edit=True, oj='none', zso=True)
	cmds.select(baseJoint)

	#get joint position
	for joint in joints:
		
		cmds.select(joint, replace=True)

		trs = cmds.xform(query=True, translation=True, ws=True)
		trs = tuple(trs)

		curveP.append(trs)

	#create curve
	cmds.curve(p=curveP)
	cmds.rename('base_crv')
	
	#duplicate curve
	cmds.duplicate()
	cmds.rename('baseDynamic_crv')
	
	#create IK handle	
	cmds.ikHandle(sj=joints[0], ee=joints[-1], curve='base_crv', sol='ikSplineSolver', roc=False, pcv=False, scv=False, ccv=False, cra=False)

	#create cluster
	for joint in joints:
		i = joints.index(joint)
		cmds.select('baseDynamic_crv.cv[{0}]'.format(i), replace=True)
		i += 1
		i = str(i)
		i = i.rjust(4, '0')
		cmds.cluster()
		cmds.rename('base_{0}_ctr'.format(i))
		cmds.setAttr("base_{0}_ctr.visibility".format(i), 0)

		#create controler
		cmds.circle(nr=(0, 0, 1), c=(0, 0, 0))
		ctrl = cmds.rename('base_{0}_ctrl'.format(i))
		cmds.delete(constructionHistory=True)

		#create group control
		cmds.group(ctrl, n="base_{0}_off".format(i))

		#parent group to joint
		cmds.parentConstraint("base_ik_{0}_jnt".format(i), "base_{0}_off".format(i), n="toDeleteConstraint_{0}".format(i), mo=False)
		cmds.select("toDeleteConstraint_{0}".format(i), replace=True)
		cmds.delete()

		#rotateCtrl
		cmds.select("base_{0}_ctrl.cv[0:7]".format(i))
		cmds.rotate(0, '90deg', 0)
		cmds.select(clear=True)

		#parent cluster to control
		cmds.parent('base_{0}_ctr'.format(i), 'base_{0}_ctrl'.format(i))

		#parent controler
		p = joints.index(joint)
		p -= 1
		if p < 0:
			pass
		else:
			p = int(i)
			p -= 1
			p = str(p)
			p = p.rjust(4, '0')
			cmds.parent("base_{0}_off".format(i), 'base_{0}_ctrl'.format(p))

	'''
	#create dynamic
	cmds.select('baseDynamic_crv', replace=True)
	mel.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"}')

	#clean dynamic creation
	cmds.select("curve1")
	cmds.rename("outDynamic_crv")
	cmds.parent("outDynamic_crv", world=True)
	cmds.parent("baseDynamic_crv", world=True)
	cmds.parent("follicle1", world=True)
	cmds.select("hairSystem1OutputCurves", "hairSystem1Follicles",replace=True)
	cmds.delete()

	#change follicle lock to start
	cmds.setAttr("follicleShape1.pointLock", 1)

	#change hairSystem attraction curve
	cmds.setAttr("hairSystemShape1.startCurveAttract", 0.25)

	#create blendShape
	cmds.select("outDynamic_crv", "base_crv", replace=True)
	cmds.blendShape(name="curveBS_01", w=[(0, 1)])
	'''
	
if __name__ == '__main__':
    dynamic()