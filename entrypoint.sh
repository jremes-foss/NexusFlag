#!/bin/bash

set -e

DB_FILE="/app/nexus_flag.db"

echo "-------------------------------------------------------"
echo "  Starting NexusFlag CTF API Initialization...         "
echo "-------------------------------------------------------"

if [ ! -f "$DB_FILE" ]; then
    echo "[!] Database file not found at $DB_FILE"
    echo "[!] Running seed.py to initialize schema and admin user..."    
    export PYTHONPATH=$PYTHONPATH:/app
    python3 /app/seed.py
    echo "[+] Database initialization complete."
else
    echo "[*] Database found. Skipping seeding to preserve existing data."
fi

mkdir -p /app/static/challenges
echo "[*] Storage directories verified."
echo "[+] Handing over to Uvicorn..."
echo "-------------------------------------------------------"

exec uvicorn app.main:app --host 0.0.0.0 --port 8000