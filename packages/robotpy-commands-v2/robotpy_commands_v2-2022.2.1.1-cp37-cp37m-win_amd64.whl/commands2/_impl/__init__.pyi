from __future__ import annotations
import commands2._impl
import typing
import _pyntcore._ntcore
import wpilib._wpilib
import wpimath._controls._controls.controller
import wpimath._controls._controls.trajectory
import wpimath.geometry._geometry
import wpimath.kinematics._kinematics
import wpiutil._wpiutil

__all__ = [
    "Command",
    "CommandBase",
    "CommandGroupBase",
    "CommandScheduler",
    "CommandState",
    "ConditionalCommand",
    "FunctionalCommand",
    "InstantCommand",
    "MecanumControllerCommand",
    "NotifierCommand",
    "PIDCommand",
    "PIDSubsystem",
    "ParallelCommandGroup",
    "ParallelDeadlineGroup",
    "ParallelRaceGroup",
    "PerpetualCommand",
    "PrintCommand",
    "ProfiledPIDCommand",
    "ProfiledPIDSubsystem",
    "ProxyScheduleCommand",
    "RamseteCommand",
    "RunCommand",
    "ScheduleCommand",
    "SequentialCommandGroup",
    "StartEndCommand",
    "Subsystem",
    "SubsystemBase",
    "Swerve2ControllerCommand",
    "Swerve3ControllerCommand",
    "Swerve4ControllerCommand",
    "Swerve6ControllerCommand",
    "TimedCommandRobot",
    "TrapezoidProfileCommand",
    "TrapezoidProfileCommandRadians",
    "TrapezoidProfileSubsystem",
    "TrapezoidProfileSubsystemRadians",
    "Trigger",
    "WaitCommand",
    "WaitUntilCommand",
    "button",
    "requirementsDisjoint"
]


