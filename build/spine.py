import maya.cmds as mc
import maya.mel as mel

from Humanoid_Autorig.build import autorig_names as namejnts
reload(namejnts)

from Humanoid_Autorig.build import fk as fk
reload(fk)

from Humanoid_Autorig.build import utils as utils
reload(utils)

def createSpine():
    spineJnts = namejnts.jointList()[0]
    #create fk spine
    fkList,fkCtls, fkGrp = fk.createFK('spine',spineJnts[:-3],r=3)
    #create ik spine
    ikJnts,chestIk,markersCtl,ik_grp = ikSpine(r=3)
    newIkJnts = ikJnts[:3] + [chestIk]
    #create ikfk switch
    switchIkFk(newIkJnts,fkList,spineJnts,ik_grp,fkGrp,markersCtl,fkCtls)
    return fkCtls, fkGrp, markersCtl, ik_grp
         
def ikSpine(r=2):
    #create a cv curve with 4 points
    spineJnts = namejnts.jointList()[0]

    posJnts = []
    #obtain the position of the joints
    for jnt in spineJnts[:4]:
        pos = mc.xform(jnt,q=True,ws=True,t=True)
        posJnts.append(pos)
    #create a cv curve with 4 points
    spineCrv = mc.curve(d=3,p=posJnts,n='spine_crv')
    #duplicate the curve and move it t othe left and right 0.5 units
    spineCrvLeft = mc.duplicate(spineCrv,rr=True)
    spineCrvRight = mc.duplicate(spineCrv,rr=True)
    mc.move(-0.5,0,0,spineCrvLeft[0],r=True)
    mc.move(0.5,0,0,spineCrvRight[0],r=True)
    #create loft surface using the spineCrvLeft and spineCrvRight
    spineSurf = mc.loft(spineCrvLeft[0],spineCrvRight[0],ch=True, u=True, c=False, ar=True, d=3, ss=True, rn=False, po=False, rsn=True,n='spine_surf')
    #create hair in the surface, u 4, v 1
    mc.select(spineSurf[0])
    createHair = mel.eval('CreateHair 4 1 0 0 0 0 0 5 0 1 1 0 1;')
    mc.delete('hairSystem1')
    mc.delete('nucleus1')
    mc.delete('pfxHair1')
    #create a list of the relatives of the hairSystem1Follicles
    hairFollicles = mc.listRelatives('hairSystem1Follicles')
    #delete hairFollicles children
    for hairFollicle in hairFollicles:
        children = mc.listRelatives(hairFollicle, c=True)
        mc.delete(children[-1])
        
    follicleShape = mc.ls(type='follicle')
    mc.setAttr(follicleShape[0]+'.parameterU', 0)
    mc.setAttr(follicleShape[-1]+'.parameterU', 1)
    mc.setAttr(follicleShape[2]+'.parameterU', 0.685)
    
    #delete the curves spineCrvLeft and spineCrvRight
    mc.delete(spineCrvLeft[0])
    mc.delete(spineCrvRight[0])
    mc.select(cl=True)
    #create a chain of ik joints in the same position and rotation of the spineJnts
    ikJnts = []
    for jnt in spineJnts[:5]:
        pos = mc.xform(jnt, q=True, ws=True, t=True)
        ikJnt = mc.joint(p=pos,n=jnt.replace('_JNT','_IK'),rad=0.25)
        #rot = mc.xform(jnt, q=True, ws=True, ro=True)
        #mc.rotate(rot[0], rot[1], rot[2], ikJnt, ws=True)
        ikJnts.append(ikJnt)
    mc.joint(ikJnts[0],e=True,oj='yzx',secondaryAxisOrient='zup',ch=True,zso=True)
    #mc.joint(ikJnts[-1],e=True,oj=None,ch=True,zso=True)
    mc.select(cl=True)    
    #create a chain of mch joints in the same position and rotation of the spineJnts
    mchJnts = []
    for jnt in spineJnts[:4]:
        pos = mc.xform(jnt, q=True, ws=True, t=True)
        mchJnt = mc.joint(p=pos,n=jnt.replace('_JNT','_MCH'),rad=0.25)
        #rot = mc.xform(jnt, q=True, ws=True, ro=True)
        #mc.rotate(rot[0], rot[1], rot[2], mchJnt, ws=True)
        mchJnts.append(mchJnt)
    mc.joint(mchJnts[0],e=True,oj='yzx',secondaryAxisOrient='zup',ch=True,zso=True)
    #mc.joint(mchJnts[-1],e=True,oj=None,ch=True,zso=True)
        
    #create ik spline handle in the ikJnts,use the spineCrv as curve
    ikHandle = mc.ikHandle(sj=mchJnts[0],ee=mchJnts[3],c=spineCrv,sol='ikSplineSolver',ccv=False,roc=True,n='spine_ikHandle')
    mc.select(cl=True)
    #create 3 joints not connected and the first on the jnt[0] position of my spineJnts, the second in the middle of the spineJnts and the third in the last position of the spineJnts
    makersJnts = ['C_pelvis_Mrkr_MCH','C_spine_Mrkr_MCH','C_chest_Mrkr_MCH']
    for jnt in makersJnts:
        mc.joint(n=jnt,rad=0.25)
        mc.select(cl=True)
    
    mc.xform(makersJnts[0],ws=True,t=mc.xform(spineJnts[0],q=True,ws=True,t=True))
    pos1,rot1,sc1 = utils.xform_info(spineJnts[1],tr=True,rot=True,sc=False)
    pos2,rot1,sc1 = utils.xform_info(spineJnts[2],tr=True,sc=False)
    pos= [(pos1[0]+pos2[0])/2,(pos1[1]+pos2[1])/2,(pos1[2]+pos2[2])/2]
    mc.xform(makersJnts[1],ws=True,t=pos)
    mc.xform(makersJnts[2],ws=True,t=mc.xform(spineJnts[3],q=True,ws=True,t=True))
    
    #select markerKnts and spineCurve and create bindSkin
    mc.select(makersJnts)
    mc.select(spineCrv,add=True)
    mc.skinCluster(tsb=True,bm=0,sm=0,nw=1,wd= 1,mi=3,omi=True,rui=True,dr=4)
    mc.select(cl=True)
    mc.select(makersJnts)
    mc.select(spineSurf[0],add=True)
    mc.skinCluster(bm=0,sm=0,nw=1,wd= 1,mi=3,omi=True,rui=True,dr=4)
    mc.select(cl=True)

    
    #create nodes
    for mchjnt,fShape in zip(mchJnts,follicleShape):
        closestPointNode = mc.createNode('closestPointOnSurface',n=mchjnt.replace('_MCH','_CPS'))
        decomposeMatrix = mc.createNode('decomposeMatrix',n=mchjnt.replace('_MCH','_DM'))
        mc.connectAttr(spineSurf[0]+'.worldSpace[0]',closestPointNode+'.inputSurface')
        mc.connectAttr(mchjnt+'.worldMatrix[0]',decomposeMatrix+'.inputMatrix')
        mc.connectAttr(decomposeMatrix+'.outputTranslate',closestPointNode+'.inPosition')
        mc.connectAttr(closestPointNode+'.parameterU',fShape+'.parameterU')
        mc.connectAttr(closestPointNode+'.parameterV',fShape+'.parameterV')
        
    #parent contraint IkJnts to follicleShape
    for ikjnt,fShape in zip(ikJnts,hairFollicles):
        #apply parent constraint to the first 3 ikJnts and in the 4th ikJnt apply point constraint
        if ikjnt != ikJnts[-2]:
            mc.parentConstraint(fShape,ikjnt,mo=True)
        else:
            mc.pointConstraint(fShape,ikjnt,mo=True)
            mc.parentConstraint(fShape,ikjnt,mo=True,skipTranslate=['x','y','z'],w=1)
            
    #create ctls for the markers
    markersCtl = []
    for mchjnt in makersJnts:
        ctl = mc.circle(n=mchjnt.replace('_Mrkr_MCH','_ctl'),nr=(0,1,0),c=(0,0,0),r=r)[0]
        posMarker = utils.pos_info(mchjnt)
        mc.xform(ctl,ws=True,t=posMarker)
        listCtl = utils.add_transforms([ctl])
        mc.setAttr(ctl+'.sx',lock=True,k=False,cb=False)
        mc.setAttr(ctl+'.sy',lock=True,k=False,cb=False)
        mc.setAttr(ctl+'.sz',lock=True,k=False,cb=False)
        mc.setAttr(ctl+'.v',lock=True,k=False,cb=False)
        markersCtl.append(ctl)
    #parent markersCtl to makersJnts
    mc.parent(makersJnts[0],markersCtl[0])
    mc.parent(makersJnts[1],markersCtl[1])
    mc.parent(makersJnts[2],markersCtl[2])
    
    #unparent last ikJnt
    mc.parent(ikJnts[-1],w=True)
    mc.select(cl=True)
    #create joint in the ikjnts[3] position and rotation
    pos = mc.xform(ikJnts[3],q=True,ws=True,t=True)
    rot = mc.xform(ikJnts[3],q=True,ws=True,ro=True)
    chestIk = mc.joint(p=pos,n='C_chest_IK',rad=0.5)
    #parent ikJnts[-1] to chestIk
    mc.parent(ikJnts[-1],chestIk)
    #create parent contraint only translate, from chestIk to ikJnts[3]
    mc.parentConstraint(makersJnts[2],chestIk,mo=True)
    #Stretchy spine
    #create curve info node for the spineCrv
    curveInfo = mc.createNode('curveInfo',n='spine_curveInfo')
    mc.connectAttr(spineCrv+'.worldSpace[0]',curveInfo+'.inputCurve')
    #create multiplyDivide node to get the curve length
    multiplyDivide01 = mc.createNode('multiplyDivide',n='spine_multiplyDivide_01')
    multiplyDivide02 = mc.createNode('multiplyDivide',n='spine_multiplyDivide_02')
    mc.setAttr(multiplyDivide01+'.operation',2)
    mc.setAttr(multiplyDivide02+'.operation',2)
    #get the curve length
    arcLenght = mc.getAttr(curveInfo+'.arcLength')
    #connect the curve length to the multiplyDivide01
    mc.setAttr(multiplyDivide01+'.input2X',arcLenght)
    mc.connectAttr(curveInfo+'.arcLength',multiplyDivide01+'.input1X')
    #set input2X of multiplyDivide02 to 1
    mc.setAttr(multiplyDivide02+'.input1X',1)
    #connect the outputX of multiplyDivide01 to the input2X of multiplyDivide02
    mc.connectAttr(multiplyDivide01+'.outputX',multiplyDivide02+'.input2X')
    
    #create attribute to control the stretch
    ctlAtr = markersCtl[-1]
    mc.addAttr(ctlAtr,ln='stretch',at='double',min=0,max=1,dv=1,k=True)
    baseCtl = ctlAtr
    attr = "stretch"
    for a in markersCtl[:2]:
        mc.addAttr(a, ln=attr, proxy="{}.{}".format(baseCtl, attr), at="float", min=0, max=1, k=1)
    #create blendColors node to control the stretch
    blendColors = mc.createNode('blendColors',n='spine_blendColors')
    mc.connectAttr(ctlAtr+'.stretch',blendColors+'.blender')
    #connect multiplyDivide01 to blendcolors
    mc.connectAttr(multiplyDivide01+'.outputX',blendColors+'.color1G')
    mc.connectAttr(multiplyDivide01+'.input2Y',blendColors+'.color2R')
    mc.connectAttr(multiplyDivide01+'.input2Y',blendColors+'.color2G')
    mc.connectAttr(multiplyDivide01+'.input2Y',blendColors+'.color2B')
    #connect multiplyDivide02 to blendColors
    mc.connectAttr(multiplyDivide02+'.outputX',blendColors+'.color1R')
    mc.connectAttr(multiplyDivide02+'.outputX',blendColors+'.color1B')
    for ikjnt in ikJnts:
        mc.connectAttr(blendColors+'.output',ikjnt+'.scale')
        
    for mchJnt in mchJnts:
        mc.connectAttr(blendColors+'.outputG',mchJnt+'.sy')
        
    #organize all ik joints and ctls in a group
    mc.select([chestIk, 'C_chest_grp', 'C_spine_grp', 'C_pelvis_grp', ikHandle[0], 'C_pelvis_MCH', 'C_pelvis_IK', 'hairSystem1Follicles', 'spine_surf', 'spine_crv'])
    
    ik_grp = mc.group(n='IK_spine_C_grp',w=True,em=False)
    
    return ikJnts,chestIk,markersCtl,ik_grp
    
