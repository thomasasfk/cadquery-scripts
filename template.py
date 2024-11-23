import inspect
import os
from abc import ABC
from abc import abstractmethod

import cadquery as cq
from cadquery.vis import show_object

from utils import export_cad_model_with_docs


class PrintableModel(ABC):
    version: int = 1  # increment when appropriate

    @property
    def name(self) -> str:
        impl_file = inspect.getfile(self.__class__)
        basename = os.path.basename(impl_file)
        name, _ = os.path.splitext(basename)
        return name

    def run(self):
        model = self.create()
        if not os.getenv('HIDE_DISPLAY'): show_object(model)
        export_cad_model_with_docs(model, self.name, self.version)

    @abstractmethod
    def create(self) -> cq.Workplane: ...
