# Agent guidance

- After writing or editing Python code, run `ruff format .` to format it,
  `ruff check .` to lint it, and a compile check (e.g.
  `python -m compileall -q .`) to catch syntax errors. Fix anything these
  report before considering the work done.
- Never use `if TYPE_CHECKING:` to guard imports. Use plain, real imports instead,
  even for type hints. If that causes a circular import, restructure the code
  (e.g. move the shared type, use a different module boundary) rather than
  falling back to `TYPE_CHECKING`.
