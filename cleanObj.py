import maya.cmds as cmds
import sys
import os
import shutil

def clean():

	mods = cmds.ls(selection=True)
	shapes=[]

	#check for selection
	if not mods:
		cmds.confirmDialog(title="Clean", message="Please select something", button=['Ok'], defaultButton="Ok")
		sys.exit()

	#clean selection to only get mesh
	for m in mods:
		shape = cmds.listRelatives(m, shapes=True)
		
		if not shape:
			pass

		else:
			shapes.append(m)

	mods = shapes

	#check for selection  after clean
	if not mods:
		cmds.confirmDialog(title="Clean", message="Please select something", button=['Ok'], defaultButton="Ok")
		sys.exit()
	

	
	#check for modPath and get parent node
	modsPath = cmds.listRelatives(mods, fullPath=True, shapes=True)
	parent=[]

	for modPath in modsPath:
		modPath = modPath.split("|")
		modPath = modPath[-3]
		parent.append(modPath)


	#get file path and create directory
	path = cmds.file(query=True, sceneName=True)
	directory, filename = os.path.split(path)
	directory = os.path.join(directory, "_obj")
	
	#create Directory	
	if os.path.exists(directory):
		pass
	else:
		os.makedirs(directory)

	#export import obj
	for mod in mods:

		#get index for parent
		i = mods.index(mod)
		print(i)
		toParent=parent[i]
		print(toParent)

		#export selected mesh to obj
		name = mod+".obj"
		path = os.path.join(directory, name).replace("\\", "/")
		cmds.select(mod)		
		cmds.file(path, typ="OBJexport",es=1, op="groups=0;ptgroups=0;materials=0;smoothing=0;normals=0")

		#delete old mesh
		cmds.delete(mod)

		#create unique namespace and import obj back
		nspace = mod+"_01"
		cmds.file(path, i=1, namespace=nspace)

		#rename mesh and delete created namespace
		cmds.select("{0}:Mesh".format(nspace))		
		cmds.rename(mod)
		cmds.namespace(removeNamespace=nspace)
		
		#reparent geo
		if not toParent:
			cmds.select(mod)
			cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
			cmds.xform(mod, centerPivots = True)
			cmds.select(clear=True)

		else:
			cmds.parent(mod, toParent)
			cmds.select(mod)
			cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
			cmds.xform(mod, centerPivots = True)
			cmds.select(clear=True)

	#delete obj folder
	shutil.rmtree(directory)
	
	#end
	cmds.confirmDialog(title="Clean", message="Clean Done", button=['Ok'], defaultButton="Ok")

if __name__ == "__main__":
	clean()	