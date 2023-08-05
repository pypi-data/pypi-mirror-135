# pylint: disable=invalid-name
from typing import NamedTuple
import re
from pathlib import Path

__all__ = ("__version__", "version_info")

with Path(__file__).with_name("_version.txt").open("r") as f:
    __version__ = f.readline().strip()


class Version(NamedTuple):
    major: int
    minor: int
    micro: int
    tag: str = None

    @classmethod
    def from_str(cls, s: str) -> "Version":
        m = re.match(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(\w*))?", s)
        major = m.group(1)
        minor = m.group(2)
        micro = m.group(3)
        tag = m.group(4)
        return cls(major, minor, micro, tag=tag)

    def __str__(self) -> str:
        """The full version as X.Y.Z-tag"""
        s = f"{self.major}.{self.minor}.{self.micro}"
        if self.tag is not None:
            s += f"-{self.tag}"
        return s

    def short_version(self) -> str:
        """The short X.Y version"""
        return f"{self.major}.{self.minor}"


version_info = Version.from_str(__version__)
