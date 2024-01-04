# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS      ?=
SPHINXBUILD     ?= sphinx-build
SPHINXAPIDOC    ?= sphinx-apidoc
SOURCEDIR       = .
BUILDDIR        = _build
SPHINXAUTOBUILD = sphinx-autobuild

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "  livehtml    to run live-preview (require Python package sphinx-autobuild)"

.PHONY: help Makefile prep

clean: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) || true
	@rmdir "$(BUILDDIR)" || true

livehtml:
	@$(SPHINXAUTOBUILD) --re-ignore 'docs/_README.md' "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

prep:
	@mkdir -p _build/ _static/

use-case-diagrams:
	@python make_diagrams.py

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile prep
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
