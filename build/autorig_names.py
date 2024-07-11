# Description: This file contains the names of the joints and locators that will be created by the autorig script.

def jointList ():
    spine = ['C_pelvis_JNT', 'C_spine01_JNT', 'C_spine02_JNT', 'C_spine03_JNT','C_neck_JNT', 'C_head_JNT', 'C_headTop_JNT']
    arm_left = ['L_clavicle_JNT', 'L_upperarm_JNT', 'L_lowerarm_JNT', 'L_hand_JNT']
    arm_right = ['R_clavicle_JNT', 'R_upperarm_JNT', 'R_lowerarm_JNT', 'R_hand_JNT']
    leg_left = ['L_thigh_JNT', 'L_calf_JNT', 'L_foot_JNT','L_toe_JNT', 'L_toeEnd_JNT']
    leg_right = ['R_thigh_JNT', 'R_calf_JNT', 'R_foot_JNT','R_toe_JNT', 'R_toeEnd_JNT']
    thumb_left = ['L_thumb01_JNT', 'L_thumb02_JNT', 'L_thumb03_JNT']
    thumb_right = ['R_thumb01_JNT', 'R_thumb02_JNT', 'R_thumb03_JNT']
    index_left = ['L_index01_JNT', 'L_index02_JNT', 'L_index03_JNT']
    index_right = ['R_index01_JNT', 'R_index02_JNT', 'R_index03_JNT']
    middle_left = ['L_middle01_JNT', 'L_middle02_JNT', 'L_middle03_JNT']
    middle_right = ['R_middle01_JNT', 'R_middle02_JNT', 'R_middle03_JNT']
    ring_left = ['L_ring01_JNT', 'L_ring02_JNT', 'L_ring03_JNT']
    ring_right = ['R_ring01_JNT', 'R_ring02_JNT', 'R_ring03_JNT']
    pinky_left = ['L_pinky01_JNT', 'L_pinky02_JNT', 'L_pinky03_JNT']
    pinky_right = ['R_pinky01_JNT', 'R_pinky02_JNT', 'R_pinky03_JNT']
    
    return spine, arm_left, arm_right, leg_left, leg_right, thumb_left, thumb_right, index_left, index_right, middle_left, middle_right, ring_left, ring_right, pinky_left, pinky_right


def locList():
    spine = ['C_pelvis_LOC', 'C_spine01_LOC', 'C_spine02_LOC', 'C_spine03_LOC','C_neck_LOC', 'C_head_LOC', 'C_headTop_LOC']
    arm_left = ['L_clavicle_LOC', 'L_upperarm_LOC', 'L_lowerarm_LOC', 'L_hand_LOC']
    arm_right = ['R_clavicle_LOC', 'R_upperarm_LOC', 'R_lowerarm_LOC', 'R_hand_LOC']
    leg_left = ['L_thigh_LOC', 'L_calf_LOC', 'L_foot_LOC','L_toe_LOC', 'L_toeEnd_LOC']
    leg_right = ['R_thigh_LOC', 'R_calf_LOC', 'R_foot_LOC','R_toe_LOC', 'R_toeEnd_LOC']
    thumb_left = ['L_thumb01_LOC', 'L_thumb02_LOC', 'L_thumb03_LOC']
    thumb_right = ['R_thumb01_LOC', 'R_thumb02_LOC', 'R_thumb03_LOC']
    index_left = ['L_index01_LOC', 'L_index02_LOC', 'L_index03_LOC']
    index_right = ['R_index01_LOC', 'R_index02_LOC', 'R_index03_LOC']
    middle_left = ['L_middle01_LOC', 'L_middle02_LOC', 'L_middle03_LOC']
    middle_right = ['R_middle01_LOC', 'R_middle02_LOC', 'R_middle03_LOC']
    ring_left = ['L_ring01_LOC', 'L_ring02_LOC', 'L_ring03_LOC']
    ring_right = ['R_ring01_LOC', 'R_ring02_LOC', 'R_ring03_LOC']
    pinky_left = ['L_pinky01_LOC', 'L_pinky02_LOC', 'L_pinky03_LOC']
    pinky_right = ['R_pinky01_LOC', 'R_pinky02_LOC', 'R_pinky03_LOC']
    leg_left_roll = ['L_RevCBank_LOC', 'L_RevEBank_LOC', 'L_RevHeel_LOC']
    leg_right_roll = ['R_RevCBank_LOC', 'R_RevEBank_LOC', 'R_RevHeel_LOC']
    
    return spine, arm_left, arm_right, leg_left, leg_right, thumb_left, thumb_right, index_left, index_right, middle_left, middle_right, ring_left, ring_right, pinky_left, pinky_right, leg_left_roll, leg_right_roll    
    