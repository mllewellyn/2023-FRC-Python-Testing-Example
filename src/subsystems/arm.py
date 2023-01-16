import commands2
from rev._rev import CANSparkMax, SparkMaxPIDController


class Arm(commands2.SubsystemBase):
    def __init__(self, neo_id: int):
        # Type hints like this are not required (or enforced) but they enable the pycharm
        # autocomplete to work and let the precompiler catch some syntax errors as you type them
        self.neo: CANSparkMax = CANSparkMax(neo_id, CANSparkMax.MotorType.kBrushless)
        self.neo_pid_controller: SparkMaxPIDController = self.neo.getPIDController()
        self.neo_pid_controller.setP(1)

        self.encoder = self.neo.getEncoder()
        super().__init__()

    def set_angle(self, angle: float) -> None:
        target_sensor_units = self._convert_angle_to_sensor_unit(angle)
        self.neo_pid_controller.setReference(
            target_sensor_units, CANSparkMax.ControlType.kPosition
        )

    def get_angle(self) -> float:
        return _convert_sensor_unit_to_angle(self.encoder.getPosition())

    def get_angular_velocity(self) -> float:
        return _convert_sensor_unit_to_angle(self.encoder.getVelocity())


# Bonus question! How would the tests need to change if we made this
# a method of the Arm object instead of a static method? What are the reasons we would want to
# choose one or the other?
def _convert_angle_to_sensor_unit(angle: float) -> float:
    """
    :param angle: Angle in degrees from horizontal. The arm is facing forward at 0 degrees, backwards at 180 degrees.
    :return: The sensor unit reading that correspond to that arm angle.
    """
    # silly example
    return 7407.0 * angle


def _convert_sensor_unit_to_angle(sensor_units: float) -> float:
    """
    :param sensor_units:
    :return: Angle in degrees from horizontal. The arm is facing forward at 0 degrees, backwards at 180 degrees.
    """
    # silly example
    return sensor_units / 7407.0
