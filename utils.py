from datetime import datetime
from pathlib import Path
from typing import Union, Dict, Tuple
import cadquery as cq


def export_cad_model(
        model: cq.Workplane,
        name: str,
        version: int,
        base_dir: Union[str, Path] = None,
        views: Dict[str, Tuple[float, float, float]] = None
) -> Path:
    if base_dir is None:
        base_dir = Path(__file__).parent / "models"
    else:
        base_dir = Path(base_dir)
    project_dir = base_dir / name
    version_dir = project_dir / f"v{version}"

    base_dir.mkdir(exist_ok=True)
    project_dir.mkdir(exist_ok=True)
    version_dir.mkdir(exist_ok=True)

    stl_filename = f"{name}.stl"
    stl_filepath = version_dir / stl_filename
    cq.exporters.export(model, str(stl_filepath))

    if views is None:
        views = {
            "front": (0, 0, 0),
            # "iso": (45, 45, 45),
            # "top": (0, 90, 0),
            # "right": (0, 0, 90),
            # "left": (0, 0, -90),
        }

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
        base_dir: Union[str, Path] = None,
        views: Dict[str, Tuple[float, float, float]] = None,
        additional_metadata: Dict[str, str] = None
) -> Path:
    version_dir = export_cad_model(model, name, version, base_dir, views)
    if views is None:
        views = {
            "front": (0, 0, 0),
            # "iso": (45, 45, 45),
            # "top": (0, 90, 0),
            # "right": (0, 0, 90),
            # "left": (0, 0, -90),
        }

    doc_filename = version_dir / f"{name}.md"
    with doc_filename.open('w') as f:
        f.write(f"# {name} (v{version})\n\n")
        if description:
            f.write(f"## Description\n{description}\n\n")

        f.write("## Metadata\n\n")
        f.write(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Model Name:** {name}\n")
        f.write(f"- **Version:** {version}\n")

        if additional_metadata:
            for key, value in additional_metadata.items():
                f.write(f"- **{key}:** {value}\n")

        f.write("\n")
        f.write("## Generated Files\n\n")
        stl_filename = f"{name}.stl"
        f.write(f"- STL File: [{stl_filename}](./{stl_filename})\n")
        f.write("- SVG Views:\n")
        f.write("\n## Model Views\n\n")
        for view_name in views.keys():
            svg_filename = f"{name}_{view_name}.svg"
            f.write(f"### {view_name.title()} View\n")
            f.write(f"![](./{svg_filename})\n\n")

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