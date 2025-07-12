# SQLite_DPM_Sync_Tool

[![CI](https://github.com/Citta123/SQLite_DPM_Sync_Tool/actions/workflows/ci.yaml/badge.svg)](https://github.com/Citta123/SQLite_DPM_Sync_Tool/actions)

Automated data fetch → photo tagging → upload pipeline for PLN prepaid meters.

## Features
- End-to-end flow: fetch data, enrich, attach photos, upload.
- One-command run: `python main.py --help`.
- Zero heavy deps (only **requests**).
- CI ready (flake8 + pytest).

![Demo](docs/assets/demo.gif)
