# cadquery-scripts

A repository for creating and managing 3D printable models using CadQuery.

## Directory Structure

```
cadquery-scripts/
├── models/                        # Generated model files (Example shown below)
│   └── example/
│       └── v1/
│           ├── example.stl        # Generated 3D model file
│           ├── example.md         # Model documentation
│           └── example.svg        # Model visualization
├── scripts/                       # Model generation scripts
│   └── example.py                 # One script per model
├── template.py                    # Base class template for model creation
├── utils.py                       # Display and export utilities
├── .gitignore                     # Git ignore file
├── .python-version                # Specifies required Python version
├── README.md                      # This file
└── requirements.txt               # Project dependencies
```

## Generate Models

To generate all models and their documentation, run:

```bash
for f in scripts/*.py; do .venv/Scripts/python -m "scripts.$(basename ${f%.*})"; done
```

