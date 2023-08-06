from __future__ import annotations
import commands1._impl._commands_v1.command
import typing
import _pyntcore._ntcore
import commands1._impl._commands_v1
import commands1._impl._commands_v1.button
import wpilib._wpilib
import wpilib.interfaces._interfaces
import wpiutil._wpiutil

__all__ = [
    "Command",
    "CommandGroup",
    "CommandGroupEntry",
    "ConditionalCommand",
    "InstantCommand",
    "PIDAnalogAccelerometer",
    "PIDAnalogGyro",
    "PIDAnalogInput",
    "PIDAnalogPotentiometer",
    "PIDBase",
    "PIDCommand",
    "PIDController",
    "PIDEncoder",
    "PIDInterface",
    "PIDMotorController",
    "PIDOutput",
    "PIDSource",
    "PIDSubsystem",
    "PIDUltrasonic",
    "PrintCommand",
    "Scheduler",
    "StartCommand",
    "Subsystem",
    "TimedCommand",
    "WaitCommand",
    "WaitForChildren",
    "WaitUntilCommand"
]


class Command(wpiutil._wpiutil.Sendable):
    """
    The Command class is at the very core of the entire command framework.

    Every command can be started with a call to Start(). Once a command is
    started it will call Initialize(), and then will repeatedly call Execute()
    until the IsFinished() returns true. Once it does,End() will be called.

    However, if at any point while it is running Cancel() is called, then the
    command will be stopped and Interrupted() will be called.

    If a command uses a Subsystem, then it should specify that it does so by
    calling the Requires() method in its constructor. Note that a Command may
    have multiple requirements, and Requires() should be called for each one.

    If a command is running and a new command with shared requirements is
    started, then one of two things will happen. If the active command is
    interruptible, then Cancel() will be called and the command will be removed
    to make way for the new one. If the active command is not interruptible, the
    other one will not even be started, and the active one will continue
    functioning.

    This class is provided by the OldCommands VendorDep
    *
    @see CommandGroup
    @see Subsystem
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new command.

        The name of this command will be default.

        Creates a new command with the given name and no timeout.

        :param name: the name for this command

        Creates a new command with the given timeout and a default name.

        :param timeout: the time before this command "times out"
                        @see IsTimedOut()

        Creates a new command with the given timeout and a default name.

        :param subsystem: the subsystem that the command requires

        Creates a new command with the given name and timeout.

        :param name:    the name of the command
        :param timeout: the time before this command "times out"
                        @see IsTimedOut()

        Creates a new command with the given name and timeout.

        :param name:      the name of the command
        :param subsystem: the subsystem that the command requires

        Creates a new command with the given name and timeout.

        :param timeout:   the time before this command "times out"
        :param subsystem: the subsystem that the command requires @see IsTimedOut()

        Creates a new command with the given name and timeout.

        :param name:      the name of the command
        :param timeout:   the time before this command "times out"
        :param subsystem: the subsystem that the command requires @see IsTimedOut()
        """
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, timeout: seconds) -> None: ...
    @typing.overload
    def __init__(self, name: str, timeout: seconds, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, timeout: seconds) -> None: ...
    @typing.overload
    def __init__(self, timeout: seconds, subsystem: Subsystem) -> None: ...
    def _cancel(self) -> None: 
        """
        This works like Cancel(), except that it doesn't throw an exception if it
        is a part of a command group.

        Should only be called by the parent command group.
        """
    def _end(self) -> None: ...
    def _execute(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def assertUnlocked(self, message: str) -> bool: 
        """
        If changes are locked, then this will generate a CommandIllegalUse error.

        :param message: The message to report on error (it is appended by a default
                        message)

        :returns: True if assert passed, false if assert failed.
        """
    def cancel(self) -> None: 
        """
        This will cancel the current command.

        This will cancel the current command eventually. It can be called multiple
        times. And it can be called when the command is not running. If the command
        is running though, then the command will be marked as canceled and
        eventually removed.

        A command can not be canceled if it is a part of a command group, you must
        cancel the command group instead.
        """
    def clearRequirements(self) -> None: 
        """
        Clears list of subsystem requirements.

        This is only used by ConditionalCommand so canceling the chosen command
        works properly in CommandGroup.
        """
    def doesRequire(self, subsystem: Subsystem) -> bool: 
        """
        Checks if the command requires the given Subsystem.

        :param subsystem: the subsystem

        :returns: whether or not the subsystem is required (false if given nullptr)
        """
    def end(self) -> None: 
        """
        Called when the command ended peacefully.

        This is where you may want to wrap up loose ends, like shutting off a motor
        that was being used in the command.
        """
    def execute(self) -> None: 
        """
        The execute method is called repeatedly until this Command either finishes
        or is canceled.
        """
    def getGroup(self) -> CommandGroup: 
        """
        Returns the CommandGroup that this command is a part of.

        Will return null if this Command is not in a group.

        :returns: The CommandGroup that this command is a part of (or null if not in
                  group)
        """
    def getID(self) -> int: 
        """
        Get the ID (sequence number) for this command.

        The ID is a unique sequence number that is incremented for each command.

        :returns: The ID of this command
        """
    def getName(self) -> str: 
        """
        Gets the name of this Command.

        :returns: Name
        """
    def getRequirements(self) -> set: 
        """
        Returns the requirements (as an std::set of Subsystem pointers) of this
        command.

        :returns: The requirements (as an std::set of Subsystem pointers) of this
                  command
        """
    def getSubsystem(self) -> str: 
        """
        Gets the subsystem name of this Command.

        :returns: Subsystem name
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def initialize(self) -> None: 
        """
        The initialize method is called the first time this Command is run after
        being started.
        """
    def interrupted(self) -> None: 
        """
        Called when the command ends because somebody called Cancel() or another
        command shared the same requirements as this one, and booted it out.

        This is where you may want to wrap up loose ends, like shutting off a motor
        that was being used in the command.

        Generally, it is useful to simply call the End() method within this method,
        as done here.
        """
    def isCanceled(self) -> bool: 
        """
        Returns whether or not this has been canceled.

        :returns: whether or not this has been canceled
        """
    def isCompleted(self) -> bool: 
        """
        Returns whether or not the command has completed running.

        :returns: whether or not the command has completed running.
        """
    def isFinished(self) -> bool: 
        """
        Returns whether this command is finished.

        If it is, then the command will be removed and End() will be called.

        It may be useful for a team to reference the IsTimedOut() method for
        time-sensitive commands.

        Returning false will result in the command never ending automatically.
        It may still be canceled manually or interrupted by another command.
        Returning true will result in the command executing once and finishing
        immediately. We recommend using InstantCommand for this.

        :returns: Whether this command is finished.
                  @see IsTimedOut()
        """
    def isInitialized(self) -> bool: 
        """
        Returns whether or not the command has been initialized.

        :returns: whether or not the command has been initialized.
        """
    def isInterruptible(self) -> bool: 
        """
        Returns whether or not this command can be interrupted.

        :returns: whether or not this command can be interrupted
        """
    def isParented(self) -> bool: 
        """
        Returns whether the command has a parent.

        :param True: if the command has a parent.
        """
    def isRunning(self) -> bool: 
        """
        Returns whether or not the command is running.

        This may return true even if the command has just been canceled, as it may
        not have yet called Interrupted().

        :returns: whether or not the command is running
        """
    def isTimedOut(self) -> bool: 
        """
        Returns whether or not the TimeSinceInitialized() method returns a number
        which is greater than or equal to the timeout for the command.

        If there is no timeout, this will always return false.

        :returns: whether the time has expired
        """
    def requires(self, subsystem: Subsystem) -> None: 
        """
        This method specifies that the given Subsystem is used by this command.

        This method is crucial to the functioning of the Command System in general.

        Note that the recommended way to call this method is in the constructor.

        :param subsystem: The Subsystem required
                          @see Subsystem
        """
    def run(self) -> bool: 
        """
        The run method is used internally to actually run the commands.

        :returns: Whether or not the command should stay within the Scheduler.
        """
    def setInterruptible(self, interruptible: bool) -> None: 
        """
        Sets whether or not this command can be interrupted.

        :param interruptible: whether or not this command can be interrupted
        """
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Command.

        :param name: name
        """
    def setParent(self, parent: CommandGroup) -> None: 
        """
        Sets the parent of this command. No actual change is made to the group.

        :param parent: the parent
        """
    def setRunWhenDisabled(self, run: bool) -> None: 
        """
        Sets whether or not this Command should run when the robot is disabled.

        By default a command will not run when the robot is disabled, and will in
        fact be canceled.

        :param run: Whether this command should run when the robot is disabled.
        """
    def setSubsystem(self, subsystem: str) -> None: 
        """
        Sets the subsystem name of this Command.

        :param subsystem: subsystem name
        """
    def setTimeout(self, timeout: seconds) -> None: 
        """
        Sets the timeout of this command.

        :param timeout: the timeout
                        @see IsTimedOut()
        """
    def start(self) -> None: 
        """
        Starts up the command. Gets the command ready to start.

        Note that the command will eventually start, however it will not
        necessarily do so immediately, and may in fact be canceled before
        initialize is even called.
        """
    def timeSinceInitialized(self) -> seconds: 
        """
        Returns the time since this command was initialized.

        This function will work even if there is no specified timeout.

        :returns: the time since this command was initialized.
        """
    def willRunWhenDisabled(self) -> bool: 
        """
        Returns whether or not this Command will run when the robot is disabled, or
        if it will cancel itself.

        :returns: Whether this Command will run when the robot is disabled, or if it
                  will cancel itself.
        """
    pass
class CommandGroup(Command, wpiutil._wpiutil.Sendable):
    """
    A CommandGroup is a list of commands which are executed in sequence.

    Commands in a CommandGroup are added using the AddSequential() method and are
    called sequentially. CommandGroups are themselves Commands and can be given
    to other CommandGroups.

    CommandGroups will carry all of the requirements of their Command
    subcommands. Additional requirements can be specified by calling Requires()
    normally in the constructor.

    CommandGroups can also execute commands in parallel, simply by adding them
    using AddParallel().

    This class is provided by the OldCommands VendorDep

    @see Command
    @see Subsystem
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new CommandGroup with the given name.

        :param name: The name for this command group
        """
    @typing.overload
    def __init__(self, name: str) -> None: ...
    def _end(self) -> None: ...
    def _execute(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    @typing.overload
    def addParallel(self, command: Command) -> None: 
        """
        Adds a new child Command to the group. The Command will be started after
        all the previously added Commands.

        Instead of waiting for the child to finish, a CommandGroup will have it run
        at the same time as the subsequent Commands. The child will run until
        either it finishes, a new child with conflicting requirements is started,
        or the main sequence runs a Command with conflicting requirements. In the
        latter two cases, the child will be canceled even if it says it can't be
        interrupted.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The command to be added

        Adds a new child Command to the group with the given timeout. The Command
        will be started after all the previously added Commands.

        Once the Command is started, it will run until it finishes, is interrupted,
        or the time expires, whichever is sooner. Note that the given Command will
        have no knowledge that it is on a timer.

        Instead of waiting for the child to finish, a CommandGroup will have it run
        at the same time as the subsequent Commands. The child will run until
        either it finishes, the timeout expires, a new child with conflicting
        requirements is started, or the main sequence runs a Command with
        conflicting requirements. In the latter two cases, the child will be
        canceled even if it says it can't be interrupted.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The command to be added
        :param timeout: The timeout
        """
    @typing.overload
    def addParallel(self, command: Command, timeout: seconds) -> None: ...
    @typing.overload
    def addSequential(self, command: Command) -> None: 
        """
        Adds a new Command to the group. The Command will be started after all the
        previously added Commands.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The Command to be added

        Adds a new Command to the group with a given timeout. The Command will be
        started after all the previously added commands.

        Once the Command is started, it will be run until it finishes or the time
        expires, whichever is sooner.  Note that the given Command will have no
        knowledge that it is on a timer.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The Command to be added
        :param timeout: The timeout
        """
    @typing.overload
    def addSequential(self, command: Command, timeout: seconds) -> None: ...
    def end(self) -> None: 
        """
        Can be overridden by teams.
        """
    def execute(self) -> None: 
        """
        Can be overridden by teams.
        """
    def getSize(self) -> int: ...
    def initialize(self) -> None: 
        """
        Can be overridden by teams.
        """
    def interrupted(self) -> None: 
        """
        Can be overridden by teams.
        """
    def isFinished(self) -> bool: 
        """
        Can be overridden by teams.
        """
    def isInterruptible(self) -> bool: ...
    pass
class CommandGroupEntry():
    class Sequence():
        """
        Members:

          kSequence_InSequence

          kSequence_BranchPeer

          kSequence_BranchChild
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        __members__: dict # value = {'kSequence_InSequence': <Sequence.kSequence_InSequence: 0>, 'kSequence_BranchPeer': <Sequence.kSequence_BranchPeer: 1>, 'kSequence_BranchChild': <Sequence.kSequence_BranchChild: 2>}
        kSequence_BranchChild: commands1._impl._commands_v1.command.CommandGroupEntry.Sequence # value = <Sequence.kSequence_BranchChild: 2>
        kSequence_BranchPeer: commands1._impl._commands_v1.command.CommandGroupEntry.Sequence # value = <Sequence.kSequence_BranchPeer: 1>
        kSequence_InSequence: commands1._impl._commands_v1.command.CommandGroupEntry.Sequence # value = <Sequence.kSequence_InSequence: 0>
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, command: Command, state: CommandGroupEntry.Sequence, timeout: seconds = -1.0) -> None: ...
    def isTimedOut(self) -> bool: ...
    @property
    def m_command(self) -> Command:
        """
        :type: Command
        """
    @property
    def m_state(self) -> CommandGroupEntry.Sequence:
        """
        :type: CommandGroupEntry.Sequence
        """
    @m_state.setter
    def m_state(self, arg0: CommandGroupEntry.Sequence) -> None:
        pass
    @property
    def m_timeout(self) -> seconds:
        """
        :type: seconds
        """
    pass
class ConditionalCommand(Command, wpiutil._wpiutil.Sendable):
    """
    A ConditionalCommand is a Command that starts one of two commands.

    A ConditionalCommand uses the Condition method to determine whether it should
    run onTrue or onFalse.

    A ConditionalCommand adds the proper Command to the Scheduler during
    Initialize() and then IsFinished() will return true once that Command has
    finished executing.

    If no Command is specified for onFalse, the occurrence of that condition
    will be a no-op.

    A ConditionalCommand will require the superset of subsystems of the onTrue
    and onFalse commands.

    This class is provided by the OldCommands VendorDep

    @see Command
    @see Scheduler
    """
    @typing.overload
    def __init__(self, name: str, onTrue: Command, onFalse: Command = None) -> None: 
        """
        Creates a new ConditionalCommand with given onTrue and onFalse Commands.

        :param onTrue:  The Command to execute if Condition() returns true
        :param onFalse: The Command to execute if Condition() returns false

        Creates a new ConditionalCommand with given onTrue and onFalse Commands.

        :param name:    The name for this command group
        :param onTrue:  The Command to execute if Condition() returns true
        :param onFalse: The Command to execute if Condition() returns false
        """
    @typing.overload
    def __init__(self, onTrue: Command, onFalse: Command = None) -> None: ...
    def _cancel(self) -> None: ...
    def _condition(self) -> bool: 
        """
        The Condition to test to determine which Command to run.

        :returns: true if m_onTrue should be run or false if m_onFalse should be run.
        """
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class InstantCommand(Command, wpiutil._wpiutil.Sendable):
    """
    This command will execute once, then finish immediately afterward.

    Subclassing InstantCommand is shorthand for returning true from IsFinished().

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new InstantCommand with the given name.

        :param name: The name for this command

        Creates a new InstantCommand with the given requirement.

        :param subsystem: The subsystem that the command requires

        Creates a new InstantCommand with the given name.

        :param name:      The name for this command
        :param subsystem: The subsystem that the command requires

        Create a command that calls the given function when run.

        :param func: The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param subsystem: The subsystems that this command runs on.
        :param func:      The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param name: The name of the command.
        :param func: The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param name:      The name of the command.
        :param subsystem: The subsystems that this command runs on.
        :param func:      The function to run when Initialize() is run.
        """
    @typing.overload
    def __init__(self, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, name: str, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem, func: typing.Callable[[], None]) -> None: ...
    def _initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class PIDSource():
    """
    PIDSource interface is a generic sensor source for the PID class.

    All sensors that can be used with the PID class will implement the PIDSource
    that returns a standard value that will be used in the PID code.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self) -> None: ...
    def getPIDSourceType(self) -> commands1._impl._commands_v1.PIDSourceType: ...
    def pidGet(self) -> float: ...
    def setPIDSourceType(self, pidSource: commands1._impl._commands_v1.PIDSourceType) -> None: 
        """
        Set which parameter you are using as a process control variable.

        :param pidSource: An enum to select the parameter.
        """
    @property
    def _m_pidSource(self) -> commands1._impl._commands_v1.PIDSourceType:
        """
        :type: commands1._impl._commands_v1.PIDSourceType
        """
    @_m_pidSource.setter
    def _m_pidSource(self, arg0: commands1._impl._commands_v1.PIDSourceType) -> None:
        pass
    pass
class PIDAnalogGyro(PIDSource, wpilib._wpilib.AnalogGyro, wpilib.interfaces._interfaces.Gyro, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for AnalogGyro for old PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Get the PIDOutput for the PIDSource base object. Can be set to return
        angle or rate using SetPIDSourceType(). Defaults to angle.

        :returns: The PIDOutput (angle or rate, defaults to angle)
        """
    @typing.overload
    def __init__(self, arg0: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: float) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.AnalogInput) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.AnalogInput, arg1: int, arg2: float) -> None: ...
    kCalibrationSampleTime = 5.0
    kDefaultVoltsPerDegreePerSecond = 0.007
    kSamplesPerSecond = 50.0
    pass
class PIDAnalogInput(PIDSource, wpilib._wpilib.AnalogInput, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for AnalogInput for old
    PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Get the Average value for the PID Source base object.

        :returns: The average voltage.
        """
    def __init__(self, arg0: int) -> None: ...
    pass
class PIDAnalogPotentiometer(PIDSource, wpilib._wpilib.AnalogPotentiometer, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for AnalogPotentiometer for old
    PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Implement the PIDSource interface.

        :returns: The current reading.
        """
    @typing.overload
    def __init__(self, arg0: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.AnalogInput) -> None: ...
    pass
class PIDInterface():
    """
    Interface for PID Control Loop.

    This class is provided by the OldCommands VendorDep

    :deprecated: All APIs which use this have been deprecated.
    """
    def __init__(self) -> None: ...
    def getD(self) -> float: ...
    def getI(self) -> float: ...
    def getP(self) -> float: ...
    def getSetpoint(self) -> float: ...
    def reset(self) -> None: ...
    def setPID(self, p: float, i: float, d: float) -> None: ...
    def setSetpoint(self, setpoint: float) -> None: ...
    pass
class PIDOutput():
    """
    PIDOutput interface is a generic output for the PID class.

    MotorControllers use this class. Users implement this interface to allow for
    a PIDController to read directly from the inputs.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self) -> None: ...
    def pidWrite(self, output: float) -> None: ...
    pass
class PIDBase(PIDInterface, PIDOutput, wpiutil._wpiutil.Sendable):
    """
    Class implements a PID Control Loop.

    Creates a separate thread which reads the given PIDSource and takes care of
    the integral calculations, as well as writing the given PIDOutput.

    This feedback controller runs in discrete time, so time deltas are not used
    in the integral and derivative calculations. Therefore, the sample rate
    affects the controller's behavior for a given set of PID constants.

    This class is provided by the OldCommands VendorDep

    :deprecated: All APIs which use this have been deprecated.
    """
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, source: PIDSource, output: PIDOutput) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, source: PIDSource, output: PIDOutput) -> None: ...
    def _calculate(self) -> None: 
        """
        Read the input, calculate the output accordingly, and write to the output.
        This should only be called by the Notifier.
        """
    def _calculateFeedForward(self) -> float: 
        """
        Calculate the feed forward term.

        Both of the provided feed forward calculations are velocity feed forwards.
        If a different feed forward calculation is desired, the user can override
        this function and provide his or her own. This function does no
        synchronization because the PIDBase class only calls it in synchronized
        code, so be careful if calling it oneself.

        If a velocity PID controller is being used, the F term should be set to 1
        over the maximum setpoint for the output. If a position PID controller is
        being used, the F term should be set to 1 over the maximum speed for the
        output measured in setpoint units per this controller's update period (see
        the default period in this class's constructor).
        """
    def _getContinuousError(self, error: float) -> float: 
        """
        Wraps error around for continuous inputs. The original error is returned if
        continuous mode is disabled. This is an unsynchronized function.

        :param error: The current error of the PID controller.

        :returns: Error for continuous inputs.
        """
    def get(self) -> float: 
        """
        Return the current PID result.

        This is always centered on zero and constrained the the max and min outs.

        :returns: the latest calculated output
        """
    def getAvgError(self) -> float: ...
    def getD(self) -> float: 
        """
        Get the Differential coefficient.

        :returns: differential coefficient
        """
    def getDeltaSetpoint(self) -> float: 
        """
        Returns the change in setpoint over time of the PIDBase.

        :returns: the change in setpoint over time
        """
    def getError(self) -> float: 
        """
        Returns the current difference of the input from the setpoint.

        :returns: the current error
        """
    def getF(self) -> float: 
        """
        Get the Feed forward coefficient.

        :returns: Feed forward coefficient
        """
    def getI(self) -> float: 
        """
        Get the Integral coefficient.

        :returns: integral coefficient
        """
    def getP(self) -> float: 
        """
        Get the Proportional coefficient.

        :returns: proportional coefficient
        """
    def getPIDSourceType(self) -> commands1._impl._commands_v1.PIDSourceType: 
        """
        Returns the type of input the PID controller is using.

        :returns: the PID controller input type
        """
    def getSetpoint(self) -> float: 
        """
        Returns the current setpoint of the PIDBase.

        :returns: the current setpoint
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def onTarget(self) -> bool: 
        """
        Return true if the error is within the percentage of the total input range,
        determined by SetTolerance. This asssumes that the maximum and minimum
        input were set using SetInput.

        Currently this just reports on target as the actual value passes through
        the setpoint. Ideally it should be based on being within the tolerance for
        some period of time.

        This will return false until at least one input value has been computed.
        """
    def pidWrite(self, output: float) -> None: 
        """
        Passes the output directly to SetSetpoint().

        PIDControllers can be nested by passing a PIDController as another
        PIDController's output. In that case, the output of the parent controller
        becomes the input (i.e., the reference) of the child.

        It is the caller's responsibility to put the data into a valid form for
        SetSetpoint().
        """
    def reset(self) -> None: 
        """
        Reset the previous error, the integral term, and disable the controller.
        """
    def setAbsoluteTolerance(self, absTolerance: float) -> None: 
        """
        Set the absolute error which is considered tolerable for use with
        OnTarget.

        :param absTolerance: error which is tolerable
        """
    def setContinuous(self, continuous: bool = True) -> None: 
        """
        Set the PID controller to consider the input to be continuous,

        Rather then using the max and min input range as constraints, it considers
        them to be the same point and automatically calculates the shortest route
        to the setpoint.

        :param continuous: true turns on continuous, false turns off continuous
        """
    def setD(self, d: float) -> None: 
        """
        Set the Differential coefficient of the PID controller gain.

        :param d: differential coefficient
        """
    def setF(self, f: float) -> None: 
        """
        Get the Feed forward coefficient of the PID controller gain.

        :param f: Feed forward coefficient
        """
    def setI(self, i: float) -> None: 
        """
        Set the Integral coefficient of the PID controller gain.

        :param i: integral coefficient
        """
    def setInputRange(self, minimumInput: float, maximumInput: float) -> None: 
        """
        Sets the maximum and minimum values expected from the input.

        :param minimumInput: the minimum value expected from the input
        :param maximumInput: the maximum value expected from the output
        """
    def setOutputRange(self, minimumOutput: float, maximumOutput: float) -> None: 
        """
        Sets the minimum and maximum values to write.

        :param minimumOutput: the minimum value to write to the output
        :param maximumOutput: the maximum value to write to the output
        """
    def setP(self, p: float) -> None: 
        """
        Set the Proportional coefficient of the PID controller gain.

        :param p: proportional coefficient
        """
    @typing.overload
    def setPID(self, p: float, i: float, d: float) -> None: 
        """
        Set the PID Controller gain parameters.

        Set the proportional, integral, and differential coefficients.

        :param p: Proportional coefficient
        :param i: Integral coefficient
        :param d: Differential coefficient

        Set the PID Controller gain parameters.

        Set the proportional, integral, and differential coefficients.

        :param p: Proportional coefficient
        :param i: Integral coefficient
        :param d: Differential coefficient
        :param f: Feed forward coefficient
        """
    @typing.overload
    def setPID(self, p: float, i: float, d: float, f: float) -> None: ...
    def setPIDSourceType(self, pidSource: commands1._impl._commands_v1.PIDSourceType) -> None: 
        """
        Sets what type of input the PID controller will use.
        """
    def setPercentTolerance(self, percent: float) -> None: 
        """
        Set the percentage error which is considered tolerable for use with
        OnTarget.

        :param percent: error which is tolerable
        """
    def setSetpoint(self, setpoint: float) -> None: 
        """
        Set the setpoint for the PIDBase.

        :param setpoint: the desired setpoint
        """
    def setTolerance(self, percent: float) -> None: ...
    def setToleranceBuffer(self, bufLength: int = 1) -> None: ...
    @property
    def _m_enabled(self) -> bool:
        """
        :type: bool
        """
    @_m_enabled.setter
    def _m_enabled(self, arg0: bool) -> None:
        pass
    @property
    def _m_pidInput(self) -> PIDSource:
        """
        :type: PIDSource
        """
    @property
    def _m_pidOutput(self) -> PIDOutput:
        """
        :type: PIDOutput
        """
    @property
    def _m_pidWriteMutex(self) -> std::mutex:
        """
        :type: std::mutex
        """
    @property
    def _m_setpointTimer(self) -> wpilib._wpilib.Timer:
        """
        :type: wpilib._wpilib.Timer
        """
    @property
    def _m_thisMutex(self) -> std::mutex:
        """
        :type: std::mutex
        """
    pass
class PIDEncoder(PIDSource, wpilib._wpilib.Encoder, wpilib.interfaces._interfaces.CounterBase, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for Encoder for old PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Get the PIDOutput for the PIDSource base object. Can be set to return
        distance or rate using SetPIDSourceType(). Defaults to distance.

        :returns: The PIDOutput (distance or rate, defaults to distance)
        """
    @typing.overload
    def __init__(self, arg0: int, arg1: int, arg2: bool, arg3: wpilib.interfaces._interfaces.CounterBase.EncodingType) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.DigitalSource, arg1: wpilib._wpilib.DigitalSource, arg2: bool, arg3: wpilib.interfaces._interfaces.CounterBase.EncodingType) -> None: ...
    pass
