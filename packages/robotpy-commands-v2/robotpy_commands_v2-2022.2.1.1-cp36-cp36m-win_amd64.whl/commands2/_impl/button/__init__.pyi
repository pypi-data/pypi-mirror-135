import commands2._impl.button
import typing
import _pyntcore._ntcore
import commands2._impl
import wpilib.interfaces._interfaces

__all__ = [
    "Button",
    "JoystickButton",
    "NetworkButton",
    "POVButton"
]


class Button(commands2._impl.Trigger):
    """
    A class used to bind command scheduling to button presses.  Can be composed
    with other buttons with the operators in Trigger.

    @see Trigger
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Create a new button that is pressed when the given condition is true.

        :param isPressed: Whether the button is pressed.

        Create a new button that is pressed active (default constructor) - activity
        can be further determined by subclass code.
        """
    @typing.overload
    def __init__(self, isPressed: typing.Callable[[], bool]) -> None: ...
    def cancelWhenPressed(self, command: commands2._impl.Command) -> Button: 
        """
        Binds a command to be canceled when the button is pressed.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        and scheduling of the command.

        :param command: The command to bind.

        :returns: The button, for chained calls.
        """
    def toggleWhenPressed(self, command: commands2._impl.Command, interruptible: bool = True) -> Button: 
        """
        Binds a command to start when the button is pressed, and be canceled when
        it is pressed again.  Takes a raw pointer, and so is non-owning; users are
        responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The button, for chained calls.
        """
    def whenHeld(self, command: commands2._impl.Command, interruptible: bool = True) -> Button: 
        """
        Binds a command to be started when the button is pressed, and canceled
        when it is released.  Takes a raw pointer, and so is non-owning; users are
        responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The button, for chained calls.
        """
    @typing.overload
    def whenPressed(self, command: commands2._impl.Command, interruptible: bool = True) -> Button: 
        """
        Binds a command to start when the button is pressed.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.

        Binds a runnable to execute when the button is pressed.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whenPressed(self, toRun: typing.Callable[[], None], requirements: typing.List[commands2._impl.Subsystem] = []) -> Button: ...
    @typing.overload
    def whenReleased(self, command: commands2._impl.Command, interruptible: bool = True) -> Button: 
        """
        Binds a command to start when the button is released.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The button, for chained calls.

        Binds a runnable to execute when the button is released.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whenReleased(self, toRun: typing.Callable[[], None], requirements: typing.List[commands2._impl.Subsystem] = []) -> Button: ...
    @typing.overload
    def whileHeld(self, command: commands2._impl.Command, interruptible: bool = True) -> Button: 
        """
        Binds a command to be started repeatedly while the button is pressed, and
        canceled when it is released.  Takes a raw pointer, and so is non-owning;
        users are responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The button, for chained calls.

        Binds a runnable to execute repeatedly while the button is pressed.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whileHeld(self, toRun: typing.Callable[[], None], requirements: typing.List[commands2._impl.Subsystem] = []) -> Button: ...
    pass
class JoystickButton(Button, commands2._impl.Trigger):
    """
    A class used to bind command scheduling to joystick button presses.  Can be
    composed with other buttons with the operators in Trigger.

    @see Trigger
    """
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, buttonNumber: int) -> None: 
        """
        Creates a JoystickButton that commands can be bound to.

        :param joystick:     The joystick on which the button is located.
        :param buttonNumber: The number of the button on the joystic.
        """
    pass
class NetworkButton(Button, commands2._impl.Trigger):
    """
    A Button that uses a NetworkTable boolean field.
    """
    @typing.overload
    def __init__(self, entry: _pyntcore._ntcore.NetworkTableEntry) -> None: 
        """
        Creates a NetworkButton that commands can be bound to.

        :param entry: The entry that is the value.

        Creates a NetworkButton that commands can be bound to.

        :param table: The table where the networktable value is located.
        :param field: The field that is the value.

        Creates a NetworkButton that commands can be bound to.

        :param table: The table where the networktable value is located.
        :param field: The field that is the value.
        """
    @typing.overload
    def __init__(self, table: _pyntcore._ntcore.NetworkTable, field: str) -> None: ...
    @typing.overload
    def __init__(self, table: str, field: str) -> None: ...
    pass
class POVButton(Button, commands2._impl.Trigger):
    """
    A class used to bind command scheduling to joystick POV presses.  Can be
    composed with other buttons with the operators in Trigger.

    @see Trigger
    """
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, angle: int, povNumber: int = 0) -> None: 
        """
        Creates a POVButton that commands can be bound to.

        :param joystick:  The joystick on which the button is located.
        :param angle:     The angle of the POV corresponding to a button press.
        :param povNumber: The number of the POV on the joystick.
        """
    pass
