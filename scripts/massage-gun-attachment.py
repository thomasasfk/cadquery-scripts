from template import PrintableModel
import cadquery as cq


class MassageGunAttachment(PrintableModel):
    def __init__(
        self,
        sections=None,
        inner_diameter=15.0,
        ball_diameter=40.0,    # Diameter of the massage ball
        ball_overlap=10.0      # How much the ball overlaps with the cylinder
    ):
        # Default sections if none provided (for the base/mounting part)
        self._sections = sections or [
            {"diameter": 18.75, "length": 11.94},
            {"diameter": 18.95, "length": 2.09},
            {"diameter": 18.82, "length": 5.63},
            {"diameter": 23.70, "length": 1.91},
            {"diameter": 23.25, "length": 30.00}
        ]
        self._inner_diameter = inner_diameter
        self._ball_diameter = ball_diameter
        self._ball_overlap = ball_overlap

    @property
    def version(self) -> int:
        return 2  # Incremented version due to design change

    @property
    def parameters(self) -> dict:
        return {
            "sections": self._sections,
            "inner_diameter": self._inner_diameter,
            "ball_diameter": self._ball_diameter,
            "ball_overlap": self._ball_overlap
        }

    def create(self) -> cq.Workplane:
        # Calculate total length for the base cylinder
        total_length = sum(section["length"] for section in self._sections)

        # Create main cylinder (base)
        current_length = 0
        result = (
            cq.Workplane("XY")
            .circle(self._sections[0]["diameter"] / 2)
            .extrude(self._sections[0]["length"])
        )
        current_length += self._sections[0]["length"]

        # Add remaining sections for the base
        for section in self._sections[1:]:
            new_section = (
                cq.Workplane("XY")
                .circle(section["diameter"] / 2)
                .extrude(section["length"])
                .translate((0, 0, current_length))
            )
            result = result.union(new_section)
            current_length += section["length"]

        # Create the massage ball with increased overlap
        # Position the ball center lower into the cylinder
        ball_position = total_length - self._ball_overlap + (self._ball_diameter / 2)
        ball = (
            cq.Workplane("XY")
            .sphere(self._ball_diameter / 2)
            .translate((0, 0, ball_position))
        )

        # Union the ball with the base
        result = result.union(ball)

        # Create main inner hole
        main_hole = (
            cq.Workplane("XY")
            .circle(self._inner_diameter / 2)
            .extrude(total_length + 1)  # Extend slightly beyond base for clean boolean
        )

        # Subtract the main hole
        result = result.cut(main_hole)

        return result


if __name__ == "__main__":
    # Create with default 10mm overlap
    attachment = MassageGunAttachment()
    attachment.run()