class PIDController(PIDBase, PIDInterface, PIDOutput, wpiutil._wpiutil.Sendable):
    """
    Class implements a PID Control Loop.

    Creates a separate thread which reads the given PIDSource and takes care of
    the integral calculations, as well as writing the given PIDOutput.

    This feedback controller runs in discrete time, so time deltas are not used
    in the integral and derivative calculations. Therefore, the sample rate
    affects the controller's behavior for a given set of PID constants.

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead.
    """
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, source: PIDSource, output: PIDOutput, period: float = 0.05) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, source: PIDSource, output: PIDOutput, period: float = 0.05) -> None: ...
    def disable(self) -> None: 
        """
        Stop running the PIDController, this sets the output to zero before
        stopping.
        """
    def enable(self) -> None: 
        """
        Begin running the PIDController.
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def isEnabled(self) -> bool: 
        """
        Return true if PIDController is enabled.
        """
    def reset(self) -> None: 
        """
        Reset the previous error, the integral term, and disable the controller.
        """
    def setEnabled(self, enable: bool) -> None: 
        """
        Set the enabled state of the PIDController.
        """
    pass
class PIDMotorController(PIDOutput, wpilib.interfaces._interfaces.MotorController, wpilib.interfaces._interfaces.SpeedController, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDOutput is implemented for MotorController for old
    PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDWrite(self, output: float) -> None: ...
    def __init__(self, motorController: wpilib.interfaces._interfaces.MotorController) -> None: ...
    def _initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def disable(self) -> None: ...
    def get(self) -> float: 
        """
        Get the recently set value of the PWM. This value is affected by the
        inversion property. If you want the value that is sent directly to the
        MotorController, use PWM::GetSpeed() instead.

        :returns: The most recently set value for the PWM between -1.0 and 1.0.
        """
    def getInverted(self) -> bool: ...
    def set(self, value: float) -> None: 
        """
        Set the PWM value.

        The PWM value is set using a range of -1.0 to 1.0, appropriately scaling
        the value for the FPGA.

        :param value: The speed value between -1.0 and 1.0 to set.
        """
    def setInverted(self, isInverted: bool) -> None: ...
    def stopMotor(self) -> None: ...
    pass
class PIDCommand(Command, wpiutil._wpiutil.Sendable, PIDOutput, PIDSource):
    """
    This class defines aCommand which interacts heavily with a PID loop.

    It provides some convenience methods to run an internal PIDController . It
    will also start and stop said PIDController when the PIDCommand is first
    initialized and ended/interrupted.

    This class is provided by the OldCommands VendorDep
    """
    def PIDGet(self) -> float: ...
    def PIDWrite(self, output: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, subsystem: Subsystem) -> None: ...
    def _end(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def getPIDController(self) -> None: ...
    def getPosition(self) -> float: ...
    def getSetpoint(self) -> float: ...
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def returnPIDInput(self) -> float: ...
    def setSetpoint(self, setpoint: float) -> None: ...
    def setSetpointRelative(self, deltaSetpoint: float) -> None: ...
    def usePIDOutput(self, output: float) -> None: ...
    pass
class PIDAnalogAccelerometer(PIDSource, wpilib._wpilib.AnalogAccelerometer, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for AnalogAccelerometer for old
    PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Get the Acceleration for the PID Source parent.

        :returns: The current acceleration in Gs.
        """
    @typing.overload
    def __init__(self, arg0: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.AnalogInput) -> None: ...
    pass
