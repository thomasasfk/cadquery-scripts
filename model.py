import inspect
import os
import cadquery as cq

from abc import ABC, abstractmethod
from cadquery.vis import show_object

from utils import export_cad_model_with_docs


class PrintableModelBase(ABC):
    @property
    @abstractmethod
    def version(self) -> int: ...

    @abstractmethod
    def create(self) -> cq.Workplane: ...

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
