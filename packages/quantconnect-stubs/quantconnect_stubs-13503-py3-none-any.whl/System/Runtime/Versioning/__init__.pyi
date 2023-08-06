import typing

import System
import System.Runtime.Versioning

System_Runtime_Versioning_FrameworkName = typing.Any


class TargetFrameworkAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def FrameworkName(self) -> str:
        ...

    @property
    def FrameworkDisplayName(self) -> str:
        ...

    @FrameworkDisplayName.setter
    def FrameworkDisplayName(self, value: str):
        ...

    def __init__(self, frameworkName: str) -> None:
        ...


class ComponentGuaranteesOptions(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Exchange = ...

    Stable = ...

    SideBySide = ...


class ComponentGuaranteesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Guarantees(self) -> int:
        """This property contains the int value of a member of the System.Runtime.Versioning.ComponentGuaranteesOptions enum."""
        ...

    def __init__(self, guarantees: System.Runtime.Versioning.ComponentGuaranteesOptions) -> None:
        ...


class ResourceScope(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Machine = ...

    Process = ...

    AppDomain = ...

    Library = ...

    Private = ...

    Assembly = ...


class ResourceConsumptionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ResourceScope(self) -> int:
        """This property contains the int value of a member of the System.Runtime.Versioning.ResourceScope enum."""
        ...

    @property
    def ConsumptionScope(self) -> int:
        """This property contains the int value of a member of the System.Runtime.Versioning.ResourceScope enum."""
        ...

    @typing.overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...

    @typing.overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope, consumptionScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class FrameworkName(System.Object, System.IEquatable[System_Runtime_Versioning_FrameworkName]):
    """This class has no documentation."""

    @property
    def Identifier(self) -> str:
        ...

    @property
    def Version(self) -> System.Version:
        ...

    @property
    def Profile(self) -> str:
        ...

    @property
    def FullName(self) -> str:
        ...

    @typing.overload
    def __init__(self, identifier: str, version: System.Version) -> None:
        ...

    @typing.overload
    def __init__(self, identifier: str, version: System.Version, profile: str) -> None:
        ...

    @typing.overload
    def __init__(self, frameworkName: str) -> None:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, other: System.Runtime.Versioning.FrameworkName) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class ResourceExposureAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ResourceExposureLevel(self) -> int:
        """This property contains the int value of a member of the System.Runtime.Versioning.ResourceScope enum."""
        ...

    def __init__(self, exposureLevel: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class RequiresPreviewFeaturesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Message(self) -> str:
        """Returns the optional message associated with this attribute instance."""
        ...

    @property
    def Url(self) -> str:
        """Returns the optional URL associated with this attribute instance."""
        ...

    @Url.setter
    def Url(self, value: str):
        """Returns the optional URL associated with this attribute instance."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new instance of the  class."""
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the  class with the specified message.
        
        :param message: An optional message associated with this attribute instance.
        """
        ...


class VersioningHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    @typing.overload
    def MakeVersionSafeName(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope) -> str:
        ...

    @staticmethod
    @typing.overload
    def MakeVersionSafeName(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope, type: typing.Type) -> str:
        ...