class Command():
    """
    A state machine representing a complete action to be performed by the robot.
    Commands are run by the CommandScheduler, and can be composed into
    CommandGroups to allow users to build complicated multi-step actions without
    the need to roll the state machine logic themselves.

    Commands are run synchronously from the main robot loop; no multithreading
    is used, unless specified explicitly from the command implementation.

    @see CommandScheduler
    """
    def __init__(self) -> None: ...
    def alongWith(self, *args) -> ParallelCommandGroup: 
        """
        Decorates this command with a set of commands to run parallel to it, ending when the last
        command ends. Often more convenient/less-verbose than constructing a new
        ParallelCommandGroup explicitly.

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    @typing.overload
    def andThen(self, *args) -> SequentialCommandGroup: 
        """
        Decorates this command with a runnable to run after the command finishes.

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue

        Decorates this command with a set of commands to run after it in sequence. Often more
        convenient/less-verbose than constructing a new :class:`.SequentialCommandGroup` explicitly.

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    @typing.overload
    def andThen(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> SequentialCommandGroup: ...
    def asProxy(self) -> ProxyScheduleCommand: 
        """
        Decorates this command to run "by proxy" by wrapping it in a
        ProxyScheduleCommand. This is useful for "forking off" from command groups
        when the user does not wish to extend the command's requirements to the
        entire command group.

        :returns: the decorated command

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def beforeStarting(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> SequentialCommandGroup: 
        """
        Decorates this command with a runnable to run before this command starts.

        :param toRun:        the Runnable to run
        :param requirements: the required subsystems

        :returns: the decorated command

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def cancel(self) -> None: 
        """
        Cancels this command.  Will call the command's interrupted() method.
        Commands will be canceled even if they are not marked as interruptible.
        """
    def deadlineWith(self, *args) -> ParallelDeadlineGroup: 
        """
        Decorates this command with a set of commands to run parallel to it, ending when the calling
        command ends and interrupting all the others. Often more convenient/less-verbose than
        constructing a new :class:`.ParallelDeadlineGroup` explicitly.

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def end(self, interrupted: bool) -> None: 
        """
        The action to take when the command ends.  Called when either the command
        finishes normally, or when it interrupted/canceled.

        :param interrupted: whether the command was interrupted/canceled
        """
    def execute(self) -> None: 
        """
        The main body of a command.  Called repeatedly while the command is
        scheduled.
        """
    def getName(self) -> str: ...
    def getRequirements(self) -> typing.Set[Subsystem]: 
        """
        Specifies the set of subsystems used by this command.  Two commands cannot
        use the same subsystem at the same time.  If the command is scheduled as
        interruptible and another command is scheduled that shares a requirement,
        the command will be interrupted.  Else, the command will not be scheduled.
        If no subsystems are required, return an empty set.

        Note: it is recommended that user implementations contain the
        requirements as a field, and return that field here, rather than allocating
        a new set every time this is called.

        :returns: the set of subsystems that are required
        """
    def hasRequirement(self, requirement: Subsystem) -> bool: 
        """
        Whether the command requires a given subsystem.  Named "HasRequirement"
        rather than "requires" to avoid confusion with Command::Requires(Subsystem)
        -- this may be able to be changed in a few years.

        :param requirement: the subsystem to inquire about

        :returns: whether the subsystem is required
        """
    def initialize(self) -> None: 
        """
        The initial subroutine of a command.  Called once when the command is
        initially scheduled.
        """
    def isFinished(self) -> bool: 
        """
        Whether the command has finished.  Once a command finishes, the scheduler
        will call its end() method and un-schedule it.

        :returns: whether the command has finished.
        """
    def isGrouped(self) -> bool: 
        """
        Whether the command is currently grouped in a command group.  Used as extra
        insurance to prevent accidental independent use of grouped commands.
        """
    def isScheduled(self) -> bool: 
        """
        Whether or not the command is currently scheduled.  Note that this does not
        detect whether the command is being run by a CommandGroup, only whether it
        is directly being run by the scheduler.

        :returns: Whether the command is scheduled.
        """
    def perpetually(self) -> PerpetualCommand: 
        """
        Decorates this command to run perpetually, ignoring its ordinary end
        conditions.  The decorated command can still be interrupted or canceled.

        :returns: the decorated command

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def raceWith(self, *args) -> ParallelRaceGroup: 
        """
        Decorates this command with a set of commands to run parallel to it, ending when the first
        command ends. Often more convenient/less-verbose than constructing a new
        ParallelRaceGroup explicitly.

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def runsWhenDisabled(self) -> bool: 
        """
        Whether the given command should run when the robot is disabled.  Override
        to return true if the command should run when disabled.

        :returns: whether the command should run when the robot is disabled
        """
    @typing.overload
    def schedule(self) -> None: 
        """
        Schedules this command.

        :param interruptible: whether this command can be interrupted by another
                              command that shares one of its requirements

        Schedules this command, defaulting to interruptible.
        """
    @typing.overload
    def schedule(self, interruptible: bool) -> None: ...
    def setGrouped(self, grouped: bool) -> None: 
        """
        Sets whether the command is currently grouped in a command group.  Can be
        used to "reclaim" a command if a group is no longer going to use it.  NOT
        ADVISED!
        """
    def withInterrupt(self, condition: typing.Callable[[], bool]) -> ParallelRaceGroup: 
        """
        Decorates this command with an interrupt condition.  If the specified
        condition becomes true before the command finishes normally, the command
        will be interrupted and un-scheduled. Note that this only applies to the
        command returned by this method; the calling command is not itself changed.

        :param condition: the interrupt condition

        :returns: the command with the interrupt condition added

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    def withTimeout(self, duration: seconds) -> ParallelRaceGroup: 
        """
        Decorates this command with a timeout.  If the specified timeout is
        exceeded before the command finishes normally, the command will be
        interrupted and un-scheduled.  Note that the timeout only applies to the
        command returned by this method; the calling command is not itself changed.

        :param duration: the timeout duration

        :returns: the command with the timeout added

        Note: This decorator works by composing this command within a CommandGroup. The command
        cannot be used independently after being decorated, or be re-decorated with a different
        decorator, unless it is manually cleared from the list of grouped commands with Command.setGrouped(False)
        The decorated command can, however, be further decorated without issue
        """
    @property
    def _m_isGrouped(self) -> bool:
        """
        :type: bool
        """
    @_m_isGrouped.setter
    def _m_isGrouped(self, arg0: bool) -> None:
        pass
    pass
class CommandBase(Command, wpiutil._wpiutil.Sendable):
    """
    A Sendable base class for Commands.
    """
    def __init__(self) -> None: ...
    @typing.overload
    def addRequirements(self, *args) -> None: 
        """
        Adds the specified Subsystem requirements to the command.

        :param requirements: the Subsystem requirements to add

        Adds the specified Subsystem requirements to the command.

        :param requirements: the Subsystem requirements to add

        Adds the specified Subsystem requirement to the command.

        :param requirement: the Subsystem requirement to add
        """
    @typing.overload
    def addRequirements(self, requirement: Subsystem) -> None: ...
    @typing.overload
    def addRequirements(self, requirements: typing.List[Subsystem]) -> None: ...
    @typing.overload
    def addRequirements(self, requirements: typing.Set[Subsystem]) -> None: ...
    def getName(self) -> str: 
        """
        Gets the name of this Command.

        :returns: Name
        """
    def getRequirements(self) -> typing.Set[Subsystem]: 
        """
        Gets the Subsystem requirements of the command.

        :returns: the Command's Subsystem requirements
        """
    def getSubsystem(self) -> str: 
        """
        Gets the subsystem name of this Command.

        :returns: Subsystem name
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Command.

        :param name: name
        """
    def setSubsystem(self, subsystem: str) -> None: 
        """
        Sets the subsystem name of this Command.

        :param subsystem: subsystem name
        """
    @property
    def _m_requirements(self) -> typing.Set[Subsystem]:
        """
        :type: typing.Set[Subsystem]
        """
    pass
class CommandGroupBase(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A base for CommandGroups.  Statically tracks commands that have been
    allocated to groups to ensure those commands are not also used independently,
    which can result in inconsistent command state and unpredictable execution.
    """
    def __init__(self) -> None: ...
    def addCommands(self, commands: typing.List[Command]) -> None: 
        """
        Adds the given commands to the command group.

        :param commands: The commands to add.
        """
    @staticmethod
    @typing.overload
    def requireUngrouped(command: Command) -> bool: 
        """
        Requires that the specified command not have been already allocated to a
        CommandGroup. Reports an error if the command is already grouped.

        :param command: The command to check

        :returns: True if all the command is ungrouped.

        Requires that the specified command not have been already allocated to a
        CommandGroup. Reports an error if the command is already grouped.

        :param command: The command to check

        :returns: True if all the command is ungrouped.

        Requires that the specified commands not have been already allocated to a
        CommandGroup. Reports an error if any of the commands are already grouped.

        :param commands: The commands to check

        :returns: True if all the commands are ungrouped.
        """
    @staticmethod
    @typing.overload
    def requireUngrouped(commands: typing.List[Command]) -> bool: ...
    pass
class CommandScheduler(_pyntcore._ntcore.NTSendable, wpiutil._wpiutil.Sendable):
    """
    The scheduler responsible for running Commands.  A Command-based robot should
    call Run() on the singleton instance in its periodic block in order to run
    commands synchronously from the main loop.  Subsystems should be registered
    with the scheduler using RegisterSubsystem() in order for their Periodic()
    methods to be called and for their default commands to be scheduled.
    """
    def addButton(self, button: typing.Callable[[], None]) -> None: 
        """
        Adds a button binding to the scheduler, which will be polled to schedule
        commands.

        :param button: The button to add
        """
    @typing.overload
    def cancel(self, command: Command) -> None: 
        """
        Cancels commands. The scheduler will only call Command::End()
        method of the canceled command with true, indicating they were
        canceled (as opposed to finishing normally).

        Commands will be canceled even if they are not scheduled as
        interruptible.

        :param command: the command to cancel

        Cancels commands. The scheduler will only call Command::End()
        method of the canceled command with true, indicating they were
        canceled (as opposed to finishing normally).

        Commands will be canceled even if they are not scheduled as
        interruptible.

        :param commands: the commands to cancel
        """
    @typing.overload
    def cancel(self, commands: typing.List[Command]) -> None: ...
    def cancelAll(self) -> None: 
        """
        Cancels all commands that are currently scheduled.
        """
    def clearButtons(self) -> None: 
        """
        Removes all button bindings from the scheduler.
        """
    def disable(self) -> None: 
        """
        Disables the command scheduler.
        """
    def enable(self) -> None: 
        """
        Enables the command scheduler.
        """
    def getDefaultCommand(self, subsystem: Subsystem) -> Command: 
        """
        Gets the default command associated with this subsystem.  Null if this
        subsystem has no default command associated with it.

        :param subsystem: the subsystem to inquire about

        :returns: the default command associated with the subsystem
        """
    @staticmethod
    def getInstance() -> CommandScheduler: 
        """
        Returns the Scheduler instance.

        :returns: the instance
        """
    def initSendable(self, builder: _pyntcore._ntcore.NTSendableBuilder) -> None: ...
    @typing.overload
    def isScheduled(self, command: Command) -> bool: 
        """
        Whether the given commands are running.  Note that this only works on
        commands that are directly scheduled by the scheduler; it will not work on
        commands inside of CommandGroups, as the scheduler does not see them.

        :param commands: the command to query

        :returns: whether the command is currently scheduled

        Whether a given command is running.  Note that this only works on commands
        that are directly scheduled by the scheduler; it will not work on commands
        inside of CommandGroups, as the scheduler does not see them.

        :param command: the command to query

        :returns: whether the command is currently scheduled
        """
    @typing.overload
    def isScheduled(self, commands: typing.List[Command]) -> bool: ...
    def onCommandExecute(self, action: typing.Callable[[Command], None]) -> None: 
        """
        Adds an action to perform on the execution of any command by the scheduler.

        :param action: the action to perform
        """
    def onCommandFinish(self, action: typing.Callable[[Command], None]) -> None: 
        """
        Adds an action to perform on the finishing of any command by the scheduler.

        :param action: the action to perform
        """
    def onCommandInitialize(self, action: typing.Callable[[Command], None]) -> None: 
        """
        Adds an action to perform on the initialization of any command by the
        scheduler.

        :param action: the action to perform
        """
    def onCommandInterrupt(self, action: typing.Callable[[Command], None]) -> None: 
        """
        Adds an action to perform on the interruption of any command by the
        scheduler.

        :param action: the action to perform
        """
    @typing.overload
    def registerSubsystem(self, *args) -> None: 
        """
        Registers subsystems with the scheduler.  This must be called for the
        subsystem's periodic block to run when the scheduler is run, and for the
        subsystem's default command to be scheduled.  It is recommended to call
        this from the constructor of your subsystem implementations.

        :param subsystem: the subsystem to register
        """
    @typing.overload
    def registerSubsystem(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def registerSubsystem(self, subsystems: typing.List[Subsystem]) -> None: ...
    def requiring(self, subsystem: Subsystem) -> Command: 
        """
        Returns the command currently requiring a given subsystem.  Null if no
        command is currently requiring the subsystem

        :param subsystem: the subsystem to be inquired about

        :returns: the command currently requiring the subsystem
        """
    @staticmethod
    def resetInstance() -> None: 
        """
        python-specific: clear the global command scheduler instance
        """
    def run(self) -> None: 
        """
        Runs a single iteration of the scheduler.  The execution occurs in the
        following order:

        Subsystem periodic methods are called.

        Button bindings are polled, and new commands are scheduled from them.

        Currently-scheduled commands are executed.

        End conditions are checked on currently-scheduled commands, and commands
        that are finished have their end methods called and are removed.

        Any subsystems not being used as requirements have their default methods
        started.
        """
    @typing.overload
    def schedule(self, command: Command) -> None: 
        """
        Schedules a command for execution.  Does nothing if the command is already
        scheduled. If a command's requirements are not available, it will only be
        started if all the commands currently using those requirements have been
        scheduled as interruptible.  If this is the case, they will be interrupted
        and the command will be scheduled.

        :param interruptible: whether this command can be interrupted
        :param command:       the command to schedule

        Schedules a command for execution, with interruptible defaulted to true.
        Does nothing if the command is already scheduled.

        :param command: the command to schedule

        Schedules multiple commands for execution.  Does nothing if the command is
        already scheduled. If a command's requirements are not available, it will
        only be started if all the commands currently using those requirements have
        been scheduled as interruptible.  If this is the case, they will be
        interrupted and the command will be scheduled.

        :param interruptible: whether the commands should be interruptible
        :param commands:      the commands to schedule

        Schedules multiple commands for execution, with interruptible defaulted to
        true.  Does nothing if the command is already scheduled.

        :param commands: the commands to schedule
        """
    @typing.overload
    def schedule(self, commands: typing.List[Command]) -> None: ...
    @typing.overload
    def schedule(self, interruptible: bool, command: Command) -> None: ...
    @typing.overload
    def schedule(self, interruptible: bool, commands: typing.List[Command]) -> None: ...
    def setDefaultCommand(self, subsystem: Subsystem, defaultCommand: Command) -> None: 
        """
        Sets the default command for a subsystem.  Registers that subsystem if it
        is not already registered.  Default commands will run whenever there is no
        other command currently scheduled that requires the subsystem.  Default
        commands should be written to never end (i.e. their IsFinished() method
        should return false), as they would simply be re-scheduled if they do.
        Default commands must also require their subsystem.

        :param subsystem:      the subsystem whose default command will be set
        :param defaultCommand: the default command to associate with the subsystem
        """
    def setPeriod(self, period: seconds) -> None: 
        """
        Changes the period of the loop overrun watchdog. This should be kept in
        sync with the TimedRobot period.
        """
    def timeSinceScheduled(self, command: Command) -> seconds: 
        """
        Returns the time since a given command was scheduled.  Note that this only
        works on commands that are directly scheduled by the scheduler; it will not
        work on commands inside of commandgroups, as the scheduler does not see
        them.

        :param command: the command to query

        :returns: the time since the command was scheduled
        """
    @typing.overload
    def unregisterSubsystem(self, *args) -> None: 
        """
        Un-registers subsystems with the scheduler.  The subsystem will no longer
        have its periodic block called, and will not have its default command
        scheduled.

        :param subsystem: the subsystem to un-register
        """
    @typing.overload
    def unregisterSubsystem(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def unregisterSubsystem(self, subsystems: typing.List[Subsystem]) -> None: ...
    pass
class CommandState():
    """
    Class that holds scheduling state for a command.  Used internally by the
    CommandScheduler
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, interruptible: bool) -> None: ...
    def isInterruptible(self) -> bool: ...
    def timeSinceInitialized(self) -> seconds: ...
    pass
class ConditionalCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    Runs one of two commands, depending on the value of the given condition when
    this command is initialized.  Does not actually schedule the selected command
    - rather, the command is run through this command; this ensures that the
    command will behave as expected if used as part of a CommandGroup.  Requires
    the requirements of both commands, again to ensure proper functioning when
    used in a CommandGroup.  If this is undesired, consider using
    ScheduleCommand.

    As this command contains multiple component commands within it, it is
    technically a command group; the command instances that are passed to it
    cannot be added to any other groups, or scheduled individually.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.

    @see ScheduleCommand
    """
    def __init__(self, onTrue: Command, onFalse: Command, condition: typing.Callable[[], bool]) -> None: 
        """
        Creates a new ConditionalCommand.

        :param onTrue:    the command to run if the condition is true
        :param onFalse:   the command to run if the condition is false
        :param condition: the condition to determine which command to run
        """
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
class FunctionalCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that allows the user to pass in functions for each of the basic
    command methods through the constructor.  Useful for inline definitions of
    complex commands - note, however, that if a command is beyond a certain
    complexity it is usually better practice to write a proper class for it than
    to inline it.
    """
    @typing.overload
    def __init__(self, arg0: typing.Callable[[], None], arg1: typing.Callable[[], None], arg2: typing.Callable[[bool], None], arg3: typing.Callable[[], bool], *args) -> None: 
        """
        Creates a new FunctionalCommand.

        :param onInit:       the function to run on command initialization
        :param onExecute:    the function to run on command execution
        :param onEnd:        the function to run on command end
        :param isFinished:   the function that determines whether the command has
                             finished
        :param requirements: the subsystems required by this command
        """
    @typing.overload
    def __init__(self, onInit: typing.Callable[[], None], onExecute: typing.Callable[[], None], onEnd: typing.Callable[[bool], None], isFinished: typing.Callable[[], bool], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class InstantCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A Command that runs instantly; it will initialize, execute once, and end on
    the same iteration of the scheduler.  Users can either pass in a Runnable and
    a set of requirements, or else subclass this command if desired.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new InstantCommand that runs the given Runnable with the given
        requirements.

        :param toRun:        the Runnable to run
        :param requirements: the subsystems required by this command

        Creates a new InstantCommand with a Runnable that does nothing.  Useful
        only as a no-arg constructor to call implicitly from subclass constructors.
        """
    @typing.overload
    def __init__(self, arg0: typing.Callable[[], None], *args) -> None: ...
    @typing.overload
    def __init__(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class MecanumControllerCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses two PID controllers (PIDController) and a profiled PID
    controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a
    mecanum drive.

    The command handles trajectory-following,
    Velocity PID calculations, and feedforwards internally. This
    is intended to be a more-or-less "complete solution" that can be used by
    teams without a great deal of controls expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw wheel speeds from the PID controllers.

    The robot angle controller does not follow the angle given by
    the trajectory but rather goes to the angle given in the final state of the
    trajectory.
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], feedforward: wpimath._controls._controls.controller.SimpleMotorFeedforwardMeters, kinematics: wpimath.kinematics._kinematics.MecanumDriveKinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], maxWheelVelocity: meters_per_second, currentWheelSpeeds: typing.Callable[[], wpimath.kinematics._kinematics.MecanumDriveWheelSpeeds], frontLeftController: wpimath._controls._controls.controller.PIDController, rearLeftController: wpimath._controls._controls.controller.PIDController, frontRightController: wpimath._controls._controls.controller.PIDController, rearRightController: wpimath._controls._controls.controller.PIDController, output: typing.Callable[[volts, volts, volts, volts], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new MecanumControllerCommand that when executed will follow
        the provided trajectory. PID control and feedforward are handled
        internally. Outputs are scaled from -12 to 12 as a voltage output to the
        motor.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:           The trajectory to follow.
        :param pose:                 A function that supplies the robot pose,
                                     provided by the odometry class.
        :param feedforward:          The feedforward to use for the drivetrain.
        :param kinematics:           The kinematics for the robot drivetrain.
        :param xController:          The Trajectory Tracker PID controller
                                     for the robot's x position.
        :param yController:          The Trajectory Tracker PID controller
                                     for the robot's y position.
        :param thetaController:      The Trajectory Tracker PID controller
                                     for angle for the robot.
        :param desiredRotation:      The angle that the robot should be facing.
                                     This is sampled at each time step.
        :param maxWheelVelocity:     The maximum velocity of a drivetrain wheel.
        :param frontLeftController:  The front left wheel velocity PID.
        :param rearLeftController:   The rear left wheel velocity PID.
        :param frontRightController: The front right wheel velocity PID.
        :param rearRightController:  The rear right wheel velocity PID.
        :param currentWheelSpeeds:   A MecanumDriveWheelSpeeds object containing
                                     the current wheel speeds.
        :param output:               The output of the velocity PIDs.
        :param requirements:         The subsystems to require.

        Constructs a new MecanumControllerCommand that when executed will follow
        the provided trajectory. PID control and feedforward are handled
        internally. Outputs are scaled from -12 to 12 as a voltage output to the
        motor.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        Note 2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:           The trajectory to follow.
        :param pose:                 A function that supplies the robot pose,
                                     provided by the odometry class.
        :param feedforward:          The feedforward to use for the drivetrain.
        :param kinematics:           The kinematics for the robot drivetrain.
        :param xController:          The Trajectory Tracker PID controller
                                     for the robot's x position.
        :param yController:          The Trajectory Tracker PID controller
                                     for the robot's y position.
        :param thetaController:      The Trajectory Tracker PID controller
                                     for angle for the robot.
        :param maxWheelVelocity:     The maximum velocity of a drivetrain wheel.
        :param frontLeftController:  The front left wheel velocity PID.
        :param rearLeftController:   The rear left wheel velocity PID.
        :param frontRightController: The front right wheel velocity PID.
        :param rearRightController:  The rear right wheel velocity PID.
        :param currentWheelSpeeds:   A MecanumDriveWheelSpeeds object containing
                                     the current wheel speeds.
        :param output:               The output of the velocity PIDs.
        :param requirements:         The subsystems to require.

        Constructs a new MecanumControllerCommand that when executed will follow
        the provided trajectory. The user should implement a velocity PID on the
        desired output wheel velocities.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path - this is left to the user, since it is not
        appropriate for paths with non-stationary end-states.

        :param trajectory:       The trajectory to follow.
        :param pose:             A function that supplies the robot pose - use one
                                 of the odometry classes to provide this.
        :param kinematics:       The kinematics for the robot drivetrain.
        :param xController:      The Trajectory Tracker PID controller
                                 for the robot's x position.
        :param yController:      The Trajectory Tracker PID controller
                                 for the robot's y position.
        :param thetaController:  The Trajectory Tracker PID controller
                                 for angle for the robot.
        :param desiredRotation:  The angle that the robot should be facing.
                                 This is sampled at every time step.
        :param maxWheelVelocity: The maximum velocity of a drivetrain wheel.
        :param output:           The output of the position PIDs.
        :param requirements:     The subsystems to require.

        Constructs a new MecanumControllerCommand that when executed will follow
        the provided trajectory. The user should implement a velocity PID on the
        desired output wheel velocities.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path - this is left to the user, since it is not
        appropriate for paths with non-stationary end-states.

        Note2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:       The trajectory to follow.
        :param pose:             A function that supplies the robot pose - use one
                                 of the odometry classes to provide this.
        :param kinematics:       The kinematics for the robot drivetrain.
        :param xController:      The Trajectory Tracker PID controller
                                 for the robot's x position.
        :param yController:      The Trajectory Tracker PID controller
                                 for the robot's y position.
        :param thetaController:  The Trajectory Tracker PID controller
                                 for angle for the robot.
        :param maxWheelVelocity: The maximum velocity of a drivetrain wheel.
        :param output:           The output of the position PIDs.
        :param requirements:     The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], feedforward: wpimath._controls._controls.controller.SimpleMotorFeedforwardMeters, kinematics: wpimath.kinematics._kinematics.MecanumDriveKinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, maxWheelVelocity: meters_per_second, currentWheelSpeeds: typing.Callable[[], wpimath.kinematics._kinematics.MecanumDriveWheelSpeeds], frontLeftController: wpimath._controls._controls.controller.PIDController, rearLeftController: wpimath._controls._controls.controller.PIDController, frontRightController: wpimath._controls._controls.controller.PIDController, rearRightController: wpimath._controls._controls.controller.PIDController, output: typing.Callable[[volts, volts, volts, volts], None], requirements: typing.List[Subsystem] = []) -> None: ...
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.MecanumDriveKinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], maxWheelVelocity: meters_per_second, output: typing.Callable[[meters_per_second, meters_per_second, meters_per_second, meters_per_second], None], requirements: typing.List[Subsystem] = []) -> None: ...
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.MecanumDriveKinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, maxWheelVelocity: meters_per_second, output: typing.Callable[[meters_per_second, meters_per_second, meters_per_second, meters_per_second], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class NotifierCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that starts a notifier to run the given runnable periodically in a
    separate thread. Has no end condition as-is; either subclass it or use
    Command::WithTimeout(double) or Command::WithInterrupt(BooleanSupplier) to
    give it one.

    WARNING: Do not use this class unless you are confident in your ability to
    make the executed code thread-safe.  If you do not know what "thread-safe"
    means, that is a good sign that you should not use this class.
    """
    def __init__(self, toRun: typing.Callable[[], None], period: seconds, requirements: typing.List[Subsystem] = []) -> None: 
        """
        Creates a new NotifierCommand.

        :param toRun:        the runnable for the notifier to run
        :param period:       the period at which the notifier should run
        :param requirements: the subsystems required by this command
        """
    def end(self, interrupted: bool) -> None: ...
    def initialize(self) -> None: ...
    pass
class PIDCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that controls an output with a PIDController.  Runs forever by
    default - to add exit conditions and/or other behavior, subclass this class.
    The controller calculation and output are performed synchronously in the
    command's execute() method.

    @see PIDController
    """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.PIDController, measurementSource: typing.Callable[[], float], setpoint: float, useOutput: typing.Callable[[float], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Creates a new PIDCommand, which controls the given output with a
        PIDController.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param setpointSource:    the controller's reference (aka setpoint)
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command

        Creates a new PIDCommand, which controls the given output with a
        PIDController with a constant setpoint.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param setpoint:          the controller's setpoint (aka setpoint)
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command
        """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.PIDController, measurementSource: typing.Callable[[], float], setpointSource: typing.Callable[[], float], useOutput: typing.Callable[[float], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def getController(self) -> wpimath._controls._controls.controller.PIDController: 
        """
        Returns the PIDController used by the command.

        :returns: The PIDController
        """
    def initialize(self) -> None: ...
    @property
    def _controller(self) -> wpimath._controls._controls.controller.PIDController:
        """
        :type: wpimath._controls._controls.controller.PIDController
        """
    @property
    def _measurement(self) -> typing.Callable[[], float]:
        """
        :type: typing.Callable[[], float]
        """
    @_measurement.setter
    def _measurement(self, arg0: typing.Callable[[], float]) -> None:
        pass
    @property
    def _setpoint(self) -> typing.Callable[[], float]:
        """
        :type: typing.Callable[[], float]
        """
    @_setpoint.setter
    def _setpoint(self, arg0: typing.Callable[[], float]) -> None:
        pass
    @property
    def _useOutput(self) -> typing.Callable[[float], None]:
        """
        :type: typing.Callable[[float], None]
        """
    @_useOutput.setter
    def _useOutput(self, arg0: typing.Callable[[float], None]) -> None:
        pass
    pass
class Subsystem():
    """
    A robot subsystem.  Subsystems are the basic unit of robot organization in
    the Command-based framework; they encapsulate low-level hardware objects
    (motor controllers, sensors, etc) and provide methods through which they can
    be used by Commands.  Subsystems are used by the CommandScheduler's resource
    management system to ensure multiple robot actions are not "fighting" over
    the same hardware; Commands that use a subsystem should include that
    subsystem in their GetRequirements() method, and resources used within a
    subsystem should generally remain encapsulated and not be shared by other
    parts of the robot.

    Subsystems must be registered with the scheduler with the
    CommandScheduler.RegisterSubsystem() method in order for the
    Periodic() method to be called.  It is recommended that this method be called
    from the constructor of users' Subsystem implementations.  The
    SubsystemBase class offers a simple base for user implementations
    that handles this.

    @see Command
    @see CommandScheduler
    @see SubsystemBase
    """
    def __init__(self) -> None: ...
    def getCurrentCommand(self) -> Command: 
        """
        Returns the command currently running on this subsystem.  Returns null if
        no command is currently scheduled that requires this subsystem.

        :returns: the scheduled command currently requiring this subsystem
        """
    def getDefaultCommand(self) -> Command: 
        """
        Gets the default command for this subsystem.  Returns null if no default
        command is currently associated with the subsystem.

        :returns: the default command associated with this subsystem
        """
    def periodic(self) -> None: 
        """
        This method is called periodically by the CommandScheduler.  Useful for
        updating subsystem-specific state that you don't want to offload to a
        Command.  Teams should try to be consistent within their own codebases
        about which responsibilities will be handled by Commands, and which will be
        handled here.
        """
    def register(self) -> None: 
        """
        Registers this subsystem with the CommandScheduler, allowing its
        Periodic() method to be called when the scheduler runs.
        """
    def setDefaultCommand(self, defaultCommand: Command) -> None: 
        """
        Sets the default Command of the subsystem.  The default command will be
        automatically scheduled when no other commands are scheduled that require
        the subsystem. Default commands should generally not end on their own, i.e.
        their IsFinished() method should always return false.  Will automatically
        register this subsystem with the CommandScheduler.

        :param defaultCommand: the default command to associate with this subsystem
        """
    def simulationPeriodic(self) -> None: 
        """
        This method is called periodically by the CommandScheduler.  Useful for
        updating subsystem-specific state that needs to be maintained for
        simulations, such as for updating simulation classes and setting simulated
        sensor readings.
        """
    pass
class ParallelCommandGroup(CommandGroupBase, CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A CommandGroup that runs a set of commands in parallel, ending when the last
    command ends.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.
    """
    @typing.overload
    def __init__(self, *args) -> None: 
        """
        Creates a new ParallelCommandGroup.  The given commands will be executed
        simultaneously. The command group will finish when the last command
        finishes.  If the CommandGroup is interrupted, only the commands that are
        still running will be interrupted.

        :param commands: the commands to include in this group.

        Creates a new ParallelCommandGroup.  The given commands will be executed
        simultaneously. The command group will finish when the last command
        finishes.  If the CommandGroup is interrupted, only the commands that are
        still running will be interrupted.

        :param commands: the commands to include in this group.
        """
    @typing.overload
    def __init__(self, commands: typing.List[Command]) -> None: ...
    @typing.overload
    def addCommands(self, *args) -> None: ...
    @typing.overload
    def addCommands(self, commands: typing.List[Command]) -> None: ...
    def alongWith(self, *args) -> ParallelCommandGroup: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
class ParallelDeadlineGroup(CommandGroupBase, CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A CommandGroup that runs a set of commands in parallel, ending only when a
    specific command (the "deadline") ends, interrupting all other commands that
    are still running at that point.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.
    """
    @typing.overload
    def __init__(self, deadline: Command, *args) -> None: 
        """
        Creates a new ParallelDeadlineGroup.  The given commands (including the
        deadline) will be executed simultaneously.  The CommandGroup will finish
        when the deadline finishes, interrupting all other still-running commands.
        If the CommandGroup is interrupted, only the commands still running will be
        interrupted.

        :param deadline: the command that determines when the group ends
        :param commands: the commands to be executed

        Creates a new ParallelDeadlineGroup.  The given commands (including the
        deadline) will be executed simultaneously.  The CommandGroup will finish
        when the deadline finishes, interrupting all other still-running commands.
        If the CommandGroup is interrupted, only the commands still running will be
        interrupted.

        :param deadline: the command that determines when the group ends
        :param commands: the commands to be executed
        """
    @typing.overload
    def __init__(self, deadline: Command, commands: typing.List[Command]) -> None: ...
    @typing.overload
    def addCommands(self, *args) -> None: ...
    @typing.overload
    def addCommands(self, commands: typing.List[Command]) -> None: ...
    def deadlineWith(self, *args) -> ParallelDeadlineGroup: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
class ParallelRaceGroup(CommandGroupBase, CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A CommandGroup that runs a set of commands in parallel, ending when any one
    of the commands ends and interrupting all the others.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.
    """
    @typing.overload
    def __init__(self, *args) -> None: 
        """
        Creates a new ParallelCommandRace.  The given commands will be executed
        simultaneously, and will "race to the finish" - the first command to finish
        ends the entire command, with all other commands being interrupted.

        :param commands: the commands to include in this group.
        """
    @typing.overload
    def __init__(self, commands: typing.List[Command]) -> None: ...
    @typing.overload
    def addCommands(self, *args) -> None: ...
    @typing.overload
    def addCommands(self, commands: typing.List[Command]) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def raceWith(self, *args) -> ParallelRaceGroup: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
class PerpetualCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that runs another command in perpetuity, ignoring that command's
    end conditions.  While this class does not extend {@link CommandGroupBase},
    it is still considered a CommandGroup, as it allows one to compose another
    command within it; the command instances that are passed to it cannot be
    added to any other groups, or scheduled individually.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.
    """
    def __init__(self, command: Command) -> None: 
        """
        Creates a new PerpetualCommand.  Will run another command in perpetuity,
        ignoring that command's end conditions, unless this command itself is
        interrupted.

        :param command: the command to run perpetually
        """
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    pass
class PrintCommand(InstantCommand, CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that prints a string when initialized.
    """
    def __init__(self, message: str) -> None: 
        """
        Creates a new a PrintCommand.

        :param message: the message to print
        """
    def runsWhenDisabled(self) -> bool: ...
    pass
class ProfiledPIDCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that controls an output with a ProfiledPIDController.  Runs forever
    by default - to add exit conditions and/or other behavior, subclass this
    class. The controller calculation and output are performed synchronously in
    the command's execute() method.

    @see ProfiledPIDController<Distance>
    """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.ProfiledPIDController, measurementSource: typing.Callable[[], float], goal: float, useOutput: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Creates a new PIDCommand, which controls the given output with a
        ProfiledPIDController.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param goalSource:        the controller's goal
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command

        Creates a new PIDCommand, which controls the given output with a
        ProfiledPIDController.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param goalSource:        the controller's goal
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command

        Creates a new PIDCommand, which controls the given output with a
        ProfiledPIDController with a constant goal.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param goal:              the controller's goal
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command

        Creates a new PIDCommand, which controls the given output with a
        ProfiledPIDController with a constant goal.

        :param controller:        the controller that controls the output.
        :param measurementSource: the measurement of the process variable
        :param goal:              the controller's goal
        :param useOutput:         the controller's output
        :param requirements:      the subsystems required by this command
        """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.ProfiledPIDController, measurementSource: typing.Callable[[], float], goal: wpimath._controls._controls.trajectory.TrapezoidProfile.State, useOutput: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None], requirements: typing.List[Subsystem] = []) -> None: ...
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.ProfiledPIDController, measurementSource: typing.Callable[[], float], goalSource: typing.Callable[[], float], useOutput: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None], requirements: typing.List[Subsystem] = []) -> None: ...
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.ProfiledPIDController, measurementSource: typing.Callable[[], float], goalSource: typing.Callable[[], wpimath._controls._controls.trajectory.TrapezoidProfile.State], useOutput: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def getController(self) -> wpimath._controls._controls.controller.ProfiledPIDController: 
        """
        Returns the ProfiledPIDController used by the command.

        :returns: The ProfiledPIDController
        """
    def initialize(self) -> None: ...
    @property
    def _controller(self) -> wpimath._controls._controls.controller.ProfiledPIDController:
        """
        :type: wpimath._controls._controls.controller.ProfiledPIDController
        """
    @property
    def _goal(self) -> typing.Callable[[], wpimath._controls._controls.trajectory.TrapezoidProfile.State]:
        """
        :type: typing.Callable[[], wpimath._controls._controls.trajectory.TrapezoidProfile.State]
        """
    @_goal.setter
    def _goal(self, arg0: typing.Callable[[], wpimath._controls._controls.trajectory.TrapezoidProfile.State]) -> None:
        pass
    @property
    def _measurement(self) -> typing.Callable[[], float]:
        """
        :type: typing.Callable[[], float]
        """
    @_measurement.setter
    def _measurement(self, arg0: typing.Callable[[], float]) -> None:
        pass
    @property
    def _useOutput(self) -> typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None]:
        """
        :type: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None]
        """
    @_useOutput.setter
    def _useOutput(self, arg0: typing.Callable[[float, wpimath._controls._controls.trajectory.TrapezoidProfile.State], None]) -> None:
        pass
    pass
class SubsystemBase(Subsystem, wpiutil._wpiutil.Sendable):
    """
    A base for subsystems that handles registration in the constructor, and
    provides a more intuitive method for setting the default command.
    """
    def __init__(self) -> None: ...
    def addChild(self, name: str, child: wpiutil._wpiutil.Sendable) -> None: 
        """
        Associate a Sendable with this Subsystem.
        Also update the child's name.

        :param name:  name to give child
        :param child: sendable
        """
    def getName(self) -> str: 
        """
        Gets the name of this Subsystem.

        :returns: Name
        """
    def getSubsystem(self) -> str: 
        """
        Gets the subsystem name of this Subsystem.

        :returns: Subsystem name
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Subsystem.

        :param name: name
        """
    def setSubsystem(self, name: str) -> None: 
        """
        Sets the subsystem name of this Subsystem.

        :param name: subsystem name
        """
    pass
class ProxyScheduleCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    Schedules the given commands when this command is initialized, and ends when
    all the commands are no longer scheduled.  Useful for forking off from
    CommandGroups.  If this command is interrupted, it will cancel all of the
    commands.
    """
    @typing.overload
    def __init__(self, *args) -> None: 
        """
        Creates a new ProxyScheduleCommand that schedules the given commands when
        initialized, and ends when they are all no longer scheduled.

        :param toSchedule: the commands to schedule
        """
    @typing.overload
    def __init__(self, toSchedule: Command) -> None: ...
    @typing.overload
    def __init__(self, toSchedule: typing.List[Command]) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class RamseteCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses a RAMSETE controller  to follow a trajectory
    with a differential drive.

    The command handles trajectory-following, PID calculations, and
    feedforwards internally.  This is intended to be a more-or-less "complete
    solution" that can be used by teams without a great deal of controls
    expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw wheel speeds from the RAMSETE controller.

    @see RamseteController
    @see Trajectory
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], controller: wpimath._controls._controls.controller.RamseteController, feedforward: wpimath._controls._controls.controller.SimpleMotorFeedforwardMeters, kinematics: wpimath.kinematics._kinematics.DifferentialDriveKinematics, wheelSpeeds: typing.Callable[[], wpimath.kinematics._kinematics.DifferentialDriveWheelSpeeds], leftController: wpimath._controls._controls.controller.PIDController, rightController: wpimath._controls._controls.controller.PIDController, output: typing.Callable[[volts, volts], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new RamseteCommand that, when executed, will follow the
        provided trajectory. PID control and feedforward are handled internally,
        and outputs are scaled -12 to 12 representing units of volts.

        Note: The controller will *not* set the outputVolts to zero upon
        completion of the path - this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose - use one of
                                the odometry classes to provide this.
        :param controller:      The RAMSETE controller used to follow the
                                trajectory.
        :param feedforward:     A component for calculating the feedforward for the
                                drive.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param wheelSpeeds:     A function that supplies the speeds of the left
                                and right sides of the robot drive.
        :param leftController:  The PIDController for the left side of the robot
                                drive.
        :param rightController: The PIDController for the right side of the robot
                                drive.
        :param output:          A function that consumes the computed left and right
                                outputs (in volts) for the robot drive.
        :param requirements:    The subsystems to require.

        Constructs a new RamseteCommand that, when executed, will follow the
        provided trajectory. Performs no PID control and calculates no
        feedforwards; outputs are the raw wheel speeds from the RAMSETE controller,
        and will need to be converted into a usable form by the user.

        :param trajectory:   The trajectory to follow.
        :param pose:         A function that supplies the robot pose - use one of
                             the odometry classes to provide this.
        :param controller:   The RAMSETE controller used to follow the
                             trajectory.
        :param kinematics:   The kinematics for the robot drivetrain.
        :param output:       A function that consumes the computed left and right
                             wheel speeds.
        :param requirements: The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], controller: wpimath._controls._controls.controller.RamseteController, kinematics: wpimath.kinematics._kinematics.DifferentialDriveKinematics, output: typing.Callable[[meters_per_second, meters_per_second], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class RunCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that runs a Runnable continuously.  Has no end condition as-is;
    either subclass it or use Command.WithTimeout() or
    Command.WithInterrupt() to give it one.  If you only wish
    to execute a Runnable once, use InstantCommand.
    """
    @typing.overload
    def __init__(self, arg0: typing.Callable[[], None], *args) -> None: 
        """
        Creates a new RunCommand.  The Runnable will be run continuously until the
        command ends.  Does not run when disabled.

        :param toRun:        the Runnable to run
        :param requirements: the subsystems to require
        """
    @typing.overload
    def __init__(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def execute(self) -> None: ...
    @property
    def _toRun(self) -> typing.Callable[[], None]:
        """
        :type: typing.Callable[[], None]
        """
    @_toRun.setter
    def _toRun(self, arg0: typing.Callable[[], None]) -> None:
        pass
    pass
class ScheduleCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    Schedules the given commands when this command is initialized.  Useful for
    forking off from CommandGroups.  Note that if run from a CommandGroup, the
    group will not know about the status of the scheduled commands, and will
    treat this command as finishing instantly.
    """
    @typing.overload
    def __init__(self, *args) -> None: 
        """
        Creates a new ScheduleCommand that schedules the given commands when
        initialized.

        :param toSchedule: the commands to schedule
        """
    @typing.overload
    def __init__(self, toSchedule: Command) -> None: ...
    @typing.overload
    def __init__(self, toSchedule: typing.List[Command]) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
class SequentialCommandGroup(CommandGroupBase, CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A CommandGroups that runs a list of commands in sequence.

    As a rule, CommandGroups require the union of the requirements of their
    component commands.
    """
    @typing.overload
    def __init__(self, *args) -> None: 
        """
        Creates a new SequentialCommandGroup.  The given commands will be run
        sequentially, with the CommandGroup finishing when the last command
        finishes.

        :param commands: the commands to include in this group.

        Creates a new SequentialCommandGroup.  The given commands will be run
        sequentially, with the CommandGroup finishing when the last command
        finishes.

        :param commands: the commands to include in this group.
        """
    @typing.overload
    def __init__(self, commands: typing.List[Command]) -> None: ...
    @typing.overload
    def addCommands(self, *args) -> None: ...
    @typing.overload
    def addCommands(self, commands: typing.List[Command]) -> None: ...
    def andThen(self, arg0: typing.Callable[[], None], arg1: typing.List[Subsystem]) -> SequentialCommandGroup: ...
    def beforeStarting(self, arg0: typing.Callable[[], None], arg1: typing.List[Subsystem]) -> SequentialCommandGroup: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    @property
    def m_commands(self) -> typing.List[Command]:
        """
        :type: typing.List[Command]
        """
    pass
class StartEndCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that runs a given runnable when it is initialized, and another
    runnable when it ends. Useful for running and then stopping a motor, or
    extending and then retracting a solenoid. Has no end condition as-is; either
    subclass it or use Command.WithTimeout() or Command.WithInterrupt() to give
    it one.
    """
    @typing.overload
    def __init__(self, arg0: typing.Callable[[], None], arg1: typing.Callable[[], None], *args) -> None: 
        """
        Creates a new StartEndCommand.  Will run the given runnables when the
        command starts and when it ends.

        :param onInit:       the Runnable to run on command init
        :param onEnd:        the Runnable to run on command end
        :param requirements: the subsystems required by this command
        """
    @typing.overload
    def __init__(self, onInit: typing.Callable[[], None], onEnd: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def initialize(self) -> None: ...
    @property
    def _onEnd(self) -> typing.Callable[[], None]:
        """
        :type: typing.Callable[[], None]
        """
    @_onEnd.setter
    def _onEnd(self, arg0: typing.Callable[[], None]) -> None:
        pass
    @property
    def _onInit(self) -> typing.Callable[[], None]:
        """
        :type: typing.Callable[[], None]
        """
    @_onInit.setter
    def _onInit(self, arg0: typing.Callable[[], None]) -> None:
        pass
    pass
class PIDSubsystem(SubsystemBase, Subsystem, wpiutil._wpiutil.Sendable):
    """
    A subsystem that uses a PIDController to control an output.  The controller
    is run synchronously from the subsystem's periodic() method.

    @see PIDController
    """
    def __init__(self, controller: wpimath._controls._controls.controller.PIDController, initialPosition: float = 0) -> None: 
        """
        Creates a new PIDSubsystem.

        :param controller:      the PIDController to use
        :param initialPosition: the initial setpoint of the subsystem
        """
    def _getMeasurement(self) -> float: 
        """
        Returns the measurement of the process variable used by the PIDController.

        :returns: the measurement of the process variable
        """
    def _useOutput(self, output: float, setpoint: float) -> None: 
        """
        Uses the output from the PIDController.

        :param output:   the output of the PIDController
        :param setpoint: the setpoint of the PIDController (for feedforward)
        """
    def disable(self) -> None: 
        """
        Disables the PID control.  Sets output to zero.
        """
    def enable(self) -> None: 
        """
        Enables the PID control.  Resets the controller.
        """
    def getController(self) -> wpimath._controls._controls.controller.PIDController: 
        """
        Returns the PIDController.

        :returns: The controller.
        """
    def getSetpoint(self) -> float: 
        """
        Gets the setpoint for the subsystem.

        :returns: the setpoint for the subsystem
        """
    def isEnabled(self) -> bool: 
        """
        Returns whether the controller is enabled.

        :returns: Whether the controller is enabled.
        """
    def periodic(self) -> None: ...
    def setSetpoint(self, setpoint: float) -> None: 
        """
        Sets the setpoint for the subsystem.

        :param setpoint: the setpoint for the subsystem
        """
    @property
    def _m_controller(self) -> wpimath._controls._controls.controller.PIDController:
        """
        :type: wpimath._controls._controls.controller.PIDController
        """
    pass
class ProfiledPIDSubsystem(SubsystemBase, Subsystem, wpiutil._wpiutil.Sendable):
    """
    A subsystem that uses a ProfiledPIDController to control an output.  The
    controller is run synchronously from the subsystem's periodic() method.

    @see ProfiledPIDController
    """
    def __init__(self, controller: wpimath._controls._controls.controller.ProfiledPIDController, initialPosition: float = 0.0) -> None: 
        """
        Creates a new ProfiledPIDSubsystem.

        :param controller:      the ProfiledPIDController to use
        :param initialPosition: the initial goal position of the subsystem
        """
    def _getMeasurement(self) -> float: 
        """
        Returns the measurement of the process variable used by the
        ProfiledPIDController.

        :returns: the measurement of the process variable
        """
    def _useOutput(self, output: float, setpoint: wpimath._controls._controls.trajectory.TrapezoidProfile.State) -> None: 
        """
        Uses the output from the ProfiledPIDController.

        :param output:   the output of the ProfiledPIDController
        :param setpoint: the setpoint state of the ProfiledPIDController, for
                         feedforward
        """
    def disable(self) -> None: 
        """
        Disables the PID control.  Sets output to zero.
        """
    def enable(self) -> None: 
        """
        Enables the PID control. Resets the controller.
        """
    def getController(self) -> wpimath._controls._controls.controller.ProfiledPIDController: 
        """
        Returns the ProfiledPIDController.

        :returns: The controller.
        """
    def isEnabled(self) -> bool: 
        """
        Returns whether the controller is enabled.

        :returns: Whether the controller is enabled.
        """
    def periodic(self) -> None: ...
    @typing.overload
    def setGoal(self, goal: float) -> None: 
        """
        Sets the goal state for the subsystem.

        :param goal: The goal state for the subsystem's motion profile.

        Sets the goal state for the subsystem.  Goal velocity assumed to be zero.

        :param goal: The goal position for the subsystem's motion profile.
        """
    @typing.overload
    def setGoal(self, goal: wpimath._controls._controls.trajectory.TrapezoidProfile.State) -> None: ...
    @property
    def _m_controller(self) -> wpimath._controls._controls.controller.ProfiledPIDController:
        """
        :type: wpimath._controls._controls.controller.ProfiledPIDController
        """
    pass
class Swerve2ControllerCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses two PID controllers (PIDController) and a profiled PID
    controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a
    swerve drive.

    The command handles trajectory-following, Velocity PID calculations, and
    feedforwards internally. This is intended to be a more-or-less "complete
    solution" that can be used by teams without a great deal of controls
    expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw module states from the position PID controllers.

    The robot angle controller does not follow the angle given by
    the trajectory but rather goes to the angle given in the final state of the
    trajectory.
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive2Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[2]]], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param desiredRotation: The angle that the drivetrain should be
                                facing. This is sampled at each time step.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.

        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        Note 2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive2Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[2]]], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class Swerve3ControllerCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses two PID controllers (PIDController) and a profiled PID
    controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a
    swerve drive.

    The command handles trajectory-following, Velocity PID calculations, and
    feedforwards internally. This is intended to be a more-or-less "complete
    solution" that can be used by teams without a great deal of controls
    expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw module states from the position PID controllers.

    The robot angle controller does not follow the angle given by
    the trajectory but rather goes to the angle given in the final state of the
    trajectory.
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive3Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[3]]], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param desiredRotation: The angle that the drivetrain should be
                                facing. This is sampled at each time step.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.

        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        Note 2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive3Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[3]]], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class Swerve4ControllerCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses two PID controllers (PIDController) and a profiled PID
    controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a
    swerve drive.

    The command handles trajectory-following, Velocity PID calculations, and
    feedforwards internally. This is intended to be a more-or-less "complete
    solution" that can be used by teams without a great deal of controls
    expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw module states from the position PID controllers.

    The robot angle controller does not follow the angle given by
    the trajectory but rather goes to the angle given in the final state of the
    trajectory.
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive4Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[4]]], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param desiredRotation: The angle that the drivetrain should be
                                facing. This is sampled at each time step.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.

        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        Note 2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive4Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[4]]], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class Swerve6ControllerCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that uses two PID controllers (PIDController) and a profiled PID
    controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a
    swerve drive.

    The command handles trajectory-following, Velocity PID calculations, and
    feedforwards internally. This is intended to be a more-or-less "complete
    solution" that can be used by teams without a great deal of controls
    expertise.

    Advanced teams seeking more flexibility (for example, those who wish to
    use the onboard PID functionality of a "smart" motor controller) may use the
    secondary constructor that omits the PID and feedforward functionality,
    returning only the raw module states from the position PID controllers.

    The robot angle controller does not follow the angle given by
    the trajectory but rather goes to the angle given in the final state of the
    trajectory.
    """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive6Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, desiredRotation: typing.Callable[[], wpimath.geometry._geometry.Rotation2d], output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[6]]], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param desiredRotation: The angle that the drivetrain should be
                                facing. This is sampled at each time step.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.

        Constructs a new SwerveControllerCommand that when executed will follow the
        provided trajectory. This command will not return output voltages but
        rather raw module states from the position controllers which need to be put
        into a velocity PID.

        Note: The controllers will *not* set the outputVolts to zero upon
        completion of the path- this is left to the user, since it is not
        appropriate for paths with nonstationary endstates.

        Note 2: The final rotation of the robot will be set to the rotation of
        the final pose in the trajectory. The robot will not follow the rotations
        from the poses at each timestep. If alternate rotation behavior is desired,
        the other constructor with a supplier for rotation should be used.

        :param trajectory:      The trajectory to follow.
        :param pose:            A function that supplies the robot pose,
                                provided by the odometry class.
        :param kinematics:      The kinematics for the robot drivetrain.
        :param xController:     The Trajectory Tracker PID controller
                                for the robot's x position.
        :param yController:     The Trajectory Tracker PID controller
                                for the robot's y position.
        :param thetaController: The Trajectory Tracker PID controller
                                for angle for the robot.
        :param output:          The raw output module states from the
                                position controllers.
        :param requirements:    The subsystems to require.
        """
    @typing.overload
    def __init__(self, trajectory: wpimath._controls._controls.trajectory.Trajectory, pose: typing.Callable[[], wpimath.geometry._geometry.Pose2d], kinematics: wpimath.kinematics._kinematics.SwerveDrive6Kinematics, xController: wpimath._controls._controls.controller.PIDController, yController: wpimath._controls._controls.controller.PIDController, thetaController: wpimath._controls._controls.controller.ProfiledPIDControllerRadians, output: typing.Callable[[typing.List[wpimath.kinematics._kinematics.SwerveModuleState[6]]], None], requirements: typing.List[Subsystem] = []) -> None: ...
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class TimedCommandRobot(wpilib._wpilib.TimedRobot, wpilib._wpilib.IterativeRobotBase, wpilib._wpilib.RobotBase):
    """
    TimedCommandRobot implements the IterativeRobotBase robot program framework.

    The TimedCommandRobot class is intended to be subclassed by a user creating a
    command-based robot program. This python-specific class calls the
    CommandScheduler run method in robotPeriodic for you.
    """
    def __init__(self) -> None: ...
    def robotPeriodic(self) -> None: 
        """
        Ensures commands are run
        """
    kDefaultPeriod = 20.0
    pass
class TrapezoidProfileCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that runs a TrapezoidProfile.  Useful for smoothly controlling
    mechanism motion.

    @see TrapezoidProfile
    """
    def __init__(self, profile: wpimath._controls._controls.trajectory.TrapezoidProfile, output: typing.Callable[[wpimath._controls._controls.trajectory.TrapezoidProfile.State], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Creates a new TrapezoidProfileCommand that will execute the given
        TrapezoidalProfile. Output will be piped to the provided consumer function.

        :param profile:      The motion profile to execute.
        :param output:       The consumer for the profile output.
        :param requirements: The list of requirements.
        """
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class TrapezoidProfileCommandRadians(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that runs a TrapezoidProfile.  Useful for smoothly controlling
    mechanism motion.

    @see TrapezoidProfile
    """
    def __init__(self, profile: wpimath._controls._controls.trajectory.TrapezoidProfileRadians, output: typing.Callable[[wpimath._controls._controls.trajectory.TrapezoidProfileRadians.State], None], requirements: typing.List[Subsystem] = []) -> None: 
        """
        Creates a new TrapezoidProfileCommand that will execute the given
        TrapezoidalProfile. Output will be piped to the provided consumer function.

        :param profile:      The motion profile to execute.
        :param output:       The consumer for the profile output.
        :param requirements: The list of requirements.
        """
    def end(self, interrupted: bool) -> None: ...
    def execute(self) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class TrapezoidProfileSubsystem(SubsystemBase, Subsystem, wpiutil._wpiutil.Sendable):
    """
    A subsystem that generates and runs trapezoidal motion profiles
    automatically.  The user specifies how to use the current state of the motion
    profile by overriding the `UseState` method.
    """
    def __init__(self, constraints: wpimath._controls._controls.trajectory.TrapezoidProfile.Constraints, initialPosition: float = 0.0, period: seconds = 0.02) -> None: 
        """
        Creates a new TrapezoidProfileSubsystem.

        :param constraints:     The constraints (maximum velocity and acceleration)
                                for the profiles.
        :param initialPosition: The initial position of the controller mechanism
                                when the subsystem is constructed.
        :param period:          The period of the main robot loop, in seconds.
        """
    def _disable(self) -> None: 
        """
        Disable the TrapezoidProfileSubsystem's output.
        """
    def _enable(self) -> None: 
        """
        Enable the TrapezoidProfileSubsystem's output.
        """
    def _useState(self, state: wpimath._controls._controls.trajectory.TrapezoidProfile.State) -> None: 
        """
        Users should override this to consume the current state of the motion
        profile.

        :param state: The current state of the motion profile.
        """
    def periodic(self) -> None: ...
    @typing.overload
    def setGoal(self, goal: float) -> None: 
        """
        Sets the goal state for the subsystem.

        :param goal: The goal state for the subsystem's motion profile.

        Sets the goal state for the subsystem.  Goal velocity assumed to be zero.

        :param goal: The goal position for the subsystem's motion profile.
        """
    @typing.overload
    def setGoal(self, goal: wpimath._controls._controls.trajectory.TrapezoidProfile.State) -> None: ...
    pass
class TrapezoidProfileSubsystemRadians(SubsystemBase, Subsystem, wpiutil._wpiutil.Sendable):
    """
    A subsystem that generates and runs trapezoidal motion profiles
    automatically.  The user specifies how to use the current state of the motion
    profile by overriding the `UseState` method.
    """
    def __init__(self, constraints: wpimath._controls._controls.trajectory.TrapezoidProfileRadians.Constraints, initialPosition: radians = 0.0, period: seconds = 0.02) -> None: 
        """
        Creates a new TrapezoidProfileSubsystem.

        :param constraints:     The constraints (maximum velocity and acceleration)
                                for the profiles.
        :param initialPosition: The initial position of the controller mechanism
                                when the subsystem is constructed.
        :param period:          The period of the main robot loop, in seconds.
        """
    def _disable(self) -> None: 
        """
        Disable the TrapezoidProfileSubsystem's output.
        """
    def _enable(self) -> None: 
        """
        Enable the TrapezoidProfileSubsystem's output.
        """
    def _useState(self, state: wpimath._controls._controls.trajectory.TrapezoidProfileRadians.State) -> None: 
        """
        Users should override this to consume the current state of the motion
        profile.

        :param state: The current state of the motion profile.
        """
    def periodic(self) -> None: ...
    @typing.overload
    def setGoal(self, goal: radians) -> None: 
        """
        Sets the goal state for the subsystem.

        :param goal: The goal state for the subsystem's motion profile.

        Sets the goal state for the subsystem.  Goal velocity assumed to be zero.

        :param goal: The goal position for the subsystem's motion profile.
        """
    @typing.overload
    def setGoal(self, goal: wpimath._controls._controls.trajectory.TrapezoidProfileRadians.State) -> None: ...
    pass
class Trigger():
    """
    A class used to bind command scheduling to events.  The
    Trigger class is a base for all command-event-binding classes, and so the
    methods are named fairly abstractly; for purpose-specific wrappers, see
    Button.

    @see Button
    """
    def __bool__(self) -> bool: 
        """
        Returns whether or not the trigger is currently active
        """
    @typing.overload
    def __init__(self) -> None: 
        """
        Create a new trigger that is active when the given condition is true.

        :param isActive: Whether the trigger is active.

        Create a new trigger that is never active (default constructor) - activity
        can be further determined by subclass code.
        """
    @typing.overload
    def __init__(self, isActive: typing.Callable[[], bool]) -> None: ...
    def and_(self, other: Trigger) -> Trigger: 
        """
        Composes this trigger with another trigger, returning a new trigger that is active when both
        triggers are active.

        :param trigger: the trigger to compose with

        :returns: the trigger that is active when both triggers are active
        """
    def cancelWhenActive(self, command: Command) -> Trigger: 
        """
        Binds a command to be canceled when the trigger becomes active.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        and scheduling of the command.

        :param command: The command to bind.

        :returns: The trigger, for chained calls.
        """
    def debounce(self, debounceTime: seconds, type: wpimath.filter._filter.Debouncer.DebounceType = DebounceType.kRising) -> Trigger: 
        """
        Creates a new debounced trigger from this trigger - it will become active
        when this trigger has been active for longer than the specified period.

        :param debounceTime: The debounce period.
        :param type:         The debounce type.

        :returns: The debounced trigger.
        """
    def not_(self) -> Trigger: 
        """
        Creates a new trigger that is active when this trigger is inactive, i.e. that acts as the
        negation of this trigger.

        :param trigger: the trigger to compose with

        :returns: the trigger that is active when both triggers are active
        """
    def or_(self, other: Trigger) -> Trigger: 
        """
        Composes this trigger with another trigger, returning a new trigger that is active when either
        triggers are active.

        :param trigger: the trigger to compose with

        :returns: the trigger that is active when both triggers are active
        """
    def toggleWhenActive(self, command: Command, interruptible: bool = True) -> Trigger: 
        """
        Binds a command to start when the trigger becomes active, and be canceled
        when it again becomes active.  Takes a raw pointer, and so is non-owning;
        users are responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.
        """
    @typing.overload
    def whenActive(self, command: Command, interruptible: bool = True) -> Trigger: 
        """
        Binds a command to start when the trigger becomes active.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.

        Binds a runnable to execute when the trigger becomes active.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whenActive(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> Trigger: ...
    @typing.overload
    def whenInactive(self, command: Command, interruptible: bool = True) -> Trigger: 
        """
        Binds a command to start when the trigger becomes inactive.  Takes a
        raw pointer, and so is non-owning; users are responsible for the lifespan
        of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.

        Binds a runnable to execute when the trigger becomes inactive.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whenInactive(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> Trigger: ...
    @typing.overload
    def whileActiveContinous(self, command: Command, interruptible: bool = True) -> Trigger: 
        """
        Binds a command to be started repeatedly while the trigger is active, and
        canceled when it becomes inactive.  Takes a raw pointer, and so is
        non-owning; users are responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.

        Binds a runnable to execute repeatedly while the trigger is active.

        :param toRun:        the runnable to execute.
        :param requirements: the required subsystems.
        """
    @typing.overload
    def whileActiveContinous(self, toRun: typing.Callable[[], None], requirements: typing.List[Subsystem] = []) -> Trigger: ...
    def whileActiveOnce(self, command: Command, interruptible: bool = True) -> Trigger: 
        """
        Binds a command to be started when the trigger becomes active, and
        canceled when it becomes inactive.  Takes a raw pointer, and so is
        non-owning; users are responsible for the lifespan of the command.

        :param command:       The command to bind.
        :param interruptible: Whether the command should be interruptible.

        :returns: The trigger, for chained calls.
        """
    pass
class WaitCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that does nothing but takes a specified amount of time to finish.
    Useful for CommandGroups.  Can also be subclassed to make a command with an
    internal timer.
    """
    def __init__(self, duration: seconds) -> None: 
        """
        Creates a new WaitCommand.  This command will do nothing, and end after the
        specified duration.

        :param duration: the time to wait
        """
    def end(self, interrupted: bool) -> None: ...
    def initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    @property
    def _m_timer(self) -> wpilib._wpilib.Timer:
        """
        :type: wpilib._wpilib.Timer
        """
    pass
class WaitUntilCommand(CommandBase, Command, wpiutil._wpiutil.Sendable):
    """
    A command that does nothing but ends after a specified match time or
    condition.  Useful for CommandGroups.
    """
    @typing.overload
    def __init__(self, condition: typing.Callable[[], bool]) -> None: 
        """
        Creates a new WaitUntilCommand that ends after a given condition becomes
        true.

        :param condition: the condition to determine when to end

        Creates a new WaitUntilCommand that ends after a given match time.

        NOTE: The match timer used for this command is UNOFFICIAL.  Using this
        command does NOT guarantee that the time at which the action is performed
        will be judged to be legal by the referees.  When in doubt, add a safety
        factor or time the action manually.

        :param time: the match time after which to end, in seconds
        """
    @typing.overload
    def __init__(self, time: seconds) -> None: ...
    def isFinished(self) -> bool: ...
    def runsWhenDisabled(self) -> bool: ...
    pass
def requirementsDisjoint(first: Command, second: Command) -> bool:
    """
    Checks if two commands have disjoint requirement sets.

    :param first:  The first command to check.
    :param second: The second command to check.

    :returns: False if first and second share a requirement.
    """
_cleanup: PyCapsule # value = <capsule object NULL>