class Subsystem(wpiutil._wpiutil.Sendable):
    """
    This class defines a major component of the robot.

    A good example of a subsystem is the drivetrain, or a claw if the robot has
    one.

    All motors should be a part of a subsystem. For instance, all the wheel
    motors should be a part of some kind of "Drivetrain" subsystem.

    Subsystems are used within the command system as requirements for Command.
    Only one command which requires a subsystem can run at a time. Also,
    subsystems can have default commands which are started if there is no command
    running which requires this subsystem.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self, name: str) -> None: 
        """
        Creates a subsystem with the given name.

        :param name: the name of the subsystem
        """
    @typing.overload
    def addChild(self, child: wpiutil._wpiutil.Sendable) -> None: 
        """
        Associate a Sendable with this Subsystem.
        Also update the child's name.

        :param name:  name to give child
        :param child: sendable

        Associate a Sendable with this Subsystem.

        :param child: sendable
        """
    @typing.overload
    def addChild(self, name: str, child: wpiutil._wpiutil.Sendable) -> None: ...
    def getCurrentCommand(self) -> Command: 
        """
        Returns the command which currently claims this subsystem.

        :returns: the command which currently claims this subsystem
        """
    def getCurrentCommandName(self) -> str: 
        """
        Returns the current command name, or empty string if no current command.

        :returns: the current command name
        """
    def getDefaultCommand(self) -> Command: 
        """
        Returns the default command (or null if there is none).

        :returns: the default command
        """
    def getDefaultCommandName(self) -> str: 
        """
        Returns the default command name, or empty string is there is none.

        :returns: the default command name
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
    def initDefaultCommand(self) -> None: 
        """
        Initialize the default command for this subsystem.

        This is meant to be the place to call SetDefaultCommand in a subsystem and
        will be called on all the subsystems by the CommandBase method before the
        program starts running by using the list of all registered Subsystems
        inside the Scheduler.

        This should be overridden by a Subsystem that has a default Command
        """
    def initSendable(self, builder: wpiutil._wpiutil.SendableBuilder) -> None: ...
    def periodic(self) -> None: 
        """
        When the run method of the scheduler is called this method will be called.
        """
    def setCurrentCommand(self, command: Command) -> None: 
        """
        Sets the current command.

        :param command: the new current command
        """
    def setDefaultCommand(self, command: Command) -> None: 
        """
        Sets the default command. If this is not called or is called with null,
        then there will be no default command for the subsystem.

        **WARNING:** This should **NOT** be called in a constructor if the
        subsystem is a singleton.

        :param command: the default command (or null if there should be none)
        """
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Subsystem.

        :param name: name
        """
    def setSubsystem(self, subsystem: str) -> None: 
        """
        Sets the subsystem name of this Subsystem.

        :param subsystem: subsystem name
        """
    pass
class PIDUltrasonic(PIDSource, wpilib._wpilib.Ultrasonic, wpiutil._wpiutil.Sendable):
    """
    Wrapper so that PIDSource is implemented for Ultrasonic for old PIDController

    This class is provided by the OldCommands VendorDep

    :deprecated: Use frc2::PIDController class instead which doesn't require this
                 wrapper.
    """
    def PIDGet(self) -> float: 
        """
        Get the range for the PIDSource base object.

        :returns: The range
        """
    @typing.overload
    def __init__(self, arg0: int, arg1: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: wpilib._wpilib.DigitalOutput, arg1: wpilib._wpilib.DigitalInput) -> None: ...
    pass
class PrintCommand(InstantCommand, Command, wpiutil._wpiutil.Sendable):
    """
    A PrintCommand is a command which prints out a string when it is initialized,
    and then immediately finishes. It is useful if you want a CommandGroup to
    print out a string when it reaches a certain point.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self, message: str) -> None: ...
    def initialize(self) -> None: ...
    pass
