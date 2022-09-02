import maya.cmds as cmds




#### WINDOW ####

myWindow = cmds.window( title="UI", widthHeight=(200, 150), sizeable=True )
cmds.columnLayout( adjustableColumn=True, rowSpacing=5 )

cmds.text( label= "Shader Template", font="boldLabelFont", height=25)
cmds.text( label= "Select your mesh or group first,", align="center" )
cmds.text( label= "then click on your desired renderer", align="center" )

cmds.setParent( '..' )


mainLayout = cmds.columnLayout(w = 500, h = 35)

cmds.separator()

newName = cmds.textFieldGrp( label = "Shader Name:", editable = True, parent=mainLayout )

cmds.setParent( '..' )


cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, adjustableColumn=True )



### RENAME ###




#### RENDERMAN ###

def rendermanAssign():

	mySelectionList = cmds.ls(sl=True)

	shaderName = cmds.textFieldGrp( newName, q=True, text=True)	

	# creer un shader
	myShader = cmds.shadingNode('PxrSurface', asShader=True, name=shaderName+"_Mtl" )


	# creer un shading group
	myShaderSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=myShader+"SG")

	# shader to shading group

	cmds.connectAttr('%s.outColor' % myShader, '%s.surfaceShader' % myShaderSG)

	# connect the nodes

	"""ALBEDO NODES"""

	remap = cmds.shadingNode('PxrRemap', name= 'remap_albedo_'+shaderName, asTexture=True)
	hsl = cmds.shadingNode('PxrHSL', name= 'HSL_albedo_'+shaderName, asTexture=True)
	cc = cmds.shadingNode('PxrColorCorrect', name= 'color_correct_albedo_'+shaderName, asTexture=True)
	pxrtexture = cmds.shadingNode('PxrTexture', name='albedo_'+shaderName, asTexture=True)

	"""SPECULAR NODES"""

	remap_spec = cmds.shadingNode('PxrRemap', name= 'remap_specular_'+shaderName, asTexture=True)
	hsl_spec = cmds.shadingNode('PxrHSL', name= 'HSL_specular_'+shaderName, asTexture=True)
	cc_spec = cmds.shadingNode('PxrColorCorrect', name= 'color_correct_specular_'+shaderName, asTexture=True)
	pxrtexture_spec = cmds.shadingNode('PxrTexture', name= 'specular_'+shaderName, asTexture=True)

	"""ROUGHNESS NODES"""

	remap_roughness = cmds.shadingNode('PxrRemap', name= 'remap_roughess_'+shaderName, asTexture=True)
	hsl_roughness = cmds.shadingNode('PxrHSL', name= 'HSL_roughness_'+shaderName, asTexture=True)
	cc_roughness = cmds.shadingNode('PxrColorCorrect', name= 'color_correct_roughness_'+shaderName, asTexture=True)
	pxrtexture_roughness = cmds.shadingNode('PxrTexture', name= 'roughness_'+shaderName, asTexture=True)

	"""BUMP AND NORMAL MAP NODES"""

	remap_bump_normal = cmds.shadingNode('PxrRemap', name= 'remap_bump_normal_'+shaderName, asTexture=True)
	pxrtexture_bump = cmds.shadingNode('PxrTexture', name= 'bump_normal_'+shaderName, asTexture=True)
	bump = cmds.shadingNode('PxrBump', name= 'bump_'+shaderName, asTexture=True)

	"""DISPLACEMENT NODES"""

	displace = cmds.shadingNode('PxrDisplace', name= 'disp_'+shaderName, asShader=True)
	dispTransform = cmds.shadingNode('PxrDispTransform', name= 'dispTransform_'+shaderName, asTexture=True)
	pxrtexture_disp = cmds.shadingNode('PxrTexture', name= 'displacement_'+shaderName, asTexture=True)



	"""ALBEDO"""

	cmds.connectAttr('%s.resultRGB' % remap, '%s.diffuseColor' % myShader)
	cmds.connectAttr('%s.resultRGB' % hsl, '%s.inputRGB' % remap)
	cmds.connectAttr('%s.resultRGB' % cc, '%s.inputRGB' % hsl)
	cmds.connectAttr('%s.resultRGB' % pxrtexture, '%s.inputRGB' % cc)

	"""SPECULAR"""

	cmds.connectAttr('%s.resultRGB' % remap_spec, '%s.specularFaceColor' % myShader)
	cmds.connectAttr('%s.resultRGB' % hsl_spec, '%s.inputRGB' % remap_spec)
	cmds.connectAttr('%s.resultRGB' % cc_spec, '%s.inputRGB' % hsl_spec)
	cmds.connectAttr('%s.resultRGB' % pxrtexture_spec, '%s.inputRGB' % cc_spec)

	"""ROUGHNESS"""

	cmds.connectAttr('%s.resultR' % remap_roughness, '%s.specularRoughness' % myShader)
	cmds.connectAttr('%s.resultRGB' % hsl_roughness, '%s.inputRGB' % remap_roughness)
	cmds.connectAttr('%s.resultRGB' % cc_roughness, '%s.inputRGB' % hsl_roughness)
	cmds.connectAttr('%s.resultRGB' % pxrtexture_roughness, '%s.inputRGB' % cc_roughness)

	"""BUMP NORMAL"""

	cmds.connectAttr('%s.resultRGB' % pxrtexture_bump, '%s.inputRGB' % remap_bump_normal)
	cmds.connectAttr('%s.resultR' % remap_bump_normal, '%s.inputBump' % bump)
	cmds.connectAttr('%s.resultN' % bump, '%s.bumpNormal' % myShader)

	"""DISPLACEMENT"""

	cmds.connectAttr('%s.resultR' % pxrtexture_disp, '%s.dispScalar' % dispTransform)
	cmds.connectAttr('%s.resultF' % dispTransform, '%s.dispScalar' % displace)
	cmds.connectAttr('%s.outColor' % displace, '%s.displacementShader' % myShaderSG)

	#PxrTexture attributes

	cmds.setAttr( pxrtexture+".atlasStyle", 1 )
	cmds.setAttr( pxrtexture+".linearize", 1 )

	#Specular attributes

	cmds.setAttr( pxrtexture_spec+".atlasStyle", 1 )

	#Roughness attributes 

	cmds.setAttr( pxrtexture_roughness+".atlasStyle", 1 )

	#Bump and normal attributes

	cmds.setAttr( pxrtexture_bump+".atlasStyle", 1 )

	#Displacement attributes

	cmds.setAttr( pxrtexture_disp+".atlasStyle", 1 )
	cmds.setAttr( dispTransform+".dispRemapMode", 2 )



	# assign le shader a la selection
	for o in mySelectionList :
		cmds.sets(o, e=True, forceElement=myShaderSG)


	print('Renderman Shader assigned to object successfully')



