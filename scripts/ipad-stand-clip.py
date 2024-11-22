import cadquery as cq

from template import PrintableModel


class IpadStandClip(PrintableModel):
    """A U-shaped clip for an iPad stand."""

    def __init__(
            self,
            length: float = 15.0,
            height: float = 2.5,
            thickness: float = 4.0,
            slot_width: float = 2.4,
            slot_depth: float = 3.0,
            fillet_radius: float = 0.3
    ):
        """Initialize clip parameters.

        Args:
            length: Length of the clip in mm
            height: Height of the clip in mm
            thickness: Total thickness of clip in mm
            slot_width: Width of the U-slot in mm (slightly larger than lip thickness)
            slot_depth: Depth of the U-slot in mm
            fillet_radius: Radius of edge fillets for printability
        """
        self._length = length
        self._height = height
        self._thickness = thickness
        self._slot_width = slot_width
        self._slot_depth = slot_depth
        self._fillet_radius = fillet_radius
        self._version = 1  # Initial version

    @property
    def version(self) -> int:
        return self._version

    @property
    def parameters(self) -> dict:
        return {
            "length": self._length,
            "height": self._height,
            "thickness": self._thickness,
            "slot_width": self._slot_width,
            "slot_depth": self._slot_depth,
            "fillet_radius": self._fillet_radius
        }

    def create(self) -> cq.Workplane:
        """Create the U-shaped clip model."""
        # Create main body
        main_body = (
            cq.Workplane("XY")
            .rect(self._length, self._thickness)
            .extrude(self._height)
            .edges("|Z")
            .fillet(self._fillet_radius)
        )

        # Create U-shaped cutout
        slot = (
            cq.Workplane("XY")
            .rect(self._length - 2, self._slot_width)
            .extrude(self._height)
            .translate((0, (self._thickness / 2 - self._slot_depth), 0))
        )

        # Subtract slot from body
        clip = main_body.cut(slot)

        return clip


if __name__ == "__main__":
    # Create and run the clip model with default parameters
    clip = IpadStandClip()
    clip.run()