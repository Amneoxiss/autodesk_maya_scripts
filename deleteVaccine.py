"""
DELETE VACCINE
"""

import maya.cmds as cmds
import os

jobs = cmds.scriptJob(lj=True)
for job in jobs:
    if "leukocyte.antivirus()" in job:
        id = job.split(":")[0]
        if id.isdigit():
            cmds.scriptJob(k=int(id), f=True)

node = cmds.ls("vaccine_gene", "breed_gene", type="script")
print(node)

for n in node:
    a = n
    if not a:
        pass
    else:
        cmds.delete(a)

#get user name
user = os.getenv('username')
path = "C:/Users/{}/Documents/maya/scripts".format(user)

files = os.listdir(path)

if not files:
    pass

else:
    if "userSetup.py" in files:
        os.remove(os.path.join(path, "userSetup.py"))

    else:
        pass  

    if "vaccine.py" in files:
        os.remove(os.path.join(path, "vaccine.py"))

    else:
        pass  
        
    if "vaccine.pyc" in files:
        os.remove(os.path.join(path, "vaccine.pyc"))

    else:
        pass

cmds.confirmDialog(title="Publish", message="DONE", button=['Ok'], defaultButton="Ok")