#!/usr/bin/env python3
import commands2.button
import wpilib

from commands.arm.go_to_angle import GoToAngle
from subsystems.arm import Arm


class MyRobot(wpilib.TimedRobot):
    """Main robot class."""

    def robotInit(self):
        """Robot-wide initialization code should go here."""
        self.lstick = wpilib.Joystick(0)
        self.motor = wpilib.Talon(3)

        self.timer = wpilib.Timer()
        self.loops = 0

        self.arm = Arm(0)

    def autonomousInit(self):
        """Called only at the beginning of autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """Called every 20ms in autonomous mode."""
        pass

    def disabledInit(self):
        """Called only at the beginning of disabled mode."""
        self.logger.info("%d loops / %f seconds", self.loops, self.timer.get())

    def disabledPeriodic(self):
        """Called every 20ms in disabled mode."""
        pass

    def teleopInit(self):
        """Called only at the beginning of teleoperated mode."""
        self.loops = 0
        self.timer.reset()
        self.timer.start()

        commands2.button.JoystickButton(self.lstick, 1).whenPressed(
            GoToAngle(10, self.arm)
        )

        commands2.button.JoystickButton(self.lstick, 1).whenPressed(
            GoToAngle(50, self.arm)
        )

    def teleopPeriodic(self):
        """Called every 20ms in teleoperated mode"""
        # Move a motor with a Joystick
        self.motor.set(self.lstick.getY())

        # Print out the number of loop iterations passed every second
        self.loops += 1
        if self.timer.advanceIfElapsed(1):
            self.logger.info("%d loops / second", self.loops)
            self.loops = 0


if __name__ == "__main__":
    wpilib.run(MyRobot)
