# The Vulnerability of Plaintext and Fast Hashing

CSI 3480 Security and Privacy in Computing - Winter 2026

This is a small demo app that shows why fast hashes are risky for password storage.
You can enter a password (or leave it blank to auto-generate one), then compare:

- MD5
- SHA-256
- bcrypt

The app runs dictionary-style checks and shows timing/rate so you can see how fast hashes differ from a slower password hash.

## Project structure

- `backend/app.py` - Flask server + API endpoints
- `backend/cracker.py` - hash and attack logic
- `frontend/index.html` - web UI
- `docs/REPORT.md` - full project report
- `requirements.txt` - dependencies

## Quick setup (copy/paste)

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the web demo

```bash
python backend/app.py
```

Open:

- `http://localhost:5000`

If port 5000 is busy on your machine, run on 5001:

```bash
python -c "from backend.app import app; app.run(host='0.0.0.0', port=5001, debug=True)"
```

Then open:

- `http://localhost:5001`

## How to use the demo

1. Open the page.
2. Type a password, or leave the field blank for an auto-generated password.
3. Click **Submit**.
4. Read the three result panels (MD5, SHA-256, bcrypt).

You will see:

- the hash output for each algorithm
- cracking/check timing
- rate (hashes/checks per second)

## Optional CLI run

```bash
python backend/cracker.py
```

## Useful settings (optional)

- `DICT_SIZE` (default `20000`)  
  Number of candidates for MD5/SHA-256 comparisons.

- `BCRYPT_ROUNDS` (default `6`)  
  bcrypt cost factor. Higher = slower, more realistic.

- `BCRYPT_ATTACK_CAP` (default `1200`)  
  Limit for bcrypt candidate checks so demo stays responsive.
  Use `0` or `full` to test bcrypt against the full list (can be very slow).

Example:

```bash
DICT_SIZE=30000 BCRYPT_ROUNDS=8 BCRYPT_ATTACK_CAP=1500 python backend/app.py
```

## Notes

- This is an educational demo, not a production auth system.
- Main takeaway: fast hashes (MD5/SHA-256) are not ideal for password storage; use bcrypt/Argon2/PBKDF2 with salt.
