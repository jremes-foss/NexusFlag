# NexusFlag CTF API

# Introduction

NexusFlag is a Python-based, easily-deployable, no-fuss, Open Source API for small community CTF (Capture the Flag) cybersecurity events. The project emphasizes accessibility, allowing communities to run their own events without heavy dependence on commercial platforms.

Built as a spiritual successor to BeeCTF, NexusFlag updates the vision of community-driven CTF software for the modern era using FastAPI, SQLAlchemy, and SQLite.

# Requirements

- OS: Linux, macOS, or WSL (Windows Subsystem for Linux)
- Python: 3.9+ (Tested up to 3.14-alpha)
- Tools: pip3, python3-venv

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/NexusFlag.git
cd NexusFlag
```

Set up the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialise and seed the database:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 seed.py
```

# Running the NexusFlag API

The API runs using Uvicorn. Once started, you can access the interactive documentation to explore endpoints.

```bash
uvicorn app.main:app --reload
```

- API Base: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

# Project Structure

- `app/models/`: Database tables (SQLAlchemy)
- `app/schemas/`: Data validation and JSON shapes (Pydantic).
- `app/api/`: API route definitions.
- `app/core/`: Security, hashing, and database configuration.

# Troubleshooting

**NOTE**: Note: If you modify the database models, delete the `nexus_flag.db` file and re-run `seed.py` to apply the changes.

# Important

NexusFlag is still under active development, so it is likely not ready for production use. This repository is used to host the code. Once MVP is ready for production use, I will remove this disclaimer from README. Thank you.

# License
NexusFlag is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. 
See the [LICENSE](LICENSE) file for the full text.