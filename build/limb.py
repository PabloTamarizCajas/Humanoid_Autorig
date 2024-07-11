import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as namejnts
reload(namejnts)

from Humanoid_Autorig.build import ik_limb as ik
reload(ik)

from Humanoid_Autorig.build import fk as fk
reload(fk)

from Humanoid_Autorig.build import utils as utils
reload(utils)

def createLimb(type, listJnts):
    #limbParent = mc.group(n='Limb_'+type + '_grp',em=True)
    fingerGrp = None
    clavicleList = None
    worldLoc = None
    if listJnts[0].startswith('L_'):
        
        side = 'L_'
        limbGrp = mc.group(n=side+type + '_grp',em=True)
        limbOff = mc.group(n=side+type + '_off',em=True)
        
        
    elif listJnts[0].startswith('R_'):

        side = 'R_'
        limbGrp = mc.group(n=side+type + '_grp',em=True)
        limbOff = mc.group(n=side+type + '_off',em=True)
        
    if type == 'leg':
        
        posParentJoint = mc.xform(listJnts[0],q=True,ws=True,t=True)
        rotParentJoint = mc.xform(listJnts[0],q=True,ws=True,ro=True)
        mc.xform(limbGrp,ws=True,t=posParentJoint,ro=rotParentJoint)
        mc.parent(limbOff,limbGrp)
        fkList,fkCtl,parentFKGrp = fk.createFK(type=type, listJnts=listJnts)
        ikList,ikCtl,parentIKGrp = ik.createIk(type=type, listJnts=listJnts)
        jointList = listJnts

        switchIkFk(ikList,fkList,jointList,parentIKGrp,parentFKGrp,ikCtl,fkCtl)
        
        mc.parent(parentFKGrp,limbOff)
        mc.parent(parentIKGrp,limbOff)
        fingerGrp = None
        clavicleList = ikList
        worldLoc = fkList
        #mc.parent(limbParent,parentFKGrp)
        
    elif type == 'arm':
        fingerGrp = mc.group(n=side+'finger_grp',em=True)
        posParentJoint = mc.xform(listJnts[1],q=True,ws=True,t=True)
        rotParentJoint = mc.xform(listJnts[1],q=True,ws=True,ro=True)
        mc.xform(limbGrp,ws=True,t=posParentJoint,ro=rotParentJoint)
        mc.parent(limbOff,limbGrp)
        fkList,fkCtl,parentFKGrp = fk.createFK(type=type, listJnts=listJnts[1:])
        ikList,ikCtl,parentIKGrp = ik.createIk(type=type, listJnts=listJnts[1:])
        posFingerGrp = mc.xform(fkList[-1],q=True,ws=True,t=True)
        rotFingerGrp = mc.xform(fkList[-1],q=True,ws=True,ro=True)
        mc.xform(fingerGrp,ws=True,t=posFingerGrp,ro=rotFingerGrp)
        jointList = listJnts

        switchIkFk(ikList,fkList,jointList[1:],parentIKGrp,parentFKGrp,ikCtl,fkCtl,fingerGrp)
        
        mc.parent(parentFKGrp,limbOff)
        mc.parent(parentIKGrp,limbOff)
    
    #create clavicle
        Locpos = mc.xform(jointList[1],q=True,ws=True,t=True)
        LocRot = mc.xform(jointList[1],q=True,ws=True,ro=True)
        localLoc = mc.spaceLocator(n=jointList[0]+'_local_LOC')
        mc.xform(localLoc,ws=True,t=Locpos,ro=LocRot)
        
        ctlPos = mc.xform(jointList[0],q=True,ws=True,t=True)
        ctlRot = mc.xform(jointList[0],q=True,ws=True,ro=True)
        clavicleCtl = mc.circle(n=jointList[0]+'_ctl', nr=(0,1,0), c=(0,0,0), r=1)[0]
        mc.xform(clavicleCtl,ws=True,t=ctlPos,ro=ctlRot)
        mc.parentConstraint(clavicleCtl,jointList[0],mo=True)
        
        clavicleList = utils.add_transforms([clavicleCtl])
        
        mc.addAttr(clavicleCtl,ln='FollowWorld',at='double',min=0,max=1,dv=1,k=True)
        
        mc.setAttr(clavicleCtl + '.tx', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.ty', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.tz', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.sx', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.sy', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.sz', lock=True,k=False, channelBox=False)
        mc.setAttr(clavicleCtl + '.v', lock=True,k=False, channelBox=False)
        
        mc.parent(localLoc,clavicleCtl)
        mc.select(cl=True)
        
        worldLoc = mc.spaceLocator(n=jointList[0]+'_world_LOC')
        mc.xform(worldLoc,ws=True,t=Locpos,ro=LocRot)
        
        localCostraint = mc.parentConstraint(localLoc,limbGrp,mo=True)

        worldContraint = mc.parentConstraint(worldLoc,limbGrp,mo=True)
        
        reverse = mc.shadingNode('reverse',asUtility=True,n=jointList[0]+'_reverse')
        mc.connectAttr(clavicleCtl+'.FollowWorld',localCostraint[0]+'.'+localLoc[0]+'W0')
        mc.connectAttr(clavicleCtl+'.FollowWorld',reverse+'.inputX')
        mc.connectAttr(reverse+'.outputX',worldContraint[0]+'.'+worldLoc[0]+'W1')

    mc.select(cl=True)

    return limbGrp, fingerGrp, clavicleList,worldLoc

def switchIkFk(ik,fk,jointList,ik_grp,fk_grp,ikCtl,fkCtl,fingerGrp=None):
    #create attribute to switch between ik and fk in each fk control
    ctl = fkCtl[0]
    mc.addAttr(ctl,ln='fkIk',at='double',min=0,max=1,dv=0,k=True)
    baseCtl = ctl
    attr = "fkIk"
    
    for a in fkCtl[1:]:
        mc.addAttr(a, ln=attr, proxy="{}.{}".format(baseCtl, attr), at="float", min=0, max=1, k=1)
    for a in ikCtl:
        mc.addAttr(a, ln=attr, proxy="{}.{}".format(baseCtl, attr), at="float", min=0, max=1, k=1)
        
    for joint, ik_name, fk_name in zip(jointList, ik, fk):
        constraint = mc.parentConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_parentConstraint'))
        reverse = mc.shadingNode('reverse', asUtility=True, n=joint.replace('_JNT', '_reverse'))
        mc.connectAttr(ctl+ '.fkIk', reverse + '.inputX')
        mc.connectAttr(ctl + '.fkIk', constraint[0] + '.' + ik_name + 'W0')
        mc.connectAttr(reverse + '.outputX', constraint[0] + '.' + fk_name + 'W1')
        mc.select(cl=True)

    mc.connectAttr(reverse+'.outputX',fk_grp+'.v',f=True)
    mc.connectAttr(fkCtl[0]+'.fkIk',ik_grp+'.v',f=True)
    if fingerGrp != None:
        fingerContraint = mc.parentConstraint(ikCtl[0], fkCtl[-1], fingerGrp, mo=False, weight=1)

        #connect finger contraint to fkIk attribute
        mc.connectAttr(ctl+'.fkIk',fingerContraint[0]+'.'+ikCtl[0]+'W0')
        mc.connectAttr(reverse + '.outputX',fingerContraint[0]+'.'+fkCtl[-1]+'W1')
    
    for ctl in fkCtl:
        mc.setAttr(ctl + '.sx', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.sy', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.sz', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.v', lock=True,k=False, channelBox=False)
        
    for ctl in ikCtl:
        mc.setAttr(ctl + '.sx', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.sy', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.sz', lock=True,k=False, channelBox=False)
        mc.setAttr(ctl + '.v', lock=True,k=False, channelBox=False)
    
    return

def createFinger(type,listJnts): 
    
    fkList,fkCtl,parentFKGrp = fk.createFK(type=type, listJnts=listJnts, r=0.2)
    
    return parentFKGrp,fkCtl
    
def buildArm1():
    limbGrp, fingerGrp, clavicleList,worldLoc = createLimb('arm',namejnts.jointList()[1])
    thumbFkGrp, thumbFk = createFinger('thumb',namejnts.jointList()[5])
    indexFkGrp, indexFk = createFinger('index',namejnts.jointList()[7])
    middleFkGrp, middleFk = createFinger('middle',namejnts.jointList()[9])
    ringFkGrp, ringFk = createFinger('ring',namejnts.jointList()[11])
    pinkyFkGrp, pinkyFk = createFinger('pinky',namejnts.jointList()[13])
    
    mc.parent(thumbFkGrp,fingerGrp)
    mc.parent(indexFkGrp,fingerGrp)
    mc.parent(middleFkGrp,fingerGrp)
    mc.parent(ringFkGrp,fingerGrp)
    mc.parent(pinkyFkGrp,fingerGrp)
    mc.parent(fingerGrp,limbGrp)
    return limbGrp,clavicleList,worldLoc

def buildArm2():
    limbGrp, fingerGrp, clavicleList,worldLoc = createLimb('arm',namejnts.jointList()[2])
    thumbFkGrp, thumbFk = createFinger('thumb',namejnts.jointList()[6])
    indexFkGrp, indexFk = createFinger('index',namejnts.jointList()[8])
    middleFkGrp, middleFk = createFinger('middle',namejnts.jointList()[10])
    ringFkGrp, ringFk = createFinger('ring',namejnts.jointList()[12])
    pinkyFkGrp, pinkyFk = createFinger('pinky',namejnts.jointList()[14])
    
    mc.parent(thumbFkGrp,fingerGrp)
    mc.parent(indexFkGrp,fingerGrp)
    mc.parent(middleFkGrp,fingerGrp)
    mc.parent(ringFkGrp,fingerGrp)
    mc.parent(pinkyFkGrp,fingerGrp)
    mc.parent(fingerGrp,limbGrp)
    return limbGrp,clavicleList,worldLoc

#createLimb('leg',namejnts.jointList()[3])
#createLimb('leg',namejnts.jointList()[4])




