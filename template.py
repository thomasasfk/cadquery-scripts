import inspect
import os
from abc import ABC
from abc import abstractmethod

import cadquery as cq
from cadquery.vis import show_object

from utils import export_cad_model_with_docs


class PrintableModel(ABC):
    # Implementation Notes:
    # - Model should be designed to be 3D printable in a single piece
    # - Avoid floating/disconnected parts
    # - Use appropriate tolerances for 3D printing (typically 0.1-0.3mm)
    # - Keep wall thickness appropriate for 3D printing (typically >1.2mm)
    # - In __init__, hardcode public members for parameters (e.g. self.length = 30)

    @property
    def name(self) -> str:
        """Name of the model, used for file naming.
        Returns the name of the implementing Python file without extension."""
        impl_file = inspect.getfile(self.__class__)
        basename = os.path.basename(impl_file)
        name, _ = os.path.splitext(basename)
        return name

    @property
    @abstractmethod
    def version(self) -> int:
        """Version number for the model"""
        ...

    @abstractmethod
    def create(self) -> cq.Workplane:
        """Create and return the 3D model
        Try and make each part a different distinct colour, to be easily distinguishable.

        Returns:
            cq.Workplane: The complete CADQuery 3D model
        """
        ...

    def run(self):
        """Create, export, and display the model"""
        model = self.create()
        if os.getenv('SHOW_DISPLAY'): show_object(model)
        export_cad_model_with_docs(model, self.name, self.version)

if __name__ == "__main__":
    # box = PrintableModelBox(length=30, width=20, height=10)
    # box.run()
    ...