import cadquery as cq

from template import PrintableModel


class MountingPlate(PrintableModel):
    """A 3D printable mounting plate with holes and circular mount.

    Features:
    - Rectangular base plate with four corner mounting holes
    - Center rectangular cutout
    - Wire gap at bottom
    - Circular mounting area with wall
    """

    def __init__(self):
        # Base plate parameters (mm)
        self.hole_spacing_length = 101.0
        self.hole_spacing_width = 61.0
        self.hole_diameter = 6.0
        self.edge_padding = 5.0
        self.plate_thickness = 2.5

        # Center cutout parameters
        self.center_hole_padding = 10.0

        # Wire gap parameters
        self.wire_gap_width = 8.0
        self.wire_gap_height = 50.0

        # Circular mount parameters
        self.circle_diameter = 100.5
        self.mount_wall_thickness = 2.0
        self.mount_height = 8.0
        self.mount_tolerance = 0.2

        # Derived dimensions
        self.total_length = self.hole_spacing_length + (2 * self.edge_padding)
        self.total_width = self.hole_spacing_width + (2 * self.edge_padding)
        self.cutout_length = self.hole_spacing_length - (2 * self.center_hole_padding)
        self.cutout_width = self.hole_spacing_width - (2 * self.center_hole_padding)

    @property
    def version(self) -> int:
        return 1

    def _create_base_plate(self) -> cq.Workplane:
        """Create the base rectangular plate."""
        return (cq.Workplane("XY")
                .box(self.total_length, self.total_width, self.plate_thickness))

    def _add_mounting_holes(self, plate: cq.Workplane) -> cq.Workplane:
        """Add the four corner mounting holes."""
        hole_positions = [
            (self.hole_spacing_length / 2, self.hole_spacing_width / 2),  # Top Right
            (-self.hole_spacing_length / 2, self.hole_spacing_width / 2),  # Top Left
            (-self.hole_spacing_length / 2, -self.hole_spacing_width / 2),  # Bottom Left
            (self.hole_spacing_length / 2, -self.hole_spacing_width / 2),  # Bottom Right
        ]

        result = plate
        for x, y in hole_positions:
            result = (result.faces(">Z")
                      .workplane()
                      .moveTo(x, y)
                      .hole(self.hole_diameter))
        return result

    def _add_center_cutout(self, plate: cq.Workplane) -> cq.Workplane:
        """Add the rectangular center cutout."""
        return (plate.faces(">Z")
                .workplane()
                .rect(self.cutout_length, self.cutout_width)
                .cutThruAll())

    def _create_wire_gap(self) -> cq.Workplane:
        """Create the wire gap cutout for the bottom edge."""
        return (cq.Workplane("XY")
                .workplane(offset=-self.plate_thickness / 2)
                .moveTo(0, -self.total_width / 2)
                .rect(self.wire_gap_width, self.wire_gap_height * 2)
                .extrude(self.plate_thickness))

    def _create_circular_mount(self) -> cq.Workplane:
        """Create the circular mounting area with wire gap, trimmed to base plate boundaries."""
        # Create main circular mount
        mount_offset = self.plate_thickness - 3.5
        outer_circle = (cq.Workplane("XY")
                        .workplane(offset=mount_offset)
                        .circle((self.circle_diameter + 2 * self.mount_wall_thickness) / 2)
                        .circle((self.circle_diameter + self.mount_tolerance) / 2)
                        .extrude(self.mount_height + 5))

        # Create and cut wire gap
        circle_wire_gap = (cq.Workplane("XY")
                           .workplane(offset=mount_offset)
                           .moveTo(0, -(self.circle_diameter + 2 * self.mount_wall_thickness) / 2)
                           .rect(self.wire_gap_width, self.wire_gap_height)
                           .extrude(self.mount_height + 5))

        # Create bounding box to trim the circular mount
        bounding_box = (cq.Workplane("XY")
                        .workplane(offset=mount_offset)
                        .rect(self.total_length, self.total_width)
                        .extrude(self.mount_height + 5))

        # Trim the circular mount to the base plate boundaries
        trimmed_mount = outer_circle.intersect(bounding_box)

        # Cut the wire gap from the trimmed mount
        return trimmed_mount.cut(circle_wire_gap)

    def create(self) -> cq.Workplane:
        """Create the complete mounting plate model."""
        # Create base plate with holes and cutout
        result = self._create_base_plate()
        result = self._add_mounting_holes(result)
        result = self._add_center_cutout(result)

        # Cut wire gap
        wire_gap = self._create_wire_gap()
        result = result.cut(wire_gap)

        # Add circular mount
        circular_mount = self._create_circular_mount()
        result = result.union(circular_mount)

        return result


if __name__ == "__main__":
    plate = MountingPlate()
    plate.run()