class Scheduler(_pyntcore._ntcore.NTSendable, wpiutil._wpiutil.Sendable):
    """
    The Scheduler is a singleton which holds the top-level running commands. It
    is in charge of both calling the command's run() method and to make sure that
    there are no two commands with conflicting requirements running.

    It is fine if teams wish to take control of the Scheduler themselves, all
    that needs to be done is to call frc::Scheduler::getInstance()->run() often
    to have Commands function correctly. However, this is already done for you if
    you use the CommandBased Robot template.

    This class is provided by the OldCommands VendorDep
    """
    def addButton(self, button: commands1._impl._commands_v1.button.ButtonScheduler) -> None: ...
    def addCommand(self, command: Command) -> None: 
        """
        Add a command to be scheduled later.

        In any pass through the scheduler, all commands are added to the additions
        list, then at the end of the pass, they are all scheduled.

        :param command: The command to be scheduled
        """
    @staticmethod
    def addToSmartDashboard(key: str) -> None: 
        """
        This is equivalent to ``wpilib.SmartDashboard.putData(key, Scheduler.getInstance())``.
        Use this instead, as SmartDashboard.putData will fail if used directly

        :param key: the key
        """
    @staticmethod
    def getInstance() -> Scheduler: 
        """
        Returns the Scheduler, creating it if one does not exist.

        :returns: the Scheduler
        """
    def initSendable(self, builder: _pyntcore._ntcore.NTSendableBuilder) -> None: ...
    def registerSubsystem(self, subsystem: Subsystem) -> None: 
        """
        Registers a Subsystem to this Scheduler, so that the Scheduler might know
        if a default Command needs to be run.

        All Subsystems should call this.

        :param subsystem: the system
        """
    def remove(self, command: Command) -> None: 
        """
        Removes the Command from the Scheduler.

        :param command: the command to remove
        """
    def removeAll(self) -> None: ...
    def resetAll(self) -> None: 
        """
        Completely resets the scheduler. Undefined behavior if running.
        """
    def run(self) -> None: 
        """
        Runs a single iteration of the loop.

        This method should be called often in order to have a functioning
        Command system. The loop has five stages:

        <ol>
        - Poll the Buttons
        - Execute/Remove the Commands
        - Send values to SmartDashboard
        - Add Commands
        - Add Defaults
        </ol>
        """
    def setEnabled(self, enabled: bool) -> None: ...
    pass
