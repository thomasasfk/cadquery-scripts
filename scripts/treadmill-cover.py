from dataclasses import dataclass
from typing import Tuple, List

import cadquery as cq

from template import PrintableModel


@dataclass
class HoleSpec:
    width: float  # in mm
    height: float  # in mm
    position: Tuple[float, float]  # (x, y) coordinates in mm


class SimplePlate(PrintableModel):
    version: int = 1

    def __init__(
            self,
            length: float = 156.35,
            width: float = 77.63,
            base_thickness: float = 3.0,  # Base plate thickness
            total_thickness: float = 6.0,  # Total thickness within base dimensions
            hole_clearance: float = 0.2,
            edge_clearance: float = 1.5,
            lip_extension: float = 1.5,  # Consistent lip extension all around
            bottom_lip: float = 0.5,  # New parameter for bottom lip
            rim_thickness: float = 1.0,  # Thickness of the rim inside holes
            rim_depth: float = 1.0,  # How deep the rim goes into the hole
    ):
        self.length = length
        self.width = width
        self.base_thickness = base_thickness
        self.total_thickness = total_thickness
        self.hole_clearance = hole_clearance
        self.edge_clearance = edge_clearance
        self.lip_extension = lip_extension
        self.bottom_lip = bottom_lip
        self.rim_thickness = rim_thickness
        self.rim_depth = rim_depth
        self.upper_section_height = self.total_thickness - self.base_thickness

        # Calculate dimensions with lip
        self.top_layer_length = self.length + (self.lip_extension * 2)
        self.top_layer_width = self.width + (self.lip_extension * 2)

        # Calculate the additional height for bottom holes
        bottom_hole_extension = self.lip_extension - self.bottom_lip

        self.holes = [
            # Top left hole
            HoleSpec(
                width=(0.425 * self.length) + hole_clearance,
                height=(0.248 * self.width) + hole_clearance,
                position=(
                    -self.length / 2 + self.edge_clearance + ((0.425 * self.length) + hole_clearance) / 2,
                    self.width / 2 - self.edge_clearance - ((0.287 * self.width) + hole_clearance) / 2
                ),
            ),
            # Top right hole
            HoleSpec(
                width=(0.425 * self.length) + hole_clearance,
                height=(0.248 * self.width) + hole_clearance,
                position=(
                    self.length / 2 - self.edge_clearance - ((0.425 * self.length) + hole_clearance) / 2,
                    self.width / 2 - self.edge_clearance - ((0.287 * self.width) + hole_clearance) / 2
                ),
            ),
            # Bottom left hole
            HoleSpec(
                width=(0.269 * self.length) + hole_clearance,
                height=(0.208 * self.width) + hole_clearance + bottom_hole_extension,
                position=(
                    -self.length / 2 + self.edge_clearance + ((0.269 * self.length) + hole_clearance) / 2,
                    -self.width / 2 + self.edge_clearance + (
                                (0.214 * self.width) + hole_clearance) / 2 - bottom_hole_extension / 2
                ),
            ),
            # Bottom middle hole
            HoleSpec(
                width=(0.373 * self.length) + hole_clearance,
                height=(0.208 * self.width) + hole_clearance + bottom_hole_extension,
                position=(
                    0,
                    -self.width / 2 + self.edge_clearance + (
                                (0.214 * self.width) + hole_clearance) / 2 - bottom_hole_extension / 2
                ),
            ),
            # Bottom right hole
            HoleSpec(
                width=(0.269 * self.length) + hole_clearance,
                height=(0.208 * self.width) + hole_clearance + bottom_hole_extension,
                position=(
                    self.length / 2 - self.edge_clearance - ((0.269 * self.length) + hole_clearance) / 2,
                    -self.width / 2 + self.edge_clearance + (
                                (0.214 * self.width) + hole_clearance) / 2 - bottom_hole_extension / 2
                ),
            ),
        ]

    @property
    def name(self) -> str:
        return "treadmil-cover"

    def create(self) -> cq.Workplane:
        # Create base plate
        base = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.base_thickness)
            .translate((0, 0, self.base_thickness / 2))
        )

        # Create upper section within base dimensions
        upper = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.upper_section_height)
            .translate((0, 0, self.base_thickness + self.upper_section_height / 2))
        )

        # Create the top layer with consistent lip all around
        top_with_lip = (
            cq.Workplane("XY")
            .box(self.top_layer_length, self.top_layer_width, self.upper_section_height)
            .translate((0, 0, self.base_thickness + self.upper_section_height / 2))
        )

        # Combine base, upper, and top with lip
        result = base.union(upper).union(top_with_lip)

        # Cut holes with rims
        for hole in self.holes:
            # Cut the main hole but not all the way through (leave rim_depth at bottom)
            result = (
                result
                .faces(">Z")
                .workplane()
                .pushPoints([hole.position])
                .rect(hole.width, hole.height)
                .cutBlind(-(self.total_thickness - self.rim_depth))
            )

            # Cut the inner hole (smaller by rim_thickness) all the way through
            result = (
                result
                .faces(">Z")
                .workplane()
                .pushPoints([hole.position])
                .rect(hole.width - (self.rim_thickness * 2), hole.height - (self.rim_thickness * 2))
                .cutThruAll()
            )

        return result

class HoleCover(PrintableModel):
    version: int = 1
    custom_name: str

    def __init__(
            self,
            hole_width: float,
            hole_height: float,
            plate_thickness: float = 6.0,  # Total plate thickness
            rim_depth: float = 1.0,  # Depth of the rim that catches the cover
            clearance: float = 0.15,
            handle_height: float = 8.0,
            handle_width: float = 15.0,
            handle_thickness: float = 4.0,
    ):
        self.hole_width = hole_width
        self.hole_height = hole_height
        self.cover_thickness = plate_thickness - rim_depth  # Cover sits on the rim
        self.clearance = clearance
        self.handle_height = handle_height
        self.handle_width = handle_width
        self.handle_thickness = handle_thickness

        # Calculate insert dimensions (slightly smaller than hole for snug fit)
        self.insert_width = hole_width - (clearance * 2)
        self.insert_height = hole_height - (clearance * 2)

    @property
    def name(self) -> str:
        return self.custom_name

    def create(self) -> cq.Workplane:
        # Create the main cover body that fits inside the hole
        cover = (
            cq.Workplane("XY")
            .box(self.insert_width, self.insert_height, self.cover_thickness)
            .translate((0, 0, self.cover_thickness / 2))
        )

        # Create a chamfered pull handle on top
        handle = (
            cq.Workplane("XY")
            .rect(self.handle_width, self.handle_thickness)
            .extrude(self.handle_height)
            .edges(">Z")
            .chamfer(0.5)
            .translate((0, 0, self.cover_thickness))
        )

        # Combine parts
        result = cover.union(handle)

        return result

if __name__ == "__main__":
    # Create the main plate
    plate_model = SimplePlate()
    main_plate = plate_model.run()

    # Create covers for each hole
    covers = []

    # Top left and right holes
    top_cover = HoleCover(
        hole_width=(0.425 * 156.35) + 0.2,
        hole_height=(0.248 * 77.63) + 0.2,
        plate_thickness=6.0,  # Match SimplePlate's total_thickness
        rim_depth=1.0,  # Match SimplePlate's rim_depth
    )
    top_cover.custom_name = "top_cover"
    covers.extend([top_cover.run(), top_cover.run()])

    # Bottom left and right holes
    bottom_side_cover = HoleCover(
        hole_width=(0.269 * 156.35) + 0.2,
        hole_height=(0.208 * 77.63) + 0.2 + 1.0,
        plate_thickness=6.0,
        rim_depth=1.0,
    )
    bottom_side_cover.custom_name = "bottom_side_cover"
    covers.extend([bottom_side_cover.run(), bottom_side_cover.run()])

    # Bottom middle hole
    bottom_middle_cover = HoleCover(
        hole_width=(0.373 * 156.35) + 0.2,
        hole_height=(0.208 * 77.63) + 0.2 + 1.0,
        plate_thickness=6.0,
        rim_depth=1.0,
    )
    bottom_middle_cover.custom_name = "bottom_middle_cover"
    covers.append(bottom_middle_cover.run())