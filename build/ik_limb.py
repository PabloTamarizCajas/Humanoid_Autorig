import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as namejnts
reload(namejnts)

from Humanoid_Autorig.build import utils as utils
reload(utils)

def createIk(type,listJnts):
     
    if listJnts[0].startswith('L_'):
        parentFkGrp = mc.group(n='IK_' + type + '_L_grp',em=True)
        side = 'L_'

    elif listJnts[0].startswith('R_'):
        parentFkGrp = mc.group(n='IK_' + type + '_R_grp',em=True)
        side = 'R_'

    
    elif listJnts[0].startswith('C_'):
        parentFkGrp = mc.group(n='IK_' + type + '_C_grp',em=True)
        side = 'C_'

    if type == 'leg':
        
        joints_ik = []
        joints_ik = createChain(listJnts,'_IK')
        ctl_ik = []
        
        ctl = createCtl(joints_ik[2],type)
        grp = utils.add_transforms([ctl])
        
        nameIkh = joints_ik[2].replace('_JNT','_ikh')
        mc.ikHandle(sj=joints_ik[0],ee=joints_ik[2],sol='ikRPsolver',n=nameIkh)
        
        pv = mc.circle(n=ctl.replace('_ctl','_pv'), nr=(1,0,0), c=(0,0,0), r=1)[0]
        pvctl,pvgrp = create_pole_vector(pv, nameIkh,dist=5)
        
        reverse_ik,groupRollGrp,legConn = reverseFootIk(joints_ik,pvgrp,side)
 
        mc.parent(nameIkh,reverse_ik[-1])
        mc.parent(reverse_ik[0],ctl)
        mc.parent(grp[0],parentFkGrp)
        mc.parent(groupRollGrp[0],ctl)
        mc.parent(joints_ik[0],parentFkGrp)
        mc.parent(pvgrp,parentFkGrp)
        mc.parent(legConn,parentFkGrp)
        
        ctl_ik.append(ctl)
        ctl_ik.append(pv)
        
    elif type == 'arm':
        joints_ik = []
        joints_ik = createChain(listJnts,'_IK')
        ctl_ik = []
        
        ctl = createCtl(joints_ik[2],type)
        grp = utils.add_transforms([ctl])
        
        nameIkh = joints_ik[2].replace('_JNT','_ikh')
        mc.ikHandle(sj=joints_ik[0],ee=joints_ik[2],sol='ikRPsolver',n=nameIkh)
        
        pv = mc.circle(n=ctl.replace('_ctl','_pv'), nr=(1,0,0), c=(0,0,0), r=1)[0]
        pvctl,pvgrp = create_pole_vector(pv, nameIkh,dist=5)
        
        mc.orientConstraint(ctl,joints_ik[-1],mo=True)
        
        mc.parent(grp[0],parentFkGrp)
        mc.parent(joints_ik[0],parentFkGrp)
        mc.parent(pvgrp,parentFkGrp)
        mc.parent(nameIkh,ctl)

        ctl_ik.append(ctl)
        ctl_ik.append(pv)
    
    return joints_ik,ctl_ik, parentFkGrp
    
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

def createCtl(name,type):
    nameCtl = name.replace('_JNT','_ctl')
    if type == 'arm':
        ypos=1
        #create ik handles
        mc.circle(n=nameCtl, nr=(0,1,0), c=(0,0,0), r=1)
        jntPos = mc.xform(name, q=True, ws=True, t=True)
        jntPos = [jntPos[0],jntPos[1]*ypos,jntPos[2]]
        jntRot = mc.xform(name, q=True, ws=True, ro=True)
        mc.xform(nameCtl, ws=True, t=jntPos,ro=jntRot)
    elif type == 'leg':
        #create ik handles
        mc.circle(n=nameCtl, nr=(0,1,0), c=(0,0,0), r=1)
        jntPos = mc.xform(name, q=True, ws=True, t=True)
        jntPos = [jntPos[0],jntPos[1],jntPos[2]]
        mc.xform(nameCtl, ws=True, t=jntPos)
    
    
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

    return pv_ctl,pv_grp

