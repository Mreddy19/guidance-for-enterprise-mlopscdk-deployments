# Build documentations <!-- omit in toc -->

**IMPORTANT**:
*Unless stated otherwise, all the instructions on this page assumes `GITROOT/` as your current
directory.*

## 1. Pre-Requisites

The Python packages required to build the documentations can be installed as follows:

```bash
pip install -r requirements-docs.txt
```

## 2. Generate HTML documentations

Run these commands:

```bash
cd docs
make clean
make html
```

then point your web browser to `docs/_build/html/index.html`.

On a multi-core machine, you can also pass the ``-j <num>`` to speed-up the build process.

```bash
cd docs
make clean

# Instruct make to run 4 jobs (commands) in parallel.
make -j 4 html
```

## 3. Development

[VS Code](https://code.visualstudio.com/) users may consider the
[Live Preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server) extension
to auto-refresh the preview of the generated HTML pages after every ``make html``.

## 4. FAQ

### 4.1. Auto-build during Development

You may use [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) to automatically
build and live-preview the documentations.

> **BEWARE**: as of this writing,
> [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) runs a ``make`` command
> for every file modified (i.e., saved). This may be too excessive when when multiple files are
> saved in a short period of time, e.g., by your favorite IDE, editor, pre-commit hooks, etc.

```bash
# Assume requirements-docs.txt has been installed
cd GITROOT/docs
pip install sphinx-autobuild
make livehtml
```

and you should see this kind of messages in your terminal:

```text
...

The HTML pages are in _build.
[I 220405 18:25:21 server:335] Serving on http://127.0.0.1:8000
[I 220405 18:25:21 handlers:62] Start watching changes
[I 220405 18:25:21 handlers:64] Start detecting changes
```

The line `Serving on http://127.0.0.1:8000` indicates that the live-preview server is running at
this address. You can then point your web-browser to <http://127.0.0.1:8000>, and it will
auto-refresh whenever you make changes to the `.rst` files.

To stop the live-preview server, press `Ctrl-C` on the same terminal where you run `make livehtml`.
