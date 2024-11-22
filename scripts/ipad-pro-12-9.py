from template import PrintableModel
import cadquery as cq


class IPadPro129Model(PrintableModel):
    def __init__(self):
        self._length = 280.6  # height in mm
        self._width = 214.9  # width in mm
        self._thickness = 6.4  # depth in mm
        self._corner_radius = 7.0
        self._screen_bezel = 8.0
        self._version_num = 1

    @property
    def version(self) -> int:
        return self._version_num

    @property
    def parameters(self) -> dict:
        return {
            "length": self._length,
            "width": self._width,
            "thickness": self._thickness,
            "corner_radius": self._corner_radius,
            "screen_bezel": self._screen_bezel
        }

    def create(self) -> cq.Workplane:
        # Create base body
        ipad = (
            cq.Workplane("XY")
            .rect(self._width, self._length)
            .extrude(self._thickness)
            # Fillet all edges
            .edges("|Z").fillet(self._corner_radius)
        )

        # Add screen area (slight depression)
        screen = (
            cq.Workplane("XY")
            .rect(
                self._width - 2 * self._screen_bezel,
                self._length - 2 * self._screen_bezel
                )
            .extrude(0.2)
            .translate((0, 0, self._thickness - 0.1))
        )

        # Add camera bump (approximate position in top left corner)
        camera_bump = (
            cq.Workplane("XY")
            .rect(25, 28)  # Approximate camera module size
            .extrude(1.5)  # Camera bump height
            .translate(
                (-self._width / 2 + 20, self._length / 2 - 20,
                 self._thickness)
            )  # Position in top left
            .edges("|Z").fillet(3)
        )

        # Combine all features
        result = ipad.union(camera_bump)
        return result


if __name__ == "__main__":
    ipad = IPadPro129Model()
    ipad.run()