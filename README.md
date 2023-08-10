# Pyprland

Python bindings for the Hyprland wayland compositor.

## Installation

**Dependencies**:
- Python 3.10
- [pydantic 2.1](https://docs.pydantic.dev/2.1/)



## Development

Start a virtual environment:
```python
cd path/to/repository/
python -m venv .venv
source .venv/bin/activate
# or for fish shell:
# source .venv/bin/activate.fish
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

Tests can be run from the repository root by invoking `pytest`:
```bash
pytest
```
