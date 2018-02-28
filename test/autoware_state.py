import rospy
import smach
import smach_ros
from time import sleep


# State Category
class Start(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['started_system'])

    def execute(self, ud):
        sleep(1)
        return 'started_system'

class InitSystem(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['end_init_system', 'got_emergency'] )

    def execute(self, ud):
        sleep(1)
        return 'end_init_system'

class DriveStart(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['to_acceleration', 'to_deceleration', 'to_stop'])

    def execute(self, ud):
        sleep(1)
        return 'to_acceleration'

class DriveJudgeArea(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['is_normallane', 'is_intersection'])
    def execute(self,ud):
        return 'is_normallane'

class DriveAreaNormalLanePursuit(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['into_intersection_out'])
    def execute(self, ud):
        sleep(0.3)
        return 'into_intersection_out'

class DriveAreaIntersectionTurnLeft(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['into_normallane_out'])
    def execute(self, ud):
        sleep(0.3)
        return 'into_normallane_out'

class GoalMission(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['restart_mission','end_mission'])
    def execute(self, ud):
        sleep(1)
        return 'end_mission'

class EmergencyCheck(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['CauseUnknown', 'CauseKnown'])
    def execute(self, ud):
        sleep(1)
        return 'CauseKnown'


