# Running the Python scripts in this repo

The Python audits under `experiments/` import each other — and the
shared geometry library — from the **repo root**:

```python
from core.geometry.e8_root_system import e8_roots_exact
from experiments.moonshine_sierpinski.leech_golay_construction import ...
```

Python only finds those packages if the repo root is on `sys.path`.
Run a script by bare file path from the wrong working directory and
you get:

```
ModuleNotFoundError: No module named 'core'
ModuleNotFoundError: No module named 'experiments'
```

## The three ways to run

1. **Directly, from anywhere (experiments scripts).** Scripts under
   `experiments/` carry a small repo-root bootstrap near the top
   (marked `repo-root bootstrap`): they locate the root from their
   own file path and put it on `sys.path` before importing. So this
   just works, from any working directory:

   ```
   python experiments/e8_weyl_orbit_audit.py
   ```

2. **As a module, from the repo root.** Works for everything,
   including files without the bootstrap:

   ```
   cd <repo root>
   python -m experiments.e8_weyl_orbit_audit
   ```

3. **Set `PYTHONPATH` to the repo root.** Then every invocation
   style works, from anywhere:

   PowerShell (per session):
   ```powershell
   $env:PYTHONPATH = "C:\path\to\PANoRAMic.os"
   ```
   PowerShell (permanent, per user):
   ```powershell
   [Environment]::SetEnvironmentVariable("PYTHONPATH", "C:\path\to\PANoRAMic.os", "User")
   ```
   POSIX shells:
   ```bash
   export PYTHONPATH=/path/to/PANoRAMic.os
   ```

## Tests and library modules

- Tests under `tests/` are run from the repo root by unittest
  discovery (`python -m unittest discover`), which already puts the
  root on the path. They deliberately carry no bootstrap.
- Modules under `core/` are a library: they are imported
  (`import core.geometry...`), never run as scripts, and likewise
  carry no bootstrap.

New experiment scripts that import from `core.` or `experiments.`
should copy the bootstrap block from any existing script (adjusting
the `parents[N]` index to the file's depth below the root) so they
stay runnable by path.
