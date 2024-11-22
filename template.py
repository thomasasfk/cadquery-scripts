from abc import ABC
from abc import abstractmethod

import cadquery as cq

from model import PrintableModelBase


class PrintableModel(PrintableModelBase, ABC):
    # Implementation Notes:
    # - Model should be designed to be 3D printable in a single piece
    # - Avoid floating/disconnected parts
    # - Use appropriate tolerances for 3D printing (typically 0.1-0.3mm)
    # - Keep wall thickness appropriate for 3D printing (typically >1.2mm)
    # - In __init__, hardcode public members for parameters (e.g. self.length = 30)

    @property
    @abstractmethod
    def version(self) -> int: ...

    @abstractmethod
    def create(self) -> cq.Workplane: ...


if __name__ == "__main__":
    # box = PrintableModelBox(length=30, width=20, height=10)
    # box.run()
    ...