class StartCommand(InstantCommand, Command, wpiutil._wpiutil.Sendable):
    """
    A PrintCommand is a command which prints out a string when it is initialized,
    and then immediately finishes. It is useful if you want a CommandGroup to
    print out a string when it reaches a certain point.

    This class is provided by the OldCommands VendorDep
    """
    def __init__(self, commandToStart: Command) -> None: ...
    def initialize(self) -> None: ...
    pass
class PIDSubsystem(Subsystem, wpiutil._wpiutil.Sendable, PIDOutput, PIDSource):
    """
    This class is designed to handle the case where there is a Subsystem which
    uses a single PIDController almost constantly (for instance, an elevator
    which attempts to stay at a constant height).

    It provides some convenience methods to run an internal PIDController. It
    also allows access to the internal PIDController in order to give total
    control to the programmer.

    This class is provided by the OldCommands VendorDep
    """
    def PIDGet(self) -> float: ...
    def PIDWrite(self, output: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float) -> None: 
        """
        Instantiates a PIDSubsystem that will use the given P, I, and D values.

        :param name: the name
        :param p:    the proportional value
        :param i:    the integral value
        :param d:    the derivative value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        :param name: the name
        :param p:    the proportional value
        :param i:    the integral value
        :param d:    the derivative value
        :param f:    the feedforward value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will also space the time between PID loop calculations to be equal to
        the given period.

        :param name:   the name
        :param p:      the proportional value
        :param i:      the integral value
        :param d:      the derivative value
        :param f:      the feedfoward value
        :param period: the time (in seconds) between calculations

        Instantiates a PIDSubsystem that will use the given P, I, and D values.

        It will use the class name as its name.

        :param p: the proportional value
        :param i: the integral value
        :param d: the derivative value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will use the class name as its name.

        :param p: the proportional value
        :param i: the integral value
        :param d: the derivative value
        :param f: the feedforward value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will use the class name as its name. It will also space the time
        between PID loop calculations to be equal to the given period.

        :param p:      the proportional value
        :param i:      the integral value
        :param d:      the derivative value
        :param f:      the feedforward value
        :param period: the time (in seconds) between calculations
        """
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float) -> None: ...
    def disable(self) -> None: 
        """
        Disables the internal PIDController.
        """
    def enable(self) -> None: 
        """
        Enables the internal PIDController.
        """
    def getPIDController(self) -> None: 
        """
        Returns the PIDController used by this PIDSubsystem.

        Use this if you would like to fine tune the PID loop.

        :returns: The PIDController used by this PIDSubsystem
        """
    def getPosition(self) -> float: 
        """
        Returns the current position.

        :returns: the current position
        """
    def getRate(self) -> float: 
        """
        Returns the current rate.

        :returns: the current rate
        """
    def getSetpoint(self) -> float: 
        """
        Return the current setpoint.

        :returns: The current setpoint
        """
    def onTarget(self) -> bool: 
        """
        Return true if the error is within the percentage of the total input range,
        determined by SetTolerance().

        This asssumes that the maximum and minimum input were set using SetInput().
        Use OnTarget() in the IsFinished() method of commands that use this
        subsystem.

        Currently this just reports on target as the actual value passes through
        the setpoint. Ideally it should be based on being within the tolerance for
        some period of time.

        :returns: True if the error is within the percentage tolerance of the input
                  range
        """
    def returnPIDInput(self) -> float: ...
    def setAbsoluteTolerance(self, absValue: float) -> None: 
        """
        Set the absolute error which is considered tolerable for use with
        OnTarget.

        :param absValue: absolute error which is tolerable
        """
    def setInputRange(self, minimumInput: float, maximumInput: float) -> None: 
        """
        Sets the maximum and minimum values expected from the input.

        :param minimumInput: the minimum value expected from the input
        :param maximumInput: the maximum value expected from the output
        """
    def setOutputRange(self, minimumOutput: float, maximumOutput: float) -> None: 
        """
        Sets the maximum and minimum values to write.

        :param minimumOutput: the minimum value to write to the output
        :param maximumOutput: the maximum value to write to the output
        """
    def setPercentTolerance(self, percent: float) -> None: 
        """
        Set the percentage error which is considered tolerable for use with
        OnTarget().

        :param percent: percentage error which is tolerable
        """
    def setSetpoint(self, setpoint: float) -> None: 
        """
        Sets the setpoint to the given value.

        If SetRange() was called, then the given setpoint will be trimmed to fit
        within the range.

        :param setpoint: the new setpoint
        """
    def setSetpointRelative(self, deltaSetpoint: float) -> None: 
        """
        Adds the given value to the setpoint.

        If SetRange() was used, then the bounds will still be honored by this
        method.

        :param deltaSetpoint: the change in the setpoint
        """
    def usePIDOutput(self, output: float) -> None: ...
    pass
