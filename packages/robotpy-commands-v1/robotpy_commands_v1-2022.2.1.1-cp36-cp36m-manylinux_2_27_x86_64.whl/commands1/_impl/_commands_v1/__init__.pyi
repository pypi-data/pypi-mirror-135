import commands1._impl._commands_v1
import typing

__all__ = [
    "PIDSourceType",
    "button",
    "command"
]


class PIDSourceType():
    """
    Members:

      kDisplacement

      kRate
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
    __members__: dict # value = {'kDisplacement': <PIDSourceType.kDisplacement: 0>, 'kRate': <PIDSourceType.kRate: 1>}
    kDisplacement: commands1._impl._commands_v1.PIDSourceType # value = <PIDSourceType.kDisplacement: 0>
    kRate: commands1._impl._commands_v1.PIDSourceType # value = <PIDSourceType.kRate: 1>
    pass
