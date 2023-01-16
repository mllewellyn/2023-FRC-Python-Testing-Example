from unittest.mock import MagicMock

import pytest

from subsystems.arm import (
    _convert_sensor_unit_to_angle,
    _convert_angle_to_sensor_unit,
    Arm,
)


# We'll start with a simple example of a unit test before we get into the more complicated example of testing the arm.


def test_unit_conversion() -> None:
    # This is a very simple test used to show how a test should run

    # Step 1: Setup
    input = 1
    expected_output = 7407

    # Step 2: Action
    actual_output = _convert_angle_to_sensor_unit(input)

    # Step 3: Check the results
    assert expected_output == actual_output


# TODO show off parameterized tests
# https://docs.pytest.org/en/6.2.x/parametrize.html


# While it's possible to use a simulated neo controller. I want to show you how to
# perform unit testing without relying on a 3rd party library. We are going to
# mock the neo using MagicMock.
# Since we need to setup an instance of an arm object with a mocked out neo for each test we can
# use a pytest fixture to help us make our code less redundant and cleaner.
# How does this all get connected together at test runtime? Well pytest does some fancy stuff
# automatically for now we'll just trust that it will get setup.


@pytest.fixture
def arm() -> Arm:
    # We hope nothing breaks during setup because there's no SparkMax to connect to.
    # This seems to be working for now but don't take how I setup these mocks using monkey patching as gospel.
    # Typically, I would use patch but right now I'm just trying to get this done.
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    arm = Arm(1)
    # MagicMock is a very cool piece of software that will automatically keep track of what
    # methods are called on it so we can assert things about them later on.
    arm.neo = MagicMock()
    arm.neo_pid_controller = MagicMock()
    arm.encoder = MagicMock()
    return arm


def test_arm_set_angle(arm: Arm):
    # No setup

    # Action
    arm.set_angle(25)

    # Assertion
    # I am breaking these out for clarity to new programmers and to tell PyCharm that are
    # these objects are magic mocks because I'm addicted to autocomplete
    mock_pid_controller: MagicMock = arm.neo_pid_controller
    # When setReference was called on the MagicMock, since there was no existing setReference attribute of the mock,
    # it "magically" created one, which is another instance of MagicMock. In a less flexible language like Java we
    # would have had to specify all the methods we wanted to mock out explicitly.
    set_reference_mock: MagicMock = mock_pid_controller.setReference
    set_reference_mock.assert_called_once()


def test_arm_get_angle(arm: Arm):
    # Setup
    # We need to mock out the return value for the encoder
    test_encoder_value = 7407
    encoder_get_position_mock: MagicMock = arm.encoder.getPosition
    encoder_get_position_mock.return_value = test_encoder_value

    # Action
    actual = arm.get_angle()

    # Assertion
    expected = _convert_sensor_unit_to_angle(test_encoder_value)
    assert actual == expected