def reverseFootIk(jointIk,pv,side):
    locList = side+'RevCBank_LOC', side+'RevEBank_LOC', side+'RevHeel_LOC', side+'toe_LOC', side+'toeEnd_LOC', side+'toe_LOC', side+'foot_LOC'
    jntList = side+'revCBank_MCH', side+'revEBank_MCH', side+'revHeel_MCH', side+'revPivot_MCH', side+'revToe_MCH',side+'revBall_MCH',side+'revAnkle_MCH'
    
    ikh2 = mc.ikHandle(sj=jointIk[-3],ee=jointIk[-2],sol='ikSCsolver',n=jntList[-2].replace('_MCH','_ikh'))
    ikh1 = mc.ikHandle(sj=jointIk[-2],ee=jointIk[-1],sol='ikSCsolver',n=jntList[-1].replace('_MCH','_ikh'))
    posikh1 = mc.xform(ikh1[0],q=True,ws=False,t=True)
    posikh2 = mc.xform(ikh1[1],q=True,ws=False,t=True)
    mc.select(cl=True)
    
    for loc,jnt in zip(locList,jntList):
        
        locPos = utils.xform_info(loc)[0]
        mc.joint(n=jnt, p=locPos, rad=0.2)
        if jnt == jntList[-2]:
            locPos = mc.xform(locList[-3], q=True, ws=True, t=True)
        
        if jnt != jntList[0]:
            mc.parent(jnt, jntList[jntList.index(jnt)-1])
            
        #condition when the jntList is the [-3], the y position must be 0
        if jnt == jntList[-3]:
            mc.setAttr(jnt+'.ty',0)
            
        mc.select(cl=True)
    
    mc.parent(ikh1[0],jntList[-3])
    mc.parent(ikh2[0],jntList[-2])
    
    rollCtl = mc.circle(n=side+'Roll_ctl', nr=(1,0,0), c=(0,0,0), r=1)[0]

    pos_ctl = mc.xform(locList[-1], q=True, ws=True, t=True)
    pos_ctl = [pos_ctl[0],pos_ctl[1],pos_ctl[2]-3]
    mc.xform(rollCtl, ws=True, t=pos_ctl)
    grpRoll = utils.add_transforms([rollCtl])
    
    mc.addAttr(rollCtl, ln='weight', at='float', dv=0, k=True, min=0, max=1)
    mc.setAttr(rollCtl+'.tx', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.ty', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.tz', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.sx', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.sy', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.sz', lock=True, keyable=False, channelBox=False)
    mc.setAttr(rollCtl+'.v', lock=True, keyable=False, channelBox=False)
    #Connect the rollCtl to the Z rotation of the joints
    rollConditionZ = mc.createNode('condition', n=rollCtl.replace('_ctl','_z_cond'))
    mc.setAttr(rollConditionZ+'.operation', 2)
    
    mc.connectAttr(rollCtl+'.rz',rollConditionZ+'.firstTerm')
    mc.connectAttr(rollCtl+'.rz',rollConditionZ+'.colorIfTrueR')
    mc.connectAttr(rollCtl+'.rz',rollConditionZ+'.colorIfFalseG')
    
    mc.connectAttr(rollConditionZ+'.outColorR',jntList[0]+'.rz')
    mc.connectAttr(rollConditionZ+'.outColorG',jntList[1]+'.rz')
    
    #Connect the rollCtl to the X rotation of the joints
    rollConditionX = mc.createNode('condition', n=rollCtl.replace('_ctl','_x_cond'))
    rollWeightBC = mc.createNode('blendColors', n=rollCtl.replace('_ctl','_weight_bc'))
    mc.setAttr(rollConditionX+'.operation', 4)
    
    mc.connectAttr(rollCtl+'.rx',rollConditionX+'.firstTerm')
    mc.connectAttr(rollCtl+'.rx',rollConditionX+'.colorIfTrueR')
    mc.connectAttr(rollCtl+'.rx',rollConditionX+'.colorIfFalseG')
    
    mc.connectAttr(rollConditionX+'.outColorR',jntList[2]+'.rx')
    mc.connectAttr(rollConditionX+'.outColorG',rollWeightBC+'.color1R')
    mc.connectAttr(rollConditionX+'.outColorG',rollWeightBC+'.color2G')
    mc.connectAttr(rollCtl+'.weight',rollWeightBC+'.blender')
    
    mc.connectAttr(rollWeightBC+'.outputR',jntList[-3]+'.rx')
    mc.connectAttr(rollWeightBC+'.outputG',jntList[-2]+'.rx')
    #local position of my ikh1
    
    setRange = mc.createNode('setRange', n=rollCtl.replace('_ctl','_setRange'))
    mc.connectAttr(rollWeightBC+'.outputR',setRange+'.valueX')
    mc.setAttr(setRange+'.oldMaxX',30)
    mc.setAttr(setRange+'.minX',posikh1[1])
    mc.connectAttr(setRange+'.outValueX',ikh1[0]+'.ty')
    
    #activate when you finished
    mc.connectAttr(rollCtl+'.ry',jntList[3]+'.ry')
    
    legConn = noFlipIk(jointIk,jntList,pv,side)
    
    return jntList,grpRoll,legConn

def noFlipIk(jointList,jntList,pv,side):
    
            posTop = mc.xform(jointList[0],q=True,ws=True,t=True)
            posBot = mc.xform(jointList[2],q=True,ws=True,t=True)
            posPv = mc.xform(pv,q=True,ws=True,t=True)
            #create Joints
            jntTop = mc.joint(n=side+'noFlipTop_MCH',p=posTop,rad=0.2)
            jntTopEnd = mc.joint(n=side+'noFlipTopEnd_MCH',p=posBot,rad=0.2)
            ikhTopFlip = mc.ikHandle(sj=jntTop,ee=jntTopEnd,sol='ikRPsolver',n=side+'noFlipTop_ikh')
            
            mc.select(cl=True)
            
            jntBot = mc.joint(n=side+'noFlipBot_MCH',p=posBot,rad=0.2)
            jntBotEnd = mc.joint(n=side+'noFlipBotEnd_MCH',p=posTop,rad=0.2)
            ikhBotFlip = mc.ikHandle(sj=jntBot,ee=jntBotEnd,sol='ikRPsolver',n=side+'noFlipBot_ikh')
            
            #create locators
            locTopNoflip = mc.spaceLocator(n=side+'noFlipTop_LOC')[0]
            locBotNoFLip = mc.spaceLocator(n=side+'noFlipBot_LOC')[0]
            locTop = mc.spaceLocator(n=side+'Top_LOC')[0]
            locBot = mc.spaceLocator(n=side+'Bot_LOC')[0]
            mc.xform(locTopNoflip,ws=True,t=(posTop[0]+1,posTop[1],posTop[2]))
            mc.xform(locBotNoFLip,ws=True,t=(posBot[0]+1,posBot[1],posBot[2]))
            mc.xform(locTop,ws=True,t=posPv)
            mc.xform(locBot,ws=True,t=posPv)
            
            #create pole vector using my locators
            mc.poleVectorConstraint(locTopNoflip,ikhTopFlip[0])
            mc.poleVectorConstraint(locBotNoFLip,ikhBotFlip[0])
            
            mc.parent(locBotNoFLip,jntList[-1])
            mc.parent(ikhTopFlip[0],jntList[-1])
            mc.parent(jntBot,jntList[-1])
            
            mc.select(cl=True)
            
            legConn = mc.joint(n=side+'legConn_MCH',p=posTop,rad=0.2)
            mc.parent(locTopNoflip,legConn)
            mc.parent(ikhBotFlip[0],legConn)
            mc.parent(jntTop,legConn)
            
            mc.parent(locBot,jntBot)
            mc.parent(locTop,jntTop)
            
            mc.pointConstraint(locTop,pv)
            mc.pointConstraint(locBot,pv)
            
            return legConn
        
