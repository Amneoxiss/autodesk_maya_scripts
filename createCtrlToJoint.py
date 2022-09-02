import maya.cmds as cmds

def controlToJnt():
    join_selection = cmds.ls(sl=1,sn=True)
    joint_name = join_selection[0]

    cmds.select(clear=True)
    cmds.circle(n=joint_name+'_ctrl', nr=(0,1,0))
    cmds.group(n=joint_name+'_trsf')

    ctrlgrp_selection = cmds.ls(sl=1,sn=True)
    ctrlgrp_name = ctrlgrp_selection[0]

    cmds.parentConstraint(joint_name, ctrlgrp_name,n=('ContraintToDelete1') ,mo=False)
    cmds.select('ContraintToDelete1', replace=True)
    cmds.delete()

    cmds.select(ctrlgrp_name)
    ctrl_selection = cmds.listRelatives(c=True)
    ctrl_name = ctrl_selection[0]

    cmds.parentConstraint(ctrl_name, joint_name, n=joint_name+'parentConstraint01', mo=True)

if __name__ == "__main__":
    controlToJnt()