import maya.cmds as mc

from Humanoid_Autorig.build import spine as sp
reload(sp)

from Humanoid_Autorig.build import limb as lb
reload(lb)

from Humanoid_Autorig.build import autorig_names as namejnts

def buildHumanoid():
    #create spine
    spFkCtls,spFkGrp,spIkCtls,spIkGrp = sp.createSpine()
    #create left limb (arm)
    aLLimbGrp,aLClavicleList,aLWolrdLoc = lb.buildArm1()
    #parent spFkGrp, spIkGrp,aLLimbGrp,aLClavicleList,aLWolrdLoc to root
    mc.parent(spFkGrp,'root')
    mc.parent(spIkGrp,'root')
    mc.parent(aLLimbGrp,'root')
    mc.parent(aLClavicleList[0],'root')
    mc.parent(aLWolrdLoc[0],'root')
    #create a parent constraint between the left clavivle and the last ik spine control and fk spine control
    clavicleLPC = mc.parentConstraint(spFkCtls[-1],spIkCtls[-1], aLClavicleList[0],mo=True)
    locWorldLPC = mc.parentConstraint(spFkCtls[-1],spIkCtls[-1], aLWolrdLoc[0],mo=True,sr=['x','y','z'],w=1)
    #connect the last fk spine ikfk attribute to the clavicle contraint
    mc.connectAttr(spFkCtls[-1]+'.fkIk',clavicleLPC[0]+'.'+spIkCtls[-1]+'W1')
    mc.connectAttr(spFkCtls[-1]+'.fkIk',locWorldLPC[0]+'.'+spIkCtls[-1]+'W1')
    #crete a reversenode to switch between ik and fk
    revNode = mc.createNode('reverse',n='clavicle_rev')
    #connect the reverse node into the 'ikfk' attribute of the spine
    mc.connectAttr(spFkCtls[-1]+'.fkIk',revNode+'.inputX')
    #connect the reverse node into the clavicle contraint
    mc.connectAttr(revNode+'.outputX',clavicleLPC[0]+'.'+spFkCtls[-1]+'W0')
    mc.connectAttr(revNode+'.outputX',locWorldLPC[0]+'.'+spFkCtls[-1]+'W0')
    #--------------------------------------------------------------------------------
    #create right limb (arm)
    aRLimbGrp,aRClavicleList,aRWolrdLoc = lb.buildArm2()
    #parent aRLimbGrp,aRClavicleList,aRWolrdLoc to root
    mc.parent(aRLimbGrp,'root')
    mc.parent(aRClavicleList[0],'root')
    mc.parent(aRWolrdLoc[0],'root')
    #create a parent constraint between the right clavivle and the last ik spine control and fk spine control
    clavicleRPC = mc.parentConstraint(spFkCtls[-1],spIkCtls[-1], aRClavicleList[0],mo=True)
    locWorldRPC = mc.parentConstraint(spFkCtls[-1],spIkCtls[-1], aRWolrdLoc[0],mo=True,sr=['x','y','z'],w=1)
    #connect the last fk spine ikfk attribute to the clavicle contraint
    mc.connectAttr(spFkCtls[-1]+'.fkIk',clavicleRPC[0]+'.'+spIkCtls[-1]+'W1')
    mc.connectAttr(spFkCtls[-1]+'.fkIk',locWorldRPC[0]+'.'+spIkCtls[-1]+'W1')
    #connect the reverse node into the clavicle contraint
    mc.connectAttr(revNode+'.outputX',clavicleRPC[0]+'.'+spFkCtls[-1]+'W0')
    mc.connectAttr(revNode+'.outputX',locWorldRPC[0]+'.'+spFkCtls[-1]+'W0')
    #--------------------------------------------------------------------------------
    #create left leg
    lLLimbGrp,a,lLIkList,lLFkList =lb.createLimb('leg',namejnts.jointList()[3])
    #--------------------------------------------------------------------------------
    #create right leg
    lRLimbGrp,a,lRIkList,lRFkList =lb.createLimb('leg',namejnts.jointList()[4])
    
    
buildHumanoid()