class TimedCommand(Command, wpiutil._wpiutil.Sendable):
    """
    A TimedCommand will wait for a timeout before finishing.

    TimedCommand is used to execute a command for a given amount of time.

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self, name: str, timeout: seconds) -> None: 
        """
        Creates a new TimedCommand with the given name and timeout.

        :param name:    the name of the command
        :param timeout: the time before this command "times out"

        Creates a new WaitCommand with the given timeout.

        :param timeout: the time before this command "times out"

        Creates a new TimedCommand with the given name and timeout.

        :param name:      the name of the command
        :param timeout:   the time before this command "times out"
        :param subsystem: the subsystem that the command requires

        Creates a new WaitCommand with the given timeout.

        :param timeout:   the time before this command "times out"
        :param subsystem: the subsystem that the command requires
        """
    @typing.overload
    def __init__(self, name: str, timeout: seconds, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, timeout: seconds) -> None: ...
    @typing.overload
    def __init__(self, timeout: seconds, subsystem: Subsystem) -> None: ...
    def isFinished(self) -> bool: 
        """
        Ends command when timed out.
        """
    pass
class WaitCommand(TimedCommand, Command, wpiutil._wpiutil.Sendable):
    """
    A WaitCommand will wait for a certain amount of time before finishing. It is
    useful if you want a CommandGroup to pause for a moment.

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self, name: str, timeout: seconds) -> None: 
        """
        Creates a new WaitCommand with the given name and timeout.

        :param timeout: the time before this command "times out"

        Creates a new WaitCommand with the given timeout.

        :param name:    the name of the command
        :param timeout: the time before this command "times out"
        """
    @typing.overload
    def __init__(self, timeout: seconds) -> None: ...
    pass
class WaitForChildren(Command, wpiutil._wpiutil.Sendable):
    """
    This command will only finish if whatever CommandGroup it is in has no active
    children. If it is not a part of a CommandGroup, then it will finish
    immediately. If it is itself an active child, then the CommandGroup will
    never end.

    This class is useful for the situation where you want to allow anything
    running in parallel to finish, before continuing in the main CommandGroup
    sequence.

    This class is provided by the OldCommands VendorDep
    """
    @typing.overload
    def __init__(self, name: str, timeout: seconds) -> None: ...
    @typing.overload
    def __init__(self, timeout: seconds) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class WaitUntilCommand(Command, wpiutil._wpiutil.Sendable):
    """
    A WaitCommand will wait until a certain match time before finishing.

    This will wait until the game clock reaches some value, then continue to
    the next command.

    This class is provided by the OldCommands VendorDep

    @see CommandGroup
    """
    @typing.overload
    def __init__(self, name: str, time: seconds) -> None: ...
    @typing.overload
    def __init__(self, time: seconds) -> None: ...
    def isFinished(self) -> bool: 
        """
        Check if we've reached the actual finish time.
        """
    pass
