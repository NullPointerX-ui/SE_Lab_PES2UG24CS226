# Lab 5: Reflection

**Name:** Khush Bhardwaj  **SRN:** PES2UG24CS226

### 1. What types of issues did the static analysis tools detect?

The three tools turned out to cover different ground with very little overlap. **Bandit** only looked for security weaknesses and found the ones that mattered most: the `shell=True` subprocess call that allows command injection, the bind to `0.0.0.0`, and the password sitting in plain sight in the source. **Pylint** found a mixture of genuine correctness problems and maintainability problems — the dangerous mutable default argument, the function that returns a value on one path and `None` on the other, the `open()` call with no encoding — along with 23 naming and docstring messages. **Flake8** was the narrowest of the three: four pure PEP 8 formatting issues (a stray space before a colon, a missing blank line, an inline comment, an over-long line) and nothing else. Severity varied enormously: a shell injection is an exploitable vulnerability, while a missing blank line is cosmetic, and the tools make no attempt to rank them against each other, so I had to.

### 2. Which issues were the most critical, and why?

The shell injection in `runScene` was the most critical by a wide margin. It is the only issue that hands an attacker control of the machine, and on a smart-home hub that means control of the door locks and cameras, not just the program. The hardcoded password came second — Bandit rates it only LOW, but a credential committed to a public GitHub repository is compromised the moment it is pushed and cannot be rotated without a release. I would rate it above the MEDIUM bind-to-all-interfaces finding for that reason, which shows that a tool's severity label is a starting point rather than a verdict.

The most interesting issue, though, was the mutable default argument. Bandit ignored it and Flake8 ignored it; Pylint reported it as a single `W0102` warning with no indication that it was anything more than untidy. In fact it was the real functional bug in the program: because every device shared one `settings` dictionary, setting the thermostat to 30 also gave the ceiling light a temperature, and the demo printed `Light settings: {'temperature': 30}` for a lamp. The tool told me *where* to look; reading the output told me *why* it mattered.

### 3. How did fixing these issues improve the code?

The Pylint score went from 4.80/10 to 10.00/10, Flake8 went to zero, and Bandit's HIGH and MEDIUM findings were eliminated. More usefully, the program now behaves correctly — each device keeps its own settings — and `set_temperature` reports an unknown device instead of crashing with a `KeyError`, which matched how `toggle_device` already behaved. The security fixes narrowed the attack surface rather than just silencing a warning: the scene path is validated against a fixed directory and run without a shell, so a hostile scene name is now simply a filename that does not exist. The naming and docstring changes do not alter a single line of behaviour, but after renaming everything to snake_case and documenting the return values, the module reads consistently and a new reader can tell what each function does and what it does when it fails.

### 4. How can static analysis be integrated into a development workflow?

The obvious place is a pre-commit hook, so Flake8 and Pylint run on changed files before a commit is accepted and formatting issues never reach review. Beyond that, the same three commands belong in CI on every pull request, with the build failing on any Bandit HIGH or MEDIUM finding and on a Pylint score below an agreed threshold (9.5 here) — that is what makes the standard hold over time instead of decaying between labs. Running the tools locally before pushing keeps the feedback loop short.

The important caveat is that static analysis is a floor, not a ceiling. Every one of the four Bandit findings here was real, but Bandit would also have passed the mutable-default bug without comment, and a tool that ran on the fixed file would still flag `B404` and `B603` even though those were reviewed and are not problems. So the workflow has to include a human deciding which findings matter, suppressing the ones that do not *with a written reason*, and reading the program's actual output — which is how I found the bug that none of the three tools called a bug.
