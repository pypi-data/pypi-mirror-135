import datetime
import typing

import System
import System.Diagnostics
import System.Reflection

System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T = typing.TypeVar("System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T")
System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T = typing.TypeVar("System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T")


class StackFrame(System.Object):
    """There is no good reason for the methods of this class to be virtual."""

    OFFSET_UNKNOWN: int = -1
    """Constant returned when the native or IL offset is unknown"""

    @property
    def IsLastFrameFromForeignExceptionStackTrace(self) -> bool:
        ...

    @typing.overload
    def __init__(self) -> None:
        """Constructs a StackFrame corresponding to the active stack frame."""
        ...

    @typing.overload
    def __init__(self, needFileInfo: bool) -> None:
        """Constructs a StackFrame corresponding to the active stack frame."""
        ...

    @typing.overload
    def __init__(self, skipFrames: int) -> None:
        """Constructs a StackFrame corresponding to a calling stack frame."""
        ...

    @typing.overload
    def __init__(self, skipFrames: int, needFileInfo: bool) -> None:
        """Constructs a StackFrame corresponding to a calling stack frame."""
        ...

    @typing.overload
    def __init__(self, fileName: str, lineNumber: int) -> None:
        """
        Constructs a "fake" stack frame, just containing the given file
        name and line number.  Use when you don't want to use the
        debugger's line mapping logic.
        """
        ...

    @typing.overload
    def __init__(self, fileName: str, lineNumber: int, colNumber: int) -> None:
        """
        Constructs a "fake" stack frame, just containing the given file
        name, line number and column number.  Use when you don't want to
        use the debugger's line mapping logic.
        """
        ...

    def GetFileColumnNumber(self) -> int:
        """
        Returns the column number in the line containing the code being executed.
        This information is normally extracted from the debugging symbols
        for the executable.
        """
        ...

    def GetFileLineNumber(self) -> int:
        """
        Returns the line number in the file containing the code being executed.
        This information is normally extracted from the debugging symbols
        for the executable.
        """
        ...

    def GetFileName(self) -> str:
        """
        Returns the file name containing the code being executed.  This
        information is normally extracted from the debugging symbols
        for the executable.
        """
        ...

    def GetILOffset(self) -> int:
        """
        Returns the offset from the start of the IL code for the
        method being executed.  This offset may be approximate depending
        on whether the jitter is generating debuggable code or not.
        """
        ...

    def GetMethod(self) -> System.Reflection.MethodBase:
        """Returns the method the frame is executing"""
        ...

    def GetNativeOffset(self) -> int:
        """
        Returns the offset from the start of the native (jitted) code for the
        method being executed
        """
        ...

    def ToString(self) -> str:
        """Builds a readable representation of the stack frame"""
        ...


class StackTrace(System.Object):
    """
    Class which represents a description of a stack trace
    There is no good reason for the methods of this class to be virtual.
    """

    METHODS_TO_SKIP: int = 0

    @property
    def FrameCount(self) -> int:
        """Property to get the number of frames in the stack trace"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Constructs a stack trace from the current location."""
        ...

    @typing.overload
    def __init__(self, fNeedFileInfo: bool) -> None:
        """Constructs a stack trace from the current location."""
        ...

    @typing.overload
    def __init__(self, skipFrames: int) -> None:
        """
        Constructs a stack trace from the current location, in a caller's
        frame
        """
        ...

    @typing.overload
    def __init__(self, skipFrames: int, fNeedFileInfo: bool) -> None:
        """
        Constructs a stack trace from the current location, in a caller's
        frame
        """
        ...

    @typing.overload
    def __init__(self, e: System.Exception) -> None:
        """Constructs a stack trace from the current location."""
        ...

    @typing.overload
    def __init__(self, e: System.Exception, fNeedFileInfo: bool) -> None:
        """Constructs a stack trace from the current location."""
        ...

    @typing.overload
    def __init__(self, e: System.Exception, skipFrames: int) -> None:
        """
        Constructs a stack trace from the current location, in a caller's
        frame
        """
        ...

    @typing.overload
    def __init__(self, e: System.Exception, skipFrames: int, fNeedFileInfo: bool) -> None:
        """
        Constructs a stack trace from the current location, in a caller's
        frame
        """
        ...

    @typing.overload
    def __init__(self, frame: System.Diagnostics.StackFrame) -> None:
        """
        Constructs a "fake" stack trace, just containing a single frame.
        Does not have the overhead of a full stack trace.
        """
        ...

    def GetFrame(self, index: int) -> System.Diagnostics.StackFrame:
        """
        Returns a given stack frame.  Stack frames are numbered starting at
        zero, which is the last stack frame pushed.
        """
        ...

    def GetFrames(self) -> typing.List[System.Diagnostics.StackFrame]:
        """
        Returns an array of all stack frames for this stacktrace.
        The array is ordered and sized such that GetFrames()[i] == GetFrame(i)
        The nth element of this array is the same as GetFrame(n).
        The length of the array is the same as FrameCount.
        """
        ...

    def ToString(self) -> str:
        """Builds a readable representation of the stack trace"""
        ...


