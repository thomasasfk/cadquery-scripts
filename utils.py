from datetime import datetime
from pathlib import Path
from typing import Union, Dict, Tuple
import cadquery as cq


def export_cad_model(
        model: cq.Workplane,
        name: str,
        version: int,
        base_dir: Union[str, Path] = "models",
        views: Dict[str, Tuple[float, float, float]] = None
) -> Path:
    """Export a CAD model to STL and SVG views from different angles.

    Args:
        model: The CadQuery model to export
        name: Name of the model (used for file naming)
        version: Version number
        base_dir: Base directory for exports (default: "models")
        views: Dictionary of view names and their rotation angles (x,y,z).
              If None, uses default views.

    Returns:
        Path: Project directory containing the exported files
    """
    # Convert base_dir to Path if it's a string
    base_dir = Path(base_dir)
    project_dir = base_dir / name
    version_dir = project_dir / f"v{version}"

    # Create directories
    base_dir.mkdir(exist_ok=True)
    project_dir.mkdir(exist_ok=True)
    version_dir.mkdir(exist_ok=True)

    # Export STL
    stl_filename = f"{name}.stl"
    stl_filepath = version_dir / stl_filename
    cq.exporters.export(model, str(stl_filepath))

    # Default views if none provided
    if views is None:
        views = {
            "front": (0, 0, 0),
            # "iso": (45, 45, 45),
            # "top": (0, 90, 0),
            # "right": (0, 0, 90),
            # "left": (0, 0, -90),
        }

    # Export SVGs from different angles
    for view_name, rotation in views.items():
        svg_filepath = version_dir / f"{name}_{view_name}.svg"
        cq.exporters.export(
            model,
            str(svg_filepath),
            exportType="SVG",
            opt={
                "projection": "orthographic",
                "width": 800,
                "height": 600,
                "rotation": rotation,
                "stroke": 2,
            }
        )

    print(f"Model exported to: {stl_filepath}")
    print(f"SVG views exported to: {version_dir}")

    return version_dir


def export_cad_model_with_docs(
        model: cq.Workplane,
        name: str,
        version: int,
        description: str = "",
        base_dir: Union[str, Path] = "models",
        views: Dict[str, Tuple[float, float, float]] = None,
        additional_metadata: Dict[str, str] = None
) -> Path:
    """Export a CAD model to STL and SVG views with markdown documentation.

    Args:
        model: The CadQuery model to export
        name: Name of the model (used for file naming)
        version: Version number
        description: Description of the model/part
        base_dir: Base directory for exports (default: "models")
        views: Dictionary of view names and their rotation angles (x,y,z).
              If None, uses default views.
        additional_metadata: Optional dictionary of additional metadata to include

    Returns:
        Path: Project directory containing the exported files
    """
    # First export the model and get the version directory
    version_dir = export_cad_model(model, name, version, base_dir, views)

    # Default views if none provided (matching export_cad_model)
    if views is None:
        views = {
            "front": (0, 0, 0),
            # "iso": (45, 45, 45),
            # "top": (0, 90, 0),
            # "right": (0, 0, 90),
            # "left": (0, 0, -90),
        }

    # Create markdown documentation
    doc_filename = version_dir / f"{name}.md"

    with doc_filename.open('w') as f:
        # Header
        f.write(f"# {name} (v{version})\n\n")

        # Description
        if description:
            f.write(f"## Description\n{description}\n\n")

        # Metadata
        f.write("## Metadata\n\n")
        f.write(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Model Name:** {name}\n")
        f.write(f"- **Version:** {version}\n")

        if additional_metadata:
            for key, value in additional_metadata.items():
                f.write(f"- **{key}:** {value}\n")
        f.write("\n")

        # Files Section
        f.write("## Generated Files\n\n")
        stl_filename = f"{name}.stl"
        f.write(f"- STL File: [{stl_filename}](./{stl_filename})\n")
        f.write("- SVG Views:\n")

        # Create SVG gallery section
        f.write("\n## Model Views\n\n")

        # Create a grid layout for the SVGs
        for view_name in views.keys():
            svg_filename = f"{name}_{view_name}.svg"
            f.write(f"### {view_name.title()} View\n")
            f.write(f"![](./{svg_filename})\n\n")

        # Add bounding box information if available
        try:
            bbox = model.val().BoundingBox()
            f.write("## Model Dimensions\n\n")
            f.write("```\n")
            f.write(f"X: {bbox.xlen:.2f} mm\n")
            f.write(f"Y: {bbox.ylen:.2f} mm\n")
            f.write(f"Z: {bbox.zlen:.2f} mm\n")
            f.write("```\n")
        except:
            pass

    print(f"Documentation generated: {doc_filename}")
    return version_dir