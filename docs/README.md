# Hyprpy documentation

The Hyprpy documentation is built using Sphinx and its autodoc plugin.

## Building

**Important:** Sphinx autodoc needs to successfully import Python code to document it.
This means that you must have the Hyprpy dependencies installed, or be in a virtual environment which has them installed, in order to build the documentation.

To build the HTML documentation, from within the `docs` directory, run

```bash
make clean && make html
```

The output files will now be in `docs/build/html`.

### Testing

To test the generated documentation after building it, from within the `docs` directory run

```bash
python -m http.server -b 127.0.0.1 -d build/html 8000
```

and visit [http://localhost:8000/](http://localhost:8000/) in your browser.