class DebuggerStepperBoundaryAttribute(System.Attribute):
    """Indicates the code following the attribute is to be executed in run, not step, mode."""

    def __init__(self) -> None:
        ...


class ConditionalAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ConditionString(self) -> str:
        ...

    def __init__(self, conditionString: str) -> None:
        ...


class Stopwatch(System.Object):
    """This class has no documentation."""

    Frequency: int = ...

    IsHighResolution: bool = True

    @property
    def IsRunning(self) -> bool:
        ...

    @property
    def Elapsed(self) -> datetime.timedelta:
        ...

    @property
    def ElapsedMilliseconds(self) -> int:
        ...

    @property
    def ElapsedTicks(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    @staticmethod
    def GetTimestamp() -> int:
        ...

    def Reset(self) -> None:
        ...

    def Restart(self) -> None:
        ...

    def Start(self) -> None:
        ...

    @staticmethod
    def StartNew() -> System.Diagnostics.Stopwatch:
        ...

    def Stop(self) -> None:
        ...


class StackFrameExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetNativeImageBase(stackFrame: System.Diagnostics.StackFrame) -> System.IntPtr:
        ...

    @staticmethod
    def GetNativeIP(stackFrame: System.Diagnostics.StackFrame) -> System.IntPtr:
        ...

    @staticmethod
    def HasILOffset(stackFrame: System.Diagnostics.StackFrame) -> bool:
        ...

    @staticmethod
    def HasMethod(stackFrame: System.Diagnostics.StackFrame) -> bool:
        ...

    @staticmethod
    def HasNativeImage(stackFrame: System.Diagnostics.StackFrame) -> bool:
        ...

    @staticmethod
    def HasSource(stackFrame: System.Diagnostics.StackFrame) -> bool:
        ...


class StackTraceHiddenAttribute(System.Attribute):
    """
    Types and Methods attributed with StackTraceHidden will be omitted from the stack trace text shown in StackTrace.ToString()
    and Exception.StackTrace
    """

    def __init__(self) -> None:
        """Initializes a new instance of the StackTraceHiddenAttribute class."""
        ...


class DebuggerStepThroughAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class DebugProvider(System.Object):
    """Provides default implementation for Write and Fail methods in Debug class."""

    s_FailCore: typing.Callable[[str, str, str, str], None]

    s_WriteCore: typing.Callable[[str], None]

    def Fail(self, message: str, detailMessage: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def FailCore(stackTrace: str, message: str, detailMessage: str, errorSource: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def FailCore(stackTrace: str, message: str, detailMessage: str, errorSource: str) -> None:
        ...

    def OnIndentLevelChanged(self, indentLevel: int) -> None:
        ...

    def OnIndentSizeChanged(self, indentSize: int) -> None:
        ...

    def Write(self, message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteCore(message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteCore(message: str) -> None:
        ...

    def WriteLine(self, message: str) -> None:
        ...


class DebuggerTypeProxyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ProxyTypeName(self) -> str:
        ...

    @property
    def Target(self) -> typing.Type:
        ...

    @Target.setter
    def Target(self, value: typing.Type):
        ...

    @property
    def TargetTypeName(self) -> str:
        ...

    @TargetTypeName.setter
    def TargetTypeName(self, value: str):
        ...

    @typing.overload
    def __init__(self, type: typing.Type) -> None:
        ...

    @typing.overload
    def __init__(self, typeName: str) -> None:
        ...


class DebuggerBrowsableState(System.Enum):
    """This class has no documentation."""

    Never = 0

    Collapsed = 2

    RootHidden = 3


class DebuggerBrowsableAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def State(self) -> int:
        """This property contains the int value of a member of the System.Diagnostics.DebuggerBrowsableState enum."""
        ...

    def __init__(self, state: System.Diagnostics.DebuggerBrowsableState) -> None:
        ...


class Debug(System.Object):
    """Provides a set of properties and methods for debugging code."""

    class AssertInterpolatedStringHandler:
        """Provides an interpolated string handler for Debug.Assert that only performs formatting if the assert fails."""

        def __init__(self, literalLength: int, formattedCount: int, condition: bool, shouldAppend: typing.Optional[bool]) -> typing.Union[None, bool]:
            """
            Creates an instance of the handler..
            
            :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
            :param formattedCount: The number of interpolation expressions in the interpolated string.
            :param condition: The condition Boolean passed to the Debug method.
            :param shouldAppend: A value indicating whether formatting should proceed.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T, format: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T, alignment: int) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_AssertInterpolatedStringHandler_T, alignment: int, format: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System.ReadOnlySpan[str]) -> None:
            """
            Writes the specified character span to the handler.
            
            :param value: The span to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System.ReadOnlySpan[str], alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified string of chars to the handler.
            
            :param value: The span to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: str, alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: typing.Any, alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        def AppendLiteral(self, value: str) -> None:
            """
            Writes the specified string to the handler.
            
            :param value: The string to write.
            """
            ...

    class WriteIfInterpolatedStringHandler:
        """Provides an interpolated string handler for Debug.WriteIf and Debug.WriteLineIf that only performs formatting if the condition applies."""

        def __init__(self, literalLength: int, formattedCount: int, condition: bool, shouldAppend: typing.Optional[bool]) -> typing.Union[None, bool]:
            """
            Creates an instance of the handler..
            
            :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
            :param formattedCount: The number of interpolation expressions in the interpolated string.
            :param condition: The condition Boolean passed to the Debug method.
            :param shouldAppend: A value indicating whether formatting should proceed.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T, format: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T, alignment: int) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System_Diagnostics_Debug_AppendFormatted_WriteIfInterpolatedStringHandler_T, alignment: int, format: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System.ReadOnlySpan[str]) -> None:
            """
            Writes the specified character span to the handler.
            
            :param value: The span to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: System.ReadOnlySpan[str], alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified string of chars to the handler.
            
            :param value: The span to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: str, alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        @typing.overload
        def AppendFormatted(self, value: typing.Any, alignment: int = 0, format: str = None) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            :param format: The format string.
            """
            ...

        def AppendLiteral(self, value: str) -> None:
            """
            Writes the specified string to the handler.
            
            :param value: The string to write.
            """
            ...

    AutoFlush: bool

    IndentLevel: int

    IndentSize: int

    @staticmethod
    @typing.overload
    def Assert(condition: bool) -> None:
        ...

    @staticmethod
    @typing.overload
    def Assert(condition: bool, message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Assert(condition: bool, message: System.Diagnostics.Debug.AssertInterpolatedStringHandler) -> None:
        ...

    @staticmethod
    @typing.overload
    def Assert(condition: bool, message: str, detailMessage: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Assert(condition: bool, message: System.Diagnostics.Debug.AssertInterpolatedStringHandler, detailMessage: System.Diagnostics.Debug.AssertInterpolatedStringHandler) -> None:
        ...

    @staticmethod
    @typing.overload
    def Assert(condition: bool, message: str, detailMessageFormat: str, *args: typing.Any) -> None:
        ...

    @staticmethod
    def Close() -> None:
        ...

    @staticmethod
    @typing.overload
    def Fail(message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Fail(message: str, detailMessage: str) -> None:
        ...

    @staticmethod
    def Flush() -> None:
        ...

    @staticmethod
    def Indent() -> None:
        ...

    @staticmethod
    @typing.overload
    def Print(message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Print(format: str, *args: typing.Any) -> None:
        ...

    @staticmethod
    def SetProvider(provider: System.Diagnostics.DebugProvider) -> System.Diagnostics.DebugProvider:
        ...

    @staticmethod
    def Unindent() -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(value: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(message: str, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def Write(value: typing.Any, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, message: System.Diagnostics.Debug.WriteIfInterpolatedStringHandler) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, value: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, message: str, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, message: System.Diagnostics.Debug.WriteIfInterpolatedStringHandler, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteIf(condition: bool, value: typing.Any, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine(message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine(value: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine(value: typing.Any, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine(format: str, *args: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLine(message: str, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, value: typing.Any) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, value: typing.Any, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, message: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, message: System.Diagnostics.Debug.WriteIfInterpolatedStringHandler) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, message: str, category: str) -> None:
        ...

    @staticmethod
    @typing.overload
    def WriteLineIf(condition: bool, message: System.Diagnostics.Debug.WriteIfInterpolatedStringHandler, category: str) -> None:
        ...


class DebuggerDisplayAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Value(self) -> str:
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Target(self) -> typing.Type:
        ...

    @Target.setter
    def Target(self, value: typing.Type):
        ...

    @property
    def TargetTypeName(self) -> str:
        ...

    @TargetTypeName.setter
    def TargetTypeName(self, value: str):
        ...

    def __init__(self, value: str) -> None:
        ...


class DebuggableAttribute(System.Attribute):
    """This class has no documentation."""

    class DebuggingModes(System.Enum):
        """This class has no documentation."""

        # Cannot convert to Python: None = ...

        Default = ...

        DisableOptimizations = ...

        IgnoreSymbolStoreSequencePoints = ...

        EnableEditAndContinue = ...

    @property
    def IsJITTrackingEnabled(self) -> bool:
        ...

    @property
    def IsJITOptimizerDisabled(self) -> bool:
        ...

    @property
    def DebuggingFlags(self) -> int:
        """This property contains the int value of a member of the System.Diagnostics.DebuggableAttribute.DebuggingModes enum."""
        ...

    @typing.overload
    def __init__(self, isJITTrackingEnabled: bool, isJITOptimizerDisabled: bool) -> None:
        ...

    @typing.overload
    def __init__(self, modes: System.Diagnostics.DebuggableAttribute.DebuggingModes) -> None:
        ...


class DebuggerHiddenAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class DebuggerVisualizerAttribute(System.Attribute):
    """
    Signifies that the attributed type has a visualizer which is pointed
    to by the parameter type name strings.
    """

    @property
    def VisualizerObjectSourceTypeName(self) -> str:
        ...

    @property
    def VisualizerTypeName(self) -> str:
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Target(self) -> typing.Type:
        ...

    @Target.setter
    def Target(self, value: typing.Type):
        ...

    @property
    def TargetTypeName(self) -> str:
        ...

    @TargetTypeName.setter
    def TargetTypeName(self, value: str):
        ...

    @typing.overload
    def __init__(self, visualizerTypeName: str) -> None:
        ...

    @typing.overload
    def __init__(self, visualizerTypeName: str, visualizerObjectSourceTypeName: str) -> None:
        ...

    @typing.overload
    def __init__(self, visualizerTypeName: str, visualizerObjectSource: typing.Type) -> None:
        ...

    @typing.overload
    def __init__(self, visualizer: typing.Type) -> None:
        ...

    @typing.overload
    def __init__(self, visualizer: typing.Type, visualizerObjectSource: typing.Type) -> None:
        ...

    @typing.overload
    def __init__(self, visualizer: typing.Type, visualizerObjectSourceTypeName: str) -> None:
        ...


class DebuggerNonUserCodeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


