
Ghidra workspace for CPSC436S
=============================

This folder hosts a copy of the Ghidra distribution used for reverse-engineering the course binaries for CPSC436S and a small launcher script to make starting Ghidra from the repository root easier.

What this folder contains
- `ghidra_12.0.4_PUBLIC/` — a Ghidra distribution (kept out of source control via `.gitignore`).
- `launch_ghidra.sh` — small helper script to run the included `ghidraRun` launcher.

Why this exists
----------------
Having a local copy of Ghidra in the repo makes it convenient to keep project metadata and reversed artifacts alongside the course files. The `launch_ghidra.sh` script avoids typing the long path to start Ghidra manually.

Usage
-----
From the repository root you can start Ghidra with:

```bash
./ghidra/launch_ghidra.sh
```

Or from within the `ghidra/` directory:

```bash
./launch_ghidra.sh
```

Any arguments passed to `launch_ghidra.sh` are forwarded to `ghidraRun`. For example, to open Ghidra with specific options, append them after the script call.

Notes
-----
- The `launch_ghidra.sh` script resolves its own directory and runs `ghidra_12.0.4_PUBLIC/ghidraRun`. If you replace or upgrade the Ghidra distribution, keep the directory name or update the script.
- The repository intentionally keeps the Ghidra binary distribution out of git (see `.gitignore`). If the `ghidra_12.0.4_PUBLIC` folder is missing, download and extract the official distribution into this `ghidra/` folder.
- If `ghidraRun` exists but is not executable, the launcher will attempt to set the executable bit for you.

Troubleshooting
---------------
- If you see the error "not found" when running the script, ensure the `ghidra_12.0.4_PUBLIC/ghidraRun` path exists inside this folder.
- On macOS you may need to allow the app to run in System Preferences > Security & Privacy the first time you launch Ghidra.

License / attribution
---------------------
Ghidra is distributed under its own license. See the `licenses/` directory inside `ghidra_12.0.4_PUBLIC/` for details.

Enjoy reversing! If you'd like, I can also add a small README section describing how/where to store Ghidra project folders inside this repo.
