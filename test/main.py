#!/usr/bin/env python

import sys
import rospy
import smach
import smach_ros
from time import sleep

import autoware_state


def main():
    rospy.init_node('autoware_state_machine')

    sm_top = smach.StateMachine(outcomes=['finished_system'])

    with sm_top:
        smach.StateMachine.add('START', autoware_state.Start(), transitions={'started_system':'INIT'})

        sm_init = smach.StateMachine(outcomes=['end_init', 'into_emergency'])
        sm_drive = smach.StateMachine(outcomes=['end_drive', 'into_emergency'])


        sm_goal = smach.StateMachine(outcomes=['end','restart'])
        sm_emergency = smach.StateMachine(outcomes=['solved_emergency'])

        with sm_init:
            smach.StateMachine.add('INIT_SYSTEM', autoware_state.InitSystem(), transitions={'end_init_system':'end_init',
                                                                             'got_emergency': 'into_emergency'})

        with sm_drive:
            smach.StateMachine.add('DRIVE_JUDGEAREA', autoware_state.DriveJudgeArea(),
                                   transitions={'is_normallane':'DRIVE_AREA_NORMALLANE',
                                                'is_intersection':'DRIVE_AREA_INTERSECTION'})

            sm_drive_area_normallane = smach.StateMachine(outcomes=['into_intersection_in'])
            sm_drive_area_intersection = smach.StateMachine(outcomes=['into_normallane_in'])

            with sm_drive_area_normallane:
                smach.StateMachine.add('DRIVE_AREA_NORMALLANE_PURSUIT', autoware_state.DriveAreaNormalLanePursuit(),
                                       transitions={'into_intersection_out': 'into_intersection_in'})

            with sm_drive_area_intersection:
                smach.StateMachine.add('DRIVE_AREA_INTERSECTION', autoware_state.DriveAreaIntersectionTurnLeft(),
                                       transitions={'into_normallane_out': 'into_normallane_in'})

            smach.StateMachine.add('DRIVE_AREA_NORMALLANE', sm_drive_area_normallane, transitions={'into_intersection_in':'DRIVE_AREA_INTERSECTION'})
            smach.StateMachine.add('DRIVE_AREA_INTERSECTION', sm_drive_area_intersection, transitions={'into_normallane_in':'DRIVE_AREA_NORMALLANE'})

        with sm_goal:
            smach.StateMachine.add('GOAL_MISSION', autoware_state.GoalMission(),transitions={'end_mission':'end',
                                                                                             'restart_mission':'restart'})

        with sm_emergency:
            smach.StateMachine.add('EMERGENCY_CHECK', autoware_state.EmergencyCheck(), transitions={'CauseUnknown':'solved_emergency',
                                                                                     'CauseKnown':'solved_emergency'})

        smach.StateMachine.add('INIT', sm_init,
                           transitions={'end_init':'DRIVE',
                                        'into_emergency':'EMG'})
        smach.StateMachine.add('DRIVE', sm_drive,
                               transitions={'end_drive':'GOAL',
                                            'into_emergency':'EMG'})
        smach.StateMachine.add('GOAL', sm_goal,
                               transitions={'end':'finished_system',
                               'restart':'INIT'})
        smach.StateMachine.add('EMG', sm_emergency,
                               transitions={'solved_emergency':'INIT'})

    sis = smach_ros.IntrospectionServer('state_machine', sm_top, '/AW_SM_ROOT')
    sis.start()

    outcome = sm_top.execute()

if __name__ == '__main__':
    main()
