# Rialtic Engine Development Library (Python)

This repository contains common modules for developing Rialtic Insight Engines with Python.

## API Documentation (Sphinx)

The code in this repository is documented using [`sphinx`](https://www.sphinx-doc.org/en/master/) and
[`autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc). This
documentation can be generated locally. `autodoc` will generate basic documentation automatically from code, and
docstrings in the code can be used to add additional information to the generated documentation.

### Documentation Practices

#### Docstring Format

We use `sphinx.ext.napoleon`, which allows us to use a simpler, more concise format for docstrings
(popularized by NumPy and Google projects). See
the [NumPy documentation](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)
for an overview of how to use this style of docstrings.

**NOTE:** One main way that our docs differ from the standard described in the NumPy docs is with regard to
the `Returns` section. We do not need to specify return type in our docs—we have the
`sphinx_autodoc_typehints` extension, which automatically reads return type from type annotations in code.

#### Docstring Guidelines

Any docstrings written will eventually need to be edited or rewritten. With this in mind, it is valuable for our
docstrings to be concise and minimal, providing only necessary information, to reduce the work required to maintain
these docs.

For simple methods and functions, the generated function signature docs may even be sufficient. In these cases a
docstring can consist of only a single line summary.

If you find yourself writing a very long complex docstring, consider whether the object being documented could use a
refactor, or needs to be simplified in some way.

### Generating HTML Documentation Locally

The generated documentation will be hosted somewhere accessible on the web, but can also be generated locally in several
formats including HTML and PDF. Follow the instructions below to generate HTML documentation locally:

1.  ```bash
    $ git clone git@github.com:rialtic-community/rialtic-engine-lib-py.git
    $ cd rialtic-engine-lib-py/docs
    $ make html
    ```
    
2. Open the following file in a browser
    ```bash

    rialtic-engine-lib-py/docs/_build/html/index.html
    ```
