from template import PrintableModel
import cadquery as cq


class iPadStand(PrintableModel):
    def __init__(
        self,
        ipad_length=280.6,
        ipad_width=214.9,
        ipad_thickness=6.4,
        clearance=0.5,
        wall_thickness=2.0,
        lip_height=10.0,
        grip_gap=0.2,
        base_width=140,
        base_length=120,
        base_height=8,
        spacer_width=60,
        spacer_length=40,
        spacer_height=25
    ):
        # iPad and clearance parameters
        self._ipad_length = ipad_length
        self._ipad_width = ipad_width
        self._ipad_thickness = ipad_thickness
        self._clearance = clearance
        self._wall_thickness = wall_thickness
        self._lip_height = lip_height
        self._grip_gap = grip_gap

        # Base parameters
        self._base_width = base_width
        self._base_length = base_length
        self._base_height = base_height

        # Spacer parameters
        self._spacer_width = spacer_width
        self._spacer_length = spacer_length
        self._spacer_height = spacer_height

        # Calculated parameters
        self._total_mount_width = self._ipad_width + (2 * self._wall_thickness) + (2 * self._clearance)
        self._connection_offset = self._total_mount_width / 6

    @property
    def version(self) -> int:
        return 1

    @property
    def parameters(self) -> dict:
        return {
            "ipad_length": self._ipad_length,
            "ipad_width": self._ipad_width,
            "ipad_thickness": self._ipad_thickness,
            "clearance": self._clearance,
            "wall_thickness": self._wall_thickness,
            "lip_height": self._lip_height,
            "grip_gap": self._grip_gap,
            "base_width": self._base_width,
            "base_length": self._base_length,
            "base_height": self._base_height,
            "spacer_width": self._spacer_width,
            "spacer_length": self._spacer_length,
            "spacer_height": self._spacer_height,
            "total_mount_width": self._total_mount_width,
            "connection_offset": self._connection_offset,
            "total_height": self._base_height + self._spacer_height + self._wall_thickness + self._lip_height
        }

    def _create_base(self) -> cq.Workplane:
        return (
            cq.Workplane("XY")
            .rect(self._base_width, self._base_length)
            .extrude(self._base_height)
            .edges("|Z")
            .fillet(3.0)
        )

    def _create_spacer(self, base: cq.Workplane) -> cq.Workplane:
        spacer = (
            cq.Workplane("XY")
            .rect(self._spacer_width, self._spacer_length)
            .extrude(self._spacer_height)
            .edges("|Z")
            .fillet(2.0)
            .translate((0, 0, self._base_height))
        )
        return base.union(spacer)

    def _create_mount(self, assembly: cq.Workplane) -> cq.Workplane:
        # Create mount base plate
        mount_base = (
            cq.Workplane("XY")
            .rect(self._total_mount_width, self._spacer_length)
            .extrude(self._wall_thickness)
            .translate((self._connection_offset, 0, self._base_height + self._spacer_height))
        )

        # Create side lips
        lip_thickness = self._wall_thickness + self._grip_gap

        left_lip = (
            cq.Workplane("XY")
            .rect(lip_thickness, self._spacer_length)
            .extrude(self._lip_height)
            .translate(
                (
                    self._connection_offset - self._total_mount_width / 2 + lip_thickness / 2,
                    0,
                    self._base_height + self._spacer_height + self._wall_thickness
                )
            )
        )

        right_lip = (
            cq.Workplane("XY")
            .rect(lip_thickness, self._spacer_length)
            .extrude(self._lip_height)
            .translate(
                (
                    self._connection_offset + self._total_mount_width / 2 - lip_thickness / 2,
                    0,
                    self._base_height + self._spacer_height + self._wall_thickness
                )
            )
        )

        return assembly.union(mount_base).union(left_lip).union(right_lip)

    def create(self) -> cq.Workplane:
        base = self._create_base()
        with_spacer = self._create_spacer(base)
        return self._create_mount(with_spacer)


if __name__ == "__main__":
    stand = iPadStand()
    stand.run()