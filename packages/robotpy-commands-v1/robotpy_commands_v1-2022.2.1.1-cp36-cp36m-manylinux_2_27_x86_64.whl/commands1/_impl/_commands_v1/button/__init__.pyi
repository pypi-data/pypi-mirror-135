import commands1._impl._commands_v1.button
import typing
import _pyntcore._ntcore
import commands1._impl._commands_v1.command
import wpilib.interfaces._interfaces
import wpiutil._wpiutil

__all__ = [
    "Button",
    "ButtonScheduler",
    "CancelButtonScheduler",
    "HeldButtonScheduler",
    "InternalButton",
    "JoystickButton",
    "NetworkButton",
    "POVButton",
    "PressedButtonScheduler",
    "ReleasedButtonScheduler",
    "ToggleButtonScheduler",
    "Trigger"
]


class Trigger(wpiutil._wpiutil.Sendable):
    """
    This class provides an easy way to link commands to inputs.

    It is very easy to link a polled input to a command. For instance, you could
    link the trigger button of a joystick to a "score" command or an encoder
    reaching a particular value.

    It is encouraged that teams write a subclass of Trigger if they want to have
    something unusual (for instance, if they want to react to the user holding
    a button while the robot is reading a certain sensor input). For this, they
    only have to write the Trigger::Get() method to get the full functionality of
    the Trigger class.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self) -> None: ...
    def cancelWhenActive(self, command: commands1._impl._commands_v1.command.Command) -> None: ...
    def get(self) -> bool: ...
    def grab(self) -> bool: ...
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def toggleWhenActive(self, command: commands1._impl._commands_v1.command.Command) -> None: ...
    def whenActive(self, command: commands1._impl._commands_v1.command.Command) -> None: ...
    def whenInactive(self, command: commands1._impl._commands_v1.command.Command) -> None: ...
    def whileActive(self, command: commands1._impl._commands_v1.command.Command) -> None: ...
    pass
class ButtonScheduler():
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    def start(self) -> None: ...
    @property
    def _m_button(self) -> Trigger:
        """
        :type: Trigger
        """
    @property
    def _m_command(self) -> commands1._impl._commands_v1.command.Command:
        """
        :type: commands1._impl._commands_v1.command.Command
        """
    @property
    def _m_pressedLast(self) -> bool:
        """
        :type: bool
        """
    @_m_pressedLast.setter
    def _m_pressedLast(self, arg0: bool) -> None:
        pass
    pass
class CancelButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    pass
class HeldButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    pass
class Button(Trigger, wpiutil._wpiutil.Sendable):
    """
    This class provides an easy way to link commands to OI inputs.

    It is very easy to link a button to a command.  For instance, you could link
    the trigger button of a joystick to a "score" command.

    This class represents a subclass of Trigger that is specifically aimed at
    buttons on an operator interface as a common use case of the more generalized
    Trigger objects. This is a simple wrapper around Trigger with the method
    names renamed to fit the Button object use.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self) -> None: ...
    def cancelWhenPressed(self, command: commands1._impl._commands_v1.command.Command) -> None: 
        """
        Cancels the specificed command when the button is pressed.

        :param command: The command to be canceled
        """
    def toggleWhenPressed(self, command: commands1._impl._commands_v1.command.Command) -> None: 
        """
        Toggle the specified command when the button is pressed.

        :param command: The command to be toggled
        """
    def whenPressed(self, command: commands1._impl._commands_v1.command.Command) -> None: 
        """
        Specifies the command to run when a button is first pressed.

        :param command: The pointer to the command to run
        """
    def whenReleased(self, command: commands1._impl._commands_v1.command.Command) -> None: 
        """
        Specifies the command to run when the button is released.

        The command will be scheduled a single time.

        :param command: The pointer to the command to run
        """
    def whileHeld(self, command: commands1._impl._commands_v1.command.Command) -> None: 
        """
        Specifies the command to be scheduled while the button is pressed.

        The command will be scheduled repeatedly while the button is pressed and
        will be canceled when the button is released.

        :param command: The pointer to the command to run
        """
    pass
class JoystickButton(Button, Trigger, wpiutil._wpiutil.Sendable):
    """
    A Button} that gets its state from a GenericHID.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, buttonNumber: int) -> None: ...
    def get(self) -> bool: ...
    pass
class NetworkButton(Button, Trigger, wpiutil._wpiutil.Sendable):
    """
    A that uses a NetworkTable boolean field.

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self, table: _pyntcore._ntcore.NetworkTable, field: str) -> None: ...
    @typing.overload
    def __init__(self, tableName: str, field: str) -> None: ...
    def get(self) -> bool: ...
    pass
class POVButton(Button, Trigger, wpiutil._wpiutil.Sendable):
    """
    A Button that gets its state from a POV on a GenericHID.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, angle: int, povNumber: int = 0) -> None: 
        """
        Creates a POV button for triggering commands.

        :param joystick:  The GenericHID object that has the POV
        :param angle:     The desired angle in degrees (e.g. 90, 270)
        :param povNumber: The POV number (@see GenericHID#GetPOV)
        """
    def get(self) -> bool: ...
    pass
class PressedButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    pass
class ReleasedButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    pass
class ToggleButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: commands1._impl._commands_v1.command.Command) -> None: ...
    def execute(self) -> None: ...
    pass
class InternalButton(Button, Trigger, wpiutil._wpiutil.Sendable):
    """
    This Button is intended to be used within a program. The programmer can
    manually set its value. Also includes a setting for whether or not it should
    invert its value.

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, inverted: bool) -> None: ...
    def get(self) -> bool: ...
    def setInverted(self, inverted: bool) -> None: ...
    def setPressed(self, pressed: bool) -> None: ...
    pass
