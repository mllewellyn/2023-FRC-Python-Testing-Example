import commands2

from subsystems.arm import Arm


class GoToAngle(commands2.CommandBase):
    def __init__(self, target_angle: float, arm: Arm, angle_tolerance: float = 2):
        self.arm = arm
        self.target_angle = self.target_angle
        self.angle_tolerance = angle_tolerance
        self.addRequirements(arm)

    def initialize(self) -> None:
        self.arm.set_angle(self.target_angle)
        # If we wanted to do something fancy like disengage a disk break but wait
        # for the break to be disengaged before trying to move the arm we could start a
        # timer here and then check it in execute.

    def execute(self) -> None:
        # Do nothing since the SparkMax is running the PID
        pass

    def end(self, interrupted: bool) -> None:
        # Engage the disk break
        pass

    def isFinished(self) -> bool:
        return abs(self.target_angle - self.arm.get_angle()) <= self.angle_tolerance
