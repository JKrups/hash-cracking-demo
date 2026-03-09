# The Vulnerability of Plaintext and Fast Hashing

**CSI 3480 Security and Privacy in Computing — Winter 2026**

This project demonstrates why storing passwords with fast, legacy hashes (like MD5) is insecure, and compares cracking time to a modern hash (SHA-256) using a simple dictionary attack.

## What it does

1. **Uses** a password you enter, or **generates** a random 12-character password (letters + digits) if you leave the field empty.
2. **Hashes** it with both MD5 and SHA-256.
3. **Runs a dictionary attack** against each hash (same wordlist, same password in the list).
4. **Reports** how long each attack took and how many hashes per second were tried.

 MD5 and SHA-256 are both **fast** hashes, so dictionary and brute-force attacks can try large numbers of guesses per second. On many systems MD5 will be faster than SHA-256, but the exact difference can vary by machine and crypto library implementation—the key takeaway is the same: **fast hashes are a poor choice for password storage**. For real password storage you should use a **dedicated password hash** (e.g. bcrypt, Argon2, PBKDF2) with a unique salt per password—not raw SHA-256.

## Project layout

- `backend/cracker.py` — Core logic: password generation, hashing, dictionary attack.
- `backend/app.py` — Flask API that runs the comparison and serves the frontend.
- `frontend/index.html` — Simple web UI to run the demo and view results.

## How to test the application (for teammates)

### Prerequisites

- **Python 3.8+** installed on your machine.

### 1. Clone and open the project

```bash
cd hash-cracking-demo
```

(If you’re in a different repo path, use that folder instead.)

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the backend server

```bash
cd backend
python app.py
```

You should see something like:

- `Running on http://127.0.0.1:5000`

**If port 5000 is already in use** (e.g. on macOS, AirPlay Receiver uses 5000):

- **macOS:** System Settings → General → AirDrop & Handoff → set **AirPlay Receiver** to **Off**, or
- Run on a different port:  
  `python -c "from app import app; app.run(host='0.0.0.0', port=5001, debug=True)"`  
  then use **http://localhost:5001** in the steps below.

### 4. Open the app in your browser

- Go to **http://localhost:5000** (or **http://localhost:5001** if you used the alternate port).

### 5. Run the demo

- **With your own password:** Type a password in the **Password** field, then click **Run comparison**.
- **With a random password:** Leave the **Password** field empty and click **Run comparison**.

You’ll see the password (yours or generated), the MD5 and SHA-256 hashes, dictionary size, and the time/hashes-per-second for cracking each hash.

### 6. Stop the application

- In the terminal where the server is running, press **Ctrl+C**.

---

### Optional: run from command line only (no web UI)

From the project root:

```bash
cd backend
python cracker.py
```

This prints one comparison to the terminal (random password, no server).

## Configuration

- **Dictionary size**: The number of candidate passwords in the attack. Default is 20,000. Set env var `DICT_SIZE` to change it (e.g. `DICT_SIZE=10000 python app.py`). Larger lists make the difference between MD5 and SHA-256 more noticeable but take longer.

## For your report

- **Methodology**: The script builds a random wordlist that includes the generated 12-char password, then runs the same list against the MD5 and SHA-256 hashes and measures elapsed time and hashes per second.
- **Diagram**: You can include a screenshot of the web demo (before/after clicking “Run comparison”) and/or a flowchart: Generate password → Hash with MD5 and SHA-256 → Dictionary attack on each → Compare times.
- **References**: Cite NIST guidelines on password hashing, and any sources you use for the introduction (e.g. OWASP, NIST SP 800-132).

## Sharing this repo on GitHub

To put this project on your GitHub so teammates can clone it:

1. **Create a new repository** on GitHub: go to [github.com/new](https://github.com/new).
2. Set **Repository name** to `hash-cracking-demo`, set visibility to **Public**, and leave "Add a README" unchecked (this project already has one).
3. Click **Create repository**.
4. In this project folder, push the existing code:

   ```bash
   cd hash-cracking-demo
   git push -u origin main
   ```

Share the repo link: **https://github.com/JKrups/hash-cracking-demo**

## License

For educational use as part of CSI 3480.
