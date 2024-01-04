# type: ignore

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "aws_enterprise_mlops_platform"
copyright = "2022, AWS ProServe"
author = "AWS ProServe"

# The full version, including alpha/beta/rc tags
release = "1.0.0-dev"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "nbsphinx"
]
autosectionlabel_prefix_document = True
source_suffix = {".rst": "restructuredtext"}

# URL-shortener. The example below aliases the long pandas url with pdug.
extlinks = {
    # "pdug": (
    #     "https://pandas.pydata.org/pandas-docs/stable/user_guide/%s",
    #     "Pandas User Guide %s",
    # )
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "_README.md"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ['mlops_custom_theme.css']
html_js_files = ['script.js']