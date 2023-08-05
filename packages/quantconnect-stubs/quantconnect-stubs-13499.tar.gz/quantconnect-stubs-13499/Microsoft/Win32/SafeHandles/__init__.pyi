import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.IO
import System.Runtime.InteropServices
import System.Threading

Interop_ErrorInfo = typing.Any


class SafeHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class SafeFileHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    DisableFileLocking: bool

    @property
    def IsAsync(self) -> bool:
        ...

    @IsAsync.setter
    def IsAsync(self, value: bool):
        ...

    @property
    def CanSeek(self) -> bool:
        ...

    @property
    def SupportsRandomAccess(self) -> bool:
        ...

    @SupportsRandomAccess.setter
    def SupportsRandomAccess(self, value: bool):
        ...

    @property
    def ThreadPoolBinding(self) -> System.Threading.ThreadPoolBoundHandle:
        ...

    t_lastCloseErrorInfo: typing.Optional[Interop_ErrorInfo]

    @property
    def IsInvalid(self) -> bool:
        ...

    @property
    def Path(self) -> str:
        ...

    NoBuffering: System.IO.FileOptions = ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, preexistingHandle: System.IntPtr, ownsHandle: bool) -> None:
        """
        Creates a Microsoft.Win32.SafeHandles.SafeFileHandle around a file handle.
        
        :param preexistingHandle: Handle to wrap
        :param ownsHandle: Whether to control the handle lifetime
        """
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...


class CriticalHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


class CriticalHandleMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


class SafeHandleMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def IsInvalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class SafeWaitHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @typing.overload
    def __init__(self) -> None:
        """Creates a Microsoft.Win32.SafeHandles.SafeWaitHandle."""
        ...

    @typing.overload
    def __init__(self, existingHandle: System.IntPtr, ownsHandle: bool) -> None:
        """
        Creates a Microsoft.Win32.SafeHandles.SafeWaitHandle around a wait handle.
        
        :param existingHandle: Handle to wrap
        :param ownsHandle: Whether to control the handle lifetime
        """
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...

    @typing.overload
    def ReleaseHandle(self) -> bool:
        """This method is protected."""
        ...


