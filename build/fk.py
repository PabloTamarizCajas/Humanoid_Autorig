import maya.cmds as mc 

from Humanoid_Autorig.build import autorig_names as namejnts
reload(namejnts)

from Humanoid_Autorig.build import utils as utils
reload(utils)

def createFK(type,listJnts):
    
    if listJnts[0].startswith('L_'):
        parentFkGrp = mc.group(n='FK_' + type + '_L_grp',em=True)

    elif listJnts[0].startswith('R_'):
        parentFkGrp = mc.group(n='FK_' + type + '_R_grp',em=True)
    
    elif listJnts[0].startswith('C_'):
        parentFkGrp = mc.group(n='FK_' + type + '_C_grp',em=True)

    joints_fk = []
    joints_fk = createChain(listJnts,'_FK')
    ctl_fk = []
    
    #create controls
    for joint in joints_fk:
        name = joint.replace('_JNT','_ctl')
        ctl = mc.circle(n=name, nr=(1,0,0), c=(0,0,0), r=1)[0]
        ctl_fk.append(ctl)
        #position control
        jntPos = mc.xform(joint, q=True, ws=True, t=True)
        #rotate control
        jntRot = mc.xform(joint, q=True, ws=True, ro=True)
        #rotate control 90 degrees
        jntRot = [jntRot[0],jntRot[1],jntRot[2]+90]
        mc.xform(ctl, ws=True, t=jntPos,ro=jntRot)
        grp = utils.add_transforms([ctl])
        
        #parent control to group
        if joint == joints_fk[0]:
            mc.parent(grp[0],parentFkGrp)
        #parent control to previous control
        else :
            mc.parent(grp[0],ctl_fk[joints_fk.index(joint)-1])
            
    mc.parent(joints_fk[0],parentFkGrp)
            
    for joint in joints_fk:
        mc.parentConstraint(ctl_fk[joints_fk.index(joint)],joint,mo=True)
        
    mc.select(cl=True)
    
    return joints_fk, ctl_fk

def createChain(jointList,suffix):
    listChain = []
    count = 0
    for joint in jointList:
        mc.select(cl=True)
        mc.select(joint)
        jntPos = mc.xform(q=True, ws=True, t=True)
        name = joint.replace('_JNT',suffix)
        jointName = mc.joint(n=name+'_JNT', p=jntPos, rad=0.4)
        listChain.append(jointName)
        #unparent the first joint
        if count == 0:
            mc.parent(listChain[count],w=True)
        
        elif count > 0:
            mc.parent(listChain[count],listChain[count-1])
            
        if count == len(jointList)-1:
            mc.select(cl=True)
            mc.select(listChain[-1])
            mc.joint(e=True, oj='none', ch=True, zso=True)
        
        count += 1
        
    return listChain
    
