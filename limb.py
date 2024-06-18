import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as namejnts
reload(names)

from Humanoid_Autorig.build import ik as ik
reload(ik)

from Humanoid_Autorig.build import fk as fk
reload(fk)

def createLimb():
    fkList = fk.createFK(type='arm', listJnts=namejnts.jointList()[1][1:])
    ikList = ik.createIk(type='arm', listJnts=namejnts.jointList()[1][1:])
    jointList = namejnts.jointList()[1][1:]
    switchIkFk(ikList[0],fkList[0],jointList)
    
def switchIkFk(ik,fk,jointList):
    armCtrl = mc.circle(n='arm_ctrl', nr=(1,0,0), c=(0,0,0), r=1)[0]
    #add attribute to control 0 to 1
    mc.addAttr(armCtrl,ln='ikFk',at='double',min=0,max=1,dv=0,k=True)

    for joint, ik_name, fk_name in zip(jointList, ik, fk):
        constraint = mc.parentConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_parentConstraint'))
        reverse = mc.shadingNode('reverse', asUtility=True, n=joint.replace('_JNT', '_reverse'))
        mc.connectAttr(armCtrl + '.ikFk', reverse + '.inputX')
        mc.connectAttr(armCtrl + '.ikFk', constraint[0] + '.' + ik_name + 'W0')
        mc.connectAttr(reverse + '.outputX', constraint[0] + '.' + fk_name + 'W1')
        mc.select(cl=True)
createLimb()