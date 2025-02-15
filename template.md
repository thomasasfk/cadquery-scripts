# 3D Printable Model Generation Request

## Context and Requirements

I have an abstract base class `PrintableModel` that serves as a template for creating 3D printable objects using CadQuery. I need help implementing a concrete subclass that:

1. Inherits from `PrintableModel`
2. Implements the abstract `create()` method to return a CadQuery workplane object
3. Follows these 3D printing design guidelines:
   - Model should be printable in a single piece
   - No floating or disconnected parts
   - Use appropriate tolerances (0.1-0.3mm)
   - Maintain proper wall thickness (>1.2mm)
4. Sets appropriate parameters as public members in `__init__`

Important implementation notes:
- Do NOT override the `name` or `run` methods - these are pre-implemented
- The `version` attribute must start at 1 and MUST keep the comment about incrementing it
- Always maintain the comment "increment when appropriate" next to the version attribute in all implementations
- Include proper type hints for parameters
- Return a complete, working CadQuery model

## Template Code

```python
import os
from abc import ABC
from abc import abstractmethod

import cadquery as cq
from cadquery.vis import show_object

from utils import export_cad_model_with_docs


class PrintableModel(ABC):
    version: int = 1  # increment when appropriate

    @property
    @abstractmethod
    def name(self) -> str: ...

    def run(self):
        model = self.create()
        if not os.getenv('HIDE_DISPLAY'): show_object(model)
        export_cad_model_with_docs(model, self.name, self.version)

    @abstractmethod
    def create(self) -> cq.Workplane: ...
```

Note, you can implement this using the following:

```python
from template import PrintableModel
```

## Your Task

Please help me create a concrete implementation of this abstract base class for the following 3D printable object:

