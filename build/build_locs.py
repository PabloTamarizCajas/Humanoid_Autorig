import maya.cmds as mc

from Humanoid_Autorig.build import autorig_names as names
reload(names)
    
def createProxyRig():
    loc_List = names.locList()
    spine = loc_List[0]
    arm_left = loc_List[1]
    arm_right = loc_List[2]
    leg_left = loc_List[3]
    leg_right = loc_List[4]
    thumb_left = loc_List[5]
    thumb_right = loc_List[6]
    index_left = loc_List[7]
    index_right = loc_List[8]
    middle_left = loc_List[9]
    middle_right = loc_List[10]
    ring_left = loc_List[11]
    ring_right = loc_List[12]
    pinky_left = loc_List[13]
    pinky_right = loc_List[14]
    leg_left_roll = loc_List[15]
    leg_right_roll = loc_List[16]
    
    C_pelvis_Loc = createLoc(spine[0],(0,10,0))
    #Create Loc Legs
    L_thigh_Loc = createLoc(leg_left[0],(2,10,0))
    R_thigh_Loc = createLoc(leg_right[0],(-2,10,0))
    L_calf_Loc = createLoc(leg_left[1],(2,5,0))
    R_calf_Loc = createLoc(leg_right[1],(-2,5,0))
    L_foot_Loc = createLoc(leg_left[2],(2,1,0))
    R_foot_Loc = createLoc(leg_right[2],(-2,1,0))
    L_revCBank_Loc = createLoc(leg_left_roll[0],(1,0,-0.5))
    R_revCBank_Loc = createLoc(leg_right_roll[0],(-1,0,-0.5))
    L_revEBank_Loc = createLoc(leg_left_roll[1],(3,0,-0.5))
    R_revEBank_Loc = createLoc(leg_right_roll[1],(-3,0,-0.5))
    L_revHeel_Loc = createLoc(leg_left_roll[2],(2,0,-2))
    R_revHeel_Loc = createLoc(leg_right_roll[2],(-2,0,-2))
    L_toe_Loc = createLoc(leg_left[3],(2,1,1))
    R_toe_Loc = createLoc(leg_right[3],(-2,1,1))
    L_toeEnd_Loc = createLoc(leg_left[4],(2,1,2))
    R_toeEnd_Loc = createLoc(leg_right[4],(-2,1,2))
    #Create Loc Spine
    C_spine01_Loc = createLoc(spine[1],(0,11,0))
    C_spine02_Loc = createLoc(spine[2],(0,12,0))
    C_spine03_Loc = createLoc(spine[3],(0,13,0))
    C_neck_Loc = createLoc(spine[4],(0,14,0))
    C_head_Loc = createLoc(spine[5],(0,15,0))
    C_headTop_Loc = createLoc(spine[6],(0,16,0))
    #Create Loc Arms
    L_clavicle_Loc = createLoc(arm_left[0],(2,13,0))
    R_clavicle_Loc = createLoc(arm_right[0],(-2,13,0))
    L_upperarm_Loc = createLoc(arm_left[1],(3,13,0))
    R_upperarm_Loc = createLoc(arm_right[1],(-3,13,0))
    L_lowerarm_Loc = createLoc(arm_left[2],(6.5,13,0))
    R_lowerarm_Loc = createLoc(arm_right[2],(-6.5,13,0))
    L_hand_Loc = createLoc(arm_left[3],(11,13,0))
    R_hand_Loc = createLoc(arm_right[3],(-11,13,0))
    
    # Create Loc Fingers:Index
    L_index01_Loc = createLoc(index_left[0],(12,13,0.5))
    R_index01_Loc = createLoc(index_right[0],(-12,13,0.5))
    L_index02_Loc = createLoc(index_left[1],(12.5,13,0.5))
    R_index02_Loc = createLoc(index_right[1],(-12.5,13,0.5))
    L_index03_Loc = createLoc(index_left[2],(13,13,0.5))
    R_index03_Loc = createLoc(index_right[2],(-13,13,0.5))
    
    # Create Loc Fingers:Middle
    L_middle01_Loc = createLoc(middle_left[0],(12,13,0))
    R_middle01_Loc = createLoc(middle_right[0],(-12,13,0))
    L_middle02_Loc = createLoc(middle_left[1],(12.5,13,0))
    R_middle02_Loc = createLoc(middle_right[1],(-12.5,13,0))
    L_middle03_Loc = createLoc(middle_left[2],(13,13,0))
    R_middle03_Loc = createLoc(middle_right[2],(-13,13,0))
    
    # Create Loc Fingers:Ring
    L_ring01_Loc = createLoc(ring_left[0],(12,13,-0.5))
    R_ring01_Loc = createLoc(ring_right[0],(-12,13,-0.5))
    L_ring02_Loc = createLoc(ring_left[1],(12.5,13,-0.5))
    R_ring02_Loc = createLoc(ring_right[1],(-12.5,13,-0.5))
    L_ring03_Loc = createLoc(ring_left[2],(13,13,-0.5))
    R_ring03_Loc = createLoc(ring_right[2],(-13,13,-0.5))
    
    # Create Loc Fingers:Pinky
    L_pinky01_Loc = createLoc(pinky_left[0],(12,13,-1))
    R_pinky01_Loc = createLoc(pinky_right[0],(-12,13,-1))
    L_pinky02_Loc = createLoc(pinky_left[1],(12.5,13,-1))
    R_pinky02_Loc = createLoc(pinky_right[1],(-12.5,13,-1))
    L_pinky03_Loc = createLoc(pinky_left[2],(13,13,-1))
    R_pinky03_Loc = createLoc(pinky_right[2],(-13,13,-1))

    # Create Loc Fingers:Thumb
    L_thumb01_Loc = createLoc(thumb_left[0],(11,13,1))
    R_thumb01_Loc = createLoc(thumb_right[0],(-11,13,1))
    L_thumb02_Loc = createLoc(thumb_left[1],(11,13,1.5))
    R_thumb02_Loc = createLoc(thumb_right[1],(-11,13,1.5))
    L_thumb03_Loc = createLoc(thumb_left[2],(11,13,2))
    R_thumb03_Loc = createLoc(thumb_right[2],(-11,13,2))
    
    #groupLocators
    mc.group('*_LOC', n='LOCATORS')

    for i in range(0,len(loc_List)):
        createMultipleLineLink(loc_List[i])
    
    createLineLink('L_thigh_LOC','C_pelvis_LOC')
    createLineLink('R_thigh_LOC','C_pelvis_LOC')
    
    createLineLink('L_clavicle_LOC','C_spine03_LOC')
    createLineLink('R_clavicle_LOC','C_spine03_LOC')
    
    createLineLink('L_thumb01_LOC','L_hand_LOC')
    createLineLink('R_thumb01_LOC','R_hand_LOC')
    mc.parent('L_thumb01_LOC','L_hand_LOC')
    mc.parent('R_thumb01_LOC','R_hand_LOC')
    createLineLink('L_index01_LOC','L_hand_LOC')
    createLineLink('R_index01_LOC','R_hand_LOC')
    mc.parent('L_index01_LOC','L_hand_LOC')
    mc.parent('R_index01_LOC','R_hand_LOC')
    createLineLink('L_middle01_LOC','L_hand_LOC')
    createLineLink('R_middle01_LOC','R_hand_LOC')
    mc.parent('L_middle01_LOC','L_hand_LOC')
    mc.parent('R_middle01_LOC','R_hand_LOC')
    createLineLink('L_ring01_LOC','L_hand_LOC')
    createLineLink('R_ring01_LOC','R_hand_LOC')
    mc.parent('L_ring01_LOC','L_hand_LOC')
    mc.parent('R_ring01_LOC','R_hand_LOC')
    createLineLink('L_pinky01_LOC','L_hand_LOC')
    createLineLink('R_pinky01_LOC','R_hand_LOC')
    mc.parent('L_pinky01_LOC','L_hand_LOC')
    mc.parent('R_pinky01_LOC','R_hand_LOC')
    
    mc.group('curve*',n='CURVES')
    
    mc.select(cl=True)
    
def createMultipleLineLink(list):
    for i in range(0,len(list)-1):
        createLineLink(list[i],list[i+1])
        mc.parent(list[i+1],list[i])    
    
def createLoc(locName, pos):
    myLoc = mc.spaceLocator(n=locName)
    myLoc = myLoc[0]
    mc.setAttr(myLoc+'.tx',pos[0])
    mc.setAttr(myLoc+'.ty',pos[1])
    mc.setAttr(myLoc+'.tz',pos[2])
    mc.setAttr(myLoc+'.localScaleX',0.2)
    mc.setAttr(myLoc+'.localScaleY',0.2)
    mc.setAttr(myLoc+'.localScaleZ',0.2)
    side = locName.split('_')
    side = side[0]
    
    if side == 'C':
        
        mc.setAttr(myLoc+'.sx',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sy',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sz',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.v',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.overrideEnabled',1)
        mc.setAttr(myLoc+'.overrideColor',17)
        
        
    if side == 'L':

        mc.setAttr(myLoc+'.sx',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sy',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sz',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.v',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.overrideEnabled',1)
        mc.setAttr(myLoc+'.overrideColor',6)
        
    elif side == 'R':

        mc.setAttr(myLoc+'.sx',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sy',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.sz',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.v',lock=True, keyable=False, channelBox=False)
        mc.setAttr(myLoc+'.overrideEnabled',1)
        mc.setAttr(myLoc+'.overrideColor',13)
    
    return(myLoc)
    
def createLineLink(loc1, loc2):
    checkLOrC = loc1.split('_')
    checkLOrC = checkLOrC[0]
    
    myLine = mc.curve(d=1,p=[(0,0,0),(0,0,0)])
    mc.select(myLine+'.cv[0]')
    cOne= mc.cluster(n='cOne')
    cOne = cOne[1]
    mc.select(myLine+'.cv[1]')
    cTwo= mc.cluster(n='cTwo')
    cTwo = cTwo[1]
    
    mc.parent(cOne,loc1)
    mc.setAttr(cOne+'.tx',0)
    mc.setAttr(cOne+'.ty',0)
    mc.setAttr(cOne+'.tz',0)
    mc.setAttr(cOne+'.v',0)
    
    mc.parent(cTwo,loc2)
    mc.setAttr(cTwo+'.tx',0)
    mc.setAttr(cTwo+'.ty',0)
    mc.setAttr(cTwo+'.tz',0)
    mc.setAttr(cTwo+'.v',0)
    mc.setAttr(myLine+'.template',True)
    mc.select(cl=True)
    
    if checkLOrC == 'L':
        rLocOne = loc1.replace('L_','R_')
        rLocTwo = loc2.replace('L_','R_')
        createLineLink(rLocOne, rLocTwo)

def mirrorTool(type):
    if type == 'selection':
        mirrorObjs = mc.ls(sl=True)
    elif type == 'L':
        mc.select('L_*')
        mirrorObjs = mc.ls(sl=True,tr=True)
        
    elif type == 'R':
        mc.select('R_*')
        mirrorObjs = mc.ls(sl=True,tr=True)
        
    for obj in mirrorObjs:
        side = obj.split('_')
        side = side[0]
        if side == 'L':
            mirrorSide = obj.replace('L_','R_')

            mc.setAttr(mirrorSide+'.tx',mc.getAttr(obj+'.tx')*-1)
            mc.setAttr(mirrorSide+'.ty',mc.getAttr(obj+'.ty'))
            mc.setAttr(mirrorSide+'.tz',mc.getAttr(obj+'.tz'))
            mc.setAttr(mirrorSide+'.rx',mc.getAttr(obj+'.rx'))
            mc.setAttr(mirrorSide+'.ry',mc.getAttr(obj+'.ry')*-1)
            mc.setAttr(mirrorSide+'.rz',mc.getAttr(obj+'.rz')*-1)
            
        elif side == 'R':
            mirrorSide = obj.replace('R_','L_')
            mc.setAttr(mirrorSide+'.tx',mc.getAttr(obj+'.tx')*-1)
            mc.setAttr(mirrorSide+'.ty',mc.getAttr(obj+'.ty'))
            mc.setAttr(mirrorSide+'.tz',mc.getAttr(obj+'.tz'))
            mc.setAttr(mirrorSide+'.rx',mc.getAttr(obj+'.rx'))
            mc.setAttr(mirrorSide+'.ry',mc.getAttr(obj+'.ry')*-1)
            mc.setAttr(mirrorSide+'.rz',mc.getAttr(obj+'.rz')*-1)
            
    mc.select(cl=True)