def switchIkFk(ik,fk,jointList,ik_grp,fk_grp,ikCtl,fkCtl):
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
        #condition for the last ik joint

        reverse = mc.shadingNode('reverse', asUtility=True, n=joint.replace('_JNT', '_reverse'))
        if joint == jointList[3]:
            parentConstraint = mc.parentConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_parentConstraint'),sr=['x','y','z'])
            orientConstraint = mc.orientConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_orientConstraint'))
            scaleConstraint = mc.scaleConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_scaleConstraint'))
            mc.connectAttr(ctl+ '.fkIk', reverse + '.inputX')
            mc.connectAttr(ctl + '.fkIk', parentConstraint[0] + '.' + ik_name + 'W0')
            mc.connectAttr(ctl + '.fkIk', orientConstraint[0] + '.' + ik_name + 'W0')
            mc.connectAttr(reverse + '.outputX', parentConstraint[0] + '.' + fk_name + 'W1')
            mc.connectAttr(reverse + '.outputX', orientConstraint[0] + '.' + fk_name + 'W1')
            mc.connectAttr(ctl + '.fkIk', scaleConstraint[0] + '.' + ik_name + 'W0')
            mc.connectAttr(reverse + '.outputX', scaleConstraint[0] + '.' + fk_name + 'W1')
            mc.select(cl=True)
        
        else:
            parentConstraint = mc.parentConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_parentConstraint'))
            scaleConstraint = mc.scaleConstraint(ik_name, fk_name, joint, mo=True, n=joint.replace('_JNT', '_scaleConstraint'))
            
            mc.connectAttr(ctl+ '.fkIk', reverse + '.inputX')
            mc.connectAttr(ctl + '.fkIk', parentConstraint[0] + '.' + ik_name + 'W0')
            mc.connectAttr(reverse + '.outputX', parentConstraint[0] + '.' + fk_name + 'W1')
            mc.connectAttr(ctl + '.fkIk', scaleConstraint[0] + '.' + ik_name + 'W0')
            mc.connectAttr(reverse + '.outputX', scaleConstraint[0] + '.' + fk_name + 'W1')
            mc.select(cl=True)

    mc.connectAttr(reverse+'.outputX',fk_grp+'.v',f=True)
    mc.connectAttr(fkCtl[0]+'.fkIk',ik_grp+'.v',f=True)
    