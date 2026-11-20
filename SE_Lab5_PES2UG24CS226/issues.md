# Lab 5: Static Code Analysis — Issues Found and Fixed

**Name:** Khush Bhardwaj  **SRN:** PES2UG24CS226
**File analysed:** `smart_home.py`
**Tools:** Pylint 3.x, Bandit 1.x, Flake8 7.x

---

## Issue table

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | `subprocess.call("bash scenes/" + sceneScript, shell=True)` | Security — Bandit **B602**, severity **HIGH** | 51 | The scene name is concatenated straight into a shell command string with `shell=True`. A name such as `party.sh; rm -rf ~` would be executed by the shell as a second command, so any caller that can influence the scene name gets arbitrary command execution on the hub. | Dropped the shell. The script name is resolved inside a fixed `SCENES_DIR`, rejected unless the resolved path really sits under that directory and is a file, and then run as an argument list: `subprocess.run(["/bin/bash", str(script_path)], check=False, shell=False)`. Shell metacharacters are now just characters in a filename. |
| 2 | `HUB_HOST = "0.0.0.0"` | Security — Bandit **B104**, severity **MEDIUM** | 4 | The hub binds to every network interface, so the controller is reachable from the whole LAN (and from the internet behind a careless router) rather than from the machine it runs on. | Changed the default to the loopback address `127.0.0.1`. A deployment that genuinely needs LAN access should opt in explicitly rather than get it by default. |
| 3 | `HUB_PASSWORD = "smarthome-demo"` | Security — Bandit **B105**, severity LOW (but high real-world impact) | 7 | The hub password is hardcoded in source. Anyone who reads the repository — and this repository is public — knows the credential, and it cannot be rotated without a code change. | Removed the literal. The password is now read at run time from the `SMARTHOME_HUB_PASSWORD` environment variable through a `hub_password()` helper, so the secret lives in the environment and never in version control. |
| 4 | `def addDevice(deviceName, kind, room="Living Room", settings={})` | Correctness / quality — Pylint **W0102** `dangerous-default-value` | 11 | **This is the behavioural bug the lab output hints at.** A mutable default is evaluated once, at definition time, so every device created without an explicit `settings` argument shares *one* dictionary. Setting the thermostat to 30 therefore also gave the ceiling light a temperature: the demo printed `Light settings: {'temperature': 30}`. | Default changed to `settings=None`; each call now builds its own dictionary (`dict(settings) if settings else {}`). The demo now correctly prints `Light settings: {}` while the thermostat keeps `{'temperature': 30}`. |
| 5 | `setTemperature` indexes `devices[deviceName]` directly | Correctness — unhandled `KeyError` | 24 | Unlike `toggleDevice`, this function never checks that the device exists, so calling it with an unknown name crashes the program with a `KeyError` instead of reporting the problem. | Switched to `devices.get(device_name)` and return `False` with a "Device not found" message, matching the behaviour of `toggle_device`. |
| 6 | `toggleDevice` returns a value on one path and `None` on the other | Quality — Pylint **R1710** `inconsistent-return-statements` | 16–20 | A caller cannot tell "the device is now off" (`False`) from "there is no such device" (implicit `None`) without extra checks, which is exactly the kind of ambiguity that produces later bugs. | Made the early exit an explicit `return None` and documented both outcomes in the docstring. |
| 7 | camelCase names throughout (`addDevice`, `deviceName`, `fileName`, …) | Style — Pylint **C0103** `invalid-name` (13 occurrences) | 11, 16, 23, 32, 36, 40, 45, 49 | The module mixes camelCase with Python's snake_case convention, which makes the code harder to read for anyone used to PEP 8. | Renamed every function and parameter to snake_case (`add_device`, `device_name`, `file_name`, …) and updated all call sites. |
| 8 | No module or function docstrings | Style — Pylint **C0114 / C0116** (10 occurrences) | 1, 11, 16, 23, 32, 36, 40, 45, 49, 54 | Nothing in the file states what the module or any function is for, what it returns, or what happens in the error cases. | Added a module docstring and a docstring to every function, including the return values and failure behaviour. |
| 9 | `open(fileName, "w")` without an encoding | Portability — Pylint **W1514** `unspecified-encoding` | 41 | The file is written in whatever encoding the platform happens to default to, so a state file written on one machine can be unreadable on another. | Added `encoding="utf-8"`. |
| 10 | `main()` called at import time | Quality / testability | 72 | The demo runs on `import smart_home`, so the module cannot be imported by a test suite or another program without side effects. | Guarded with `if __name__ == "__main__": main()`. |
| 11 | `{"light" : 10, ...}`, one blank line before `saveState`, `#` comment with one space, 80-character line | Style — Flake8 **E203, E302, E261, E501** | 6, 40, 66, 68 | Four PEP 8 violations flagged by Flake8. | Removed the space before the colon, used two blank lines between top-level definitions, two spaces before the inline comment, and wrapped the long line. |

---

## Before and after

| Tool | Before | After |
|------|--------|-------|
| Pylint | **4.80/10** — 27 messages | **10.00/10** — 0 messages |
| Bandit | 1 HIGH (B602), 1 MEDIUM (B104), 2 LOW | 0 HIGH, 0 MEDIUM, 2 LOW (informational only) |
| Flake8 | 4 issues (E203, E302, E261, E501) | 0 issues |

The two remaining Bandit findings are **B404** ("consider the implications of importing `subprocess`") and **B603** ("subprocess call — check for execution of untrusted input"). Both are informational notices that Bandit raises for *any* use of `subprocess`, and neither can be cleared while the module legitimately needs to run a scene script. They were reviewed and accepted: the call no longer uses a shell, the executable is a fixed absolute path, and the only argument is a path that has been verified to live inside `scenes/`.

Raw tool output is in `pylint_report.txt`, `bandit_report.txt` and `flake8_report.txt`, with the original runs kept alongside as `*_report_before.txt`.
