import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as namejnts
reload(namejnts)

from Humanoid_Autorig.build import utils as utils

def createIk(type,listJnts):
     
    if listJnts[0].startswith('L_'):
        parentFkGrp = mc.group(n='IK_' + type + '_L_grp',em=True)

    elif listJnts[0].startswith('R_'):
        parentFkGrp = mc.group(n='IK_' + type + '_R_grp',em=True)
    
    elif listJnts[0].startswith('C_'):
        parentFkGrp = mc.group(n='IK_' + type + '_C_grp',em=True)

    joints_ik = []
    joints_ik = createChain(listJnts,'_IK')
    ctl_ik = []
    
    ctl = createCtl(joints_ik)
    grp = utils.add_transforms([ctl])
    
    nameIkh = joints_ik[-1].replace('_JNT','_ikh')
    mc.ikHandle(sj=joints_ik[0],ee=joints_ik[-1],sol='ikRPsolver',n=nameIkh)
    
    pv = mc.circle(n=ctl.replace('_ctl','_pv'), nr=(1,0,0), c=(0,0,0), r=1)[0]
    create_pole_vector(pv, nameIkh,dist=5)
    mc.parent(nameIkh,ctl)
    mc.parent(grp[0],parentFkGrp)
    
    ctl_ik.append(ctl)
    ctl_ik.append(pv)
    
    return joints_ik, ctl_ik
    
    

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

def createCtl(name):
    nameCtl = name[-1].replace('_JNT','_ctl')
    #create ik handles
    mc.circle(n=nameCtl, nr=(1,0,0), c=(0,0,0), r=1)
    jntPos = mc.xform(name[-1], q=True, ws=True, t=True)
    jntRot = mc.xform(name[-1], q=True, ws=True, ro=True)
    jntRot = [jntRot[0],jntRot[1],jntRot[2]+90]
    mc.xform(nameCtl, ws=True, t=jntPos,ro=jntRot)
    
    return nameCtl

def create_pole_vector(pv_ctl, ik_handle, dist = 1):

    # Find the start joint from querying ik handle
    start_joint = mc.ikHandle(ik_handle, q=True, startJoint=True)
    mid_joint = mc.listRelatives(start_joint, children=True, type='joint')

    # Constrain the pole vector control transform between start joint and ik_handle
    mc.delete(mc.pointConstraint(start_joint, ik_handle, pv_ctl))

    # Aim pole vector control to mid_joint - Aim X-axis
    mc.delete(mc.aimConstraint(mid_joint[0], pv_ctl, aim=[1, 0, 0], u=[0, 0, 1], wut='none'))

    # Find distance from pole vector control to mid_joint
    pv_pos = mc.xform(pv_ctl, q=True, ws=True, t=True)
    mid_pos = mc.xform(mid_joint[0], q=True, ws=True, t=True)
    pv_dist = (pv_pos[0] - mid_pos[0], pv_pos[1] - mid_pos[1], pv_pos[2] - mid_pos[2])

    # Add offset away from mid position
    # - Moves pole vector to mid position PLUS original distance from initial position to mid position
    pv_pos_off = (mid_pos[0] - pv_dist[0], mid_pos[1] - pv_dist[1], mid_pos[2] - pv_dist[2])
    pv_pos_off = (pv_pos_off[0], pv_pos_off[1], pv_pos_off[2]*dist)
    mc.xform(pv_ctl, t=pv_pos_off)

    # Add group node above pole vector control to zero it out
    pv_grp = mc.duplicate(pv_ctl, po=True, name='{}_grp'.format(pv_ctl))[0]
    mc.parent(pv_ctl, pv_grp)

    # Create pole vector constraint
    mc.poleVectorConstraint(pv_ctl, ik_handle)

    return pv_pos_off