### ARNOLD ###

def arnoldAssign():

	mySelectionList = cmds.ls(sl=True)

	shaderName = cmds.textFieldGrp( newName, q=True, text=True)

	# create shader

	myShader = cmds.shadingNode('aiStandardSurface', asShader=True, name=shaderName+"_Mtl" )

	# create a shading group

	myShaderSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=myShader+"SG")

	# assign shader to shading group

	cmds.connectAttr('%s.outColor' % myShader, '%s.surfaceShader' % myShaderSG)

	# assign shader to selection
	for o in mySelectionList :
		cmds.sets(o, e=True, forceElement=myShaderSG)

	# connect nodes ALBEDO
	
	myFile_Albedo = cmds.shadingNode("file", asTexture=True, name='albedo_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Albedo_'+myShader)
	rangeAlbedo = cmds.shadingNode("aiRange", asTexture=True, name='Range_Albedo_'+myShader)
	colorCorrectAlbedo = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Albedo_'+myShader)

	cmds.connectAttr(myUVFile + ".coverage", myFile_Albedo +".coverage", force=True)
	cmds.connectAttr(myUVFile + ".translateFrame", myFile_Albedo +".translateFrame", force=True)
	cmds.connectAttr(myUVFile +".rotateFrame", myFile_Albedo +".rotateFrame", force=True)
	cmds.connectAttr(myUVFile +".mirrorU", myFile_Albedo +".mirrorU", force=True)
	cmds.connectAttr(myUVFile +".mirrorV", myFile_Albedo +".mirrorV", force=True)
	cmds.connectAttr(myUVFile +".stagger", myFile_Albedo +".stagger", force=True)
	cmds.connectAttr(myUVFile +".wrapU", myFile_Albedo +".wrapU", force=True)
	cmds.connectAttr(myUVFile +".wrapV", myFile_Albedo +".wrapV", force=True)
	cmds.connectAttr(myUVFile +".repeatUV", myFile_Albedo +".repeatUV", force=True)
	cmds.connectAttr(myUVFile +".offset", myFile_Albedo +".offset", force=True)
	cmds.connectAttr(myUVFile +".rotateUV", myFile_Albedo +".rotateUV", force=True)
	cmds.connectAttr(myUVFile +".noiseUV", myFile_Albedo +".noiseUV", force=True)
	cmds.connectAttr(myUVFile +".vertexUvOne", myFile_Albedo +".vertexUvOne", force=True)
	cmds.connectAttr(myUVFile +".vertexUvTwo", myFile_Albedo +".vertexUvTwo", force=True)
	cmds.connectAttr(myUVFile +".vertexUvThree", myFile_Albedo +".vertexUvThree", force=True)
	cmds.connectAttr(myUVFile +".vertexCameraOne", myFile_Albedo +".vertexCameraOne", force=True)
	cmds.connectAttr(myUVFile +".outUV", myFile_Albedo +".uvCoord", force=True)


	cmds.connectAttr(myFile_Albedo +".outColor", colorCorrectAlbedo + ".input", force=True)
	cmds.connectAttr(colorCorrectAlbedo +".outColor", rangeAlbedo +".input", force=True)
	cmds.connectAttr(rangeAlbedo + ".outColor", myShader + ".baseColor", force=True)

	# attributes 

	cmds.setAttr(myFile_Albedo+".uvTilingMode", 3)
	cmds.setAttr(myFile_Albedo+".colorSpace", "sRGB", type='string' )

	# connect nodes METALNESS

	myFile_Metalness = cmds.shadingNode("file", asTexture=True, name='metalness_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Metalness_'+myShader)
	rangeMetalness = cmds.shadingNode("aiRange", asTexture=True, name='Range_Metalness_'+myShader)
	colorCorrectMetalness = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Metalness_'+myShader)
	
	cmds.connectAttr(myUVFile + ".coverage",myFile_Metalness +".coverage",force = True)
	cmds.connectAttr(myUVFile + ".translateFrame",myFile_Metalness +".translateFrame",force = True)
	cmds.connectAttr(myUVFile + ".rotateFrame",myFile_Metalness +".rotateFrame",force = True)
	cmds.connectAttr(myUVFile + ".mirrorU",myFile_Metalness +".mirrorU",force = True)
	cmds.connectAttr(myUVFile + ".mirrorV",myFile_Metalness +".mirrorV",force = True)
	cmds.connectAttr(myUVFile + ".stagger",myFile_Metalness +".stagger",force = True)
	cmds.connectAttr(myUVFile + ".wrapU",myFile_Metalness +".wrapU",force = True)
	cmds.connectAttr(myUVFile + ".wrapV",myFile_Metalness +".wrapV",force = True)
	cmds.connectAttr(myUVFile + ".repeatUV",myFile_Metalness +".repeatUV",force = True)
	cmds.connectAttr(myUVFile + ".offset",myFile_Metalness +".offset",force = True)
	cmds.connectAttr(myUVFile + ".rotateUV",myFile_Metalness +".rotateUV",force = True)
	cmds.connectAttr(myUVFile + ".noiseUV",myFile_Metalness +".noiseUV",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvOne",myFile_Metalness +".vertexUvOne",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvTwo",myFile_Metalness +".vertexUvTwo",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvThree",myFile_Metalness +".vertexUvThree",force = True)
	cmds.connectAttr(myUVFile + ".vertexCameraOne",myFile_Metalness +".vertexCameraOne",force = True)
	cmds.connectAttr(myUVFile + ".outUV",myFile_Metalness +".uvCoord",force = True)


	cmds.connectAttr(myFile_Metalness +".outColor", colorCorrectMetalness +".input", force=True)
	cmds.connectAttr(colorCorrectMetalness +".outColor", rangeMetalness +".input", force=True)
	cmds.connectAttr(rangeMetalness + ".outColorR", myShader + ".metalness",force = True)

	# attributes

	cmds.setAttr(myFile_Metalness+".uvTilingMode", 3)
	cmds.setAttr(myFile_Metalness+".colorSpace", "Raw", type='string')

	# connect nodes SPECULAR

	myFile_SpecularWeight = cmds.shadingNode("file", asTexture=True, name='specular_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Specular_'+myShader)
	rangeSpecular = cmds.shadingNode("aiRange", asTexture=True, name='Range_Specular_'+myShader)
	colorCorrectSpecular = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Specular_'+myShader)

	cmds.connectAttr(myUVFile + ".coverage",myFile_SpecularWeight +".coverage",force = True)
	cmds.connectAttr(myUVFile + ".translateFrame",myFile_SpecularWeight +".translateFrame",force = True)
	cmds.connectAttr(myUVFile + ".rotateFrame",myFile_SpecularWeight +".rotateFrame",force = True)
	cmds.connectAttr(myUVFile + ".mirrorU",myFile_SpecularWeight +".mirrorU",force = True)
	cmds.connectAttr(myUVFile + ".mirrorV",myFile_SpecularWeight +".mirrorV",force = True)
	cmds.connectAttr(myUVFile + ".stagger",myFile_SpecularWeight +".stagger",force = True)
	cmds.connectAttr(myUVFile + ".wrapU",myFile_SpecularWeight +".wrapU",force = True)
	cmds.connectAttr(myUVFile + ".wrapV",myFile_SpecularWeight +".wrapV",force = True)
	cmds.connectAttr(myUVFile + ".repeatUV",myFile_SpecularWeight +".repeatUV",force = True)
	cmds.connectAttr(myUVFile + ".offset",myFile_SpecularWeight +".offset",force = True)
	cmds.connectAttr(myUVFile + ".rotateUV",myFile_SpecularWeight +".rotateUV",force = True)
	cmds.connectAttr(myUVFile + ".noiseUV",myFile_SpecularWeight +".noiseUV",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvOne",myFile_SpecularWeight +".vertexUvOne",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvTwo",myFile_SpecularWeight +".vertexUvTwo",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvThree",myFile_SpecularWeight +".vertexUvThree",force = True)
	cmds.connectAttr(myUVFile + ".vertexCameraOne",myFile_SpecularWeight +".vertexCameraOne",force = True)
	cmds.connectAttr(myUVFile + ".outUV",myFile_SpecularWeight +".uvCoord",force = True)


	cmds.connectAttr(myFile_SpecularWeight + ".outColor", colorCorrectSpecular + ".input", force=True)
	cmds.connectAttr(colorCorrectSpecular + ".outColor", rangeSpecular + ".input", force=True)
	cmds.connectAttr(rangeSpecular + ".outColorR", myShader + ".specular",force = True)

	# attributes

	cmds.setAttr(myFile_SpecularWeight+".uvTilingMode", 3)
	cmds.setAttr(myFile_SpecularWeight+".colorSpace", "Raw", type='string')


	# connect nodes ROUGHNESS

	myFile_Roughness = cmds.shadingNode("file", asTexture=True, name='roughness_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Roughness_'+myShader)
	rangeRoughness = cmds.shadingNode("aiRange", asTexture=True, name='Range_Roughness_'+myShader)
	colorCorrectRoughness = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Roughness_'+myShader)

	cmds.connectAttr(myUVFile + ".coverage",myFile_Roughness +".coverage",force = True)
	cmds.connectAttr(myUVFile + ".translateFrame",myFile_Roughness +".translateFrame",force = True)
	cmds.connectAttr(myUVFile + ".rotateFrame",myFile_Roughness +".rotateFrame",force = True)
	cmds.connectAttr(myUVFile + ".mirrorU",myFile_Roughness +".mirrorU",force = True)
	cmds.connectAttr(myUVFile + ".mirrorV",myFile_Roughness +".mirrorV",force = True)
	cmds.connectAttr(myUVFile + ".stagger",myFile_Roughness +".stagger",force = True)
	cmds.connectAttr(myUVFile + ".wrapU",myFile_Roughness +".wrapU",force = True)
	cmds.connectAttr(myUVFile + ".wrapV",myFile_Roughness +".wrapV",force = True)
	cmds.connectAttr(myUVFile + ".repeatUV",myFile_Roughness +".repeatUV",force = True)
	cmds.connectAttr(myUVFile + ".offset",myFile_Roughness +".offset",force = True)
	cmds.connectAttr(myUVFile + ".rotateUV",myFile_Roughness +".rotateUV",force = True)
	cmds.connectAttr(myUVFile + ".noiseUV",myFile_Roughness +".noiseUV",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvOne",myFile_Roughness +".vertexUvOne",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvTwo",myFile_Roughness +".vertexUvTwo",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvThree",myFile_Roughness +".vertexUvThree",force = True)
	cmds.connectAttr(myUVFile + ".vertexCameraOne",myFile_Roughness +".vertexCameraOne",force = True)
	cmds.connectAttr(myUVFile + ".outUV",myFile_Roughness +".uvCoord",force = True)


	cmds.connectAttr(myFile_Roughness + ".outColor", colorCorrectRoughness + ".input", force=True)
	cmds.connectAttr(colorCorrectRoughness + ".outColor", rangeRoughness + ".input", force=True)
	cmds.connectAttr(rangeRoughness + ".outColorR", myShader + ".specularRoughness",force = True)

	# attributes

	cmds.setAttr(myFile_Roughness+".uvTilingMode", 3)
	cmds.setAttr(myFile_Roughness+".colorSpace", "Raw", type='string')


	# connect nodes BUMP


	myFile_Bump = cmds.shadingNode("file", asTexture=True, name='bump_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Bump_'+myShader)
	rangeBump = cmds.shadingNode("aiRange", asTexture=True, name='Range_Bump_'+myShader)
	colorCorrectBump = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Bump_'+myShader)
	bump = cmds.shadingNode("aiBump2d", asShader=True, name='BumpSettings_'+myShader)


	cmds.connectAttr(myUVFile + ".coverage",myFile_Bump +".coverage",force = True)
	cmds.connectAttr(myUVFile + ".translateFrame",myFile_Bump +".translateFrame",force = True)
	cmds.connectAttr(myUVFile + ".rotateFrame",myFile_Bump +".rotateFrame",force = True)
	cmds.connectAttr(myUVFile + ".mirrorU",myFile_Bump +".mirrorU",force = True)
	cmds.connectAttr(myUVFile + ".mirrorV",myFile_Bump +".mirrorV",force = True)
	cmds.connectAttr(myUVFile + ".stagger",myFile_Bump +".stagger",force = True)
	cmds.connectAttr(myUVFile + ".wrapU",myFile_Bump +".wrapU",force = True)
	cmds.connectAttr(myUVFile + ".wrapV",myFile_Bump +".wrapV",force = True)
	cmds.connectAttr(myUVFile + ".repeatUV",myFile_Bump +".repeatUV",force = True)
	cmds.connectAttr(myUVFile + ".offset",myFile_Bump +".offset",force = True)
	cmds.connectAttr(myUVFile + ".rotateUV",myFile_Bump +".rotateUV",force = True)
	cmds.connectAttr(myUVFile + ".noiseUV",myFile_Bump +".noiseUV",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvOne",myFile_Bump +".vertexUvOne",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvTwo",myFile_Bump +".vertexUvTwo",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvThree",myFile_Bump +".vertexUvThree",force = True)
	cmds.connectAttr(myUVFile + ".vertexCameraOne",myFile_Bump +".vertexCameraOne",force = True)
	cmds.connectAttr(myUVFile + ".outUV",myFile_Bump +".uvCoord",force = True)


	cmds.connectAttr(myFile_Bump + ".outColor", colorCorrectBump + ".input", force=True)
	cmds.connectAttr(colorCorrectBump + ".outColor", rangeBump + ".input", force=True)
	cmds.connectAttr(rangeBump + ".outColorR", bump + ".bumpMap",force = True)
	cmds.connectAttr(bump +".outValue", myShader +".normalCamera", force=True)

	# attributes

	cmds.setAttr(myFile_Bump+".uvTilingMode", 3)
	cmds.setAttr(myFile_Bump+".colorSpace", "Raw", type='string')


	# connect nodes DISPLACEMENT

	myFile_Displacement = cmds.shadingNode("file", asTexture=True, name='displacement_'+myShader)
	myUVFile = cmds.shadingNode("place2dTexture", asTexture=True, name='Tile_Displacement_'+myShader)
	rangeDisp = cmds.shadingNode("aiRange", asTexture=True, name='Range_Displacement_'+myShader)
	colorCorrectDisp = cmds.shadingNode("aiColorCorrect", asTexture=True, name='ColorCorrect_Displacement_'+myShader)
	displace = cmds.shadingNode("displacementShader", asShader=True, name='DisplacementSettings_'+myShader) 


	cmds.connectAttr(myUVFile + ".coverage",myFile_Displacement +".coverage",force = True)
	cmds.connectAttr(myUVFile + ".translateFrame",myFile_Displacement +".translateFrame",force = True)
	cmds.connectAttr(myUVFile + ".rotateFrame",myFile_Displacement +".rotateFrame",force = True)
	cmds.connectAttr(myUVFile + ".mirrorU",myFile_Displacement +".mirrorU",force = True)
	cmds.connectAttr(myUVFile + ".mirrorV",myFile_Displacement +".mirrorV",force = True)
	cmds.connectAttr(myUVFile + ".stagger",myFile_Displacement +".stagger",force = True)
	cmds.connectAttr(myUVFile + ".wrapU",myFile_Displacement +".wrapU",force = True)
	cmds.connectAttr(myUVFile + ".wrapV",myFile_Displacement +".wrapV",force = True)
	cmds.connectAttr(myUVFile + ".repeatUV",myFile_Displacement +".repeatUV",force = True)
	cmds.connectAttr(myUVFile + ".offset",myFile_Displacement +".offset",force = True)
	cmds.connectAttr(myUVFile + ".rotateUV",myFile_Displacement +".rotateUV",force = True)
	cmds.connectAttr(myUVFile + ".noiseUV",myFile_Displacement +".noiseUV",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvOne",myFile_Displacement +".vertexUvOne",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvTwo",myFile_Displacement +".vertexUvTwo",force = True)
	cmds.connectAttr(myUVFile + ".vertexUvThree",myFile_Displacement +".vertexUvThree",force = True)
	cmds.connectAttr(myUVFile + ".vertexCameraOne",myFile_Displacement +".vertexCameraOne",force = True)
	cmds.connectAttr(myUVFile + ".outUV",myFile_Displacement +".uvCoord",force = True)


	cmds.connectAttr(myFile_Displacement + ".outColor", colorCorrectDisp + ".input", force=True)
	cmds.connectAttr(colorCorrectDisp + ".outColor", rangeDisp + ".input", force=True)
	cmds.connectAttr(rangeDisp + ".outColorR", displace + ".displacement",force = True)
	cmds.connectAttr(displace +".displacement", myShaderSG +".displacementShader", force=True)

	# attributes

	cmds.setAttr(myFile_Displacement+".uvTilingMode", 3)
	cmds.setAttr(myFile_Displacement+".colorSpace", "Raw", type='string')

	print('Arnold Shader assigned to object successfully')

	




cmds.button( label="Arnold", c='arnoldAssign()' )
cmds.button( label="Renderman", c='rendermanAssign()' )




















cmds.showWindow(myWindow)

print('Happy Texturing!')
