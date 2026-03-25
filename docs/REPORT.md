# The Vulnerability of Plaintext and Fast Hashing

**Course:** CSI 3480 Security and Privacy in Computing (Winter 2026)  
**Group Number:** [Enter group number]  
**Group Members:** [Member 1], [Member 2], [Member 3]

---

## Introduction

We chose this project because password storage is a common security topic that is often explained at a high level but not demonstrated concretely. Many people know plaintext storage is bad, but fewer people understand why "just hashing" is still not enough when the hash is fast. We wanted to build something practical that makes this difference visible in seconds.

This topic is interesting because it connects theory and real-world risk. In data breaches, attackers often obtain password databases and run offline guessing attacks. If passwords are stored with fast hashes such as MD5 or raw SHA-256, attackers can test many guesses quickly. By contrast, modern password hashing methods (bcrypt, Argon2, PBKDF2) intentionally slow each guess and include salts, increasing attack cost significantly. We wanted our project to show this security principle in a way that non-specialists can observe and understand.

This topic is important because password compromise is still one of the most common causes of account takeover. Weak storage decisions create long-term risk even if the application appears secure during normal operation. Demonstrating this risk clearly helps reinforce secure-by-design decisions for future projects.

---

## Problem Statement

### What is the problem?

The core problem is insecure password storage. Storing plaintext passwords is immediately dangerous because any leak directly exposes user credentials. Storing passwords with fast hashes (for example MD5, and in many contexts unsalted SHA-256) still leaves systems vulnerable to dictionary and brute-force attacks because these algorithms are computationally cheap.

### What did we plan to achieve?

We planned to create an educational Python demo (CLI + optional Flask web UI) that:

1. Accepts a user-provided password or generates a random 12-character password.
2. Hashes the password with MD5 and SHA-256.
3. Runs the same candidate dictionary against both hashes.
4. Reports elapsed cracking time and hashes/second for each algorithm.

### What is the project purpose?

The purpose is to demonstrate, with measurable output, that fast hashes are not appropriate for real password storage, and to justify the recommendation of slow, salted password-hashing algorithms (bcrypt, Argon2, PBKDF2).

---

## Methodology

Our implementation is organized into three layers: core logic, API service, and web interface.

### 1) Core logic (`backend/cracker.py`)

- Generated a random 12-character password (letters + digits) when no input was provided.
- Built a dictionary list that uses project-local seed candidates (`dictionary_12.txt`) when available, and fills remaining candidates with generated strings of the same length.
- Shuffled the dictionary before testing to avoid predictable password position.
- Implemented hash functions for MD5 and SHA-256.
- Implemented bcrypt using `bcrypt.hashpw` and `bcrypt.gensalt(rounds=...)`, and a dictionary-style attack using `bcrypt.checkpw` per candidate (matching the teammate pattern). Because each bcrypt verification is expensive, the demo optionally caps the bcrypt candidate list while still including the real password, so the web UI remains responsive.
- Implemented a dictionary attack loop that:
  - hashes each candidate,
  - compares against the target hash,
  - records elapsed time and attempt count,
  - computes hashes/second.

To keep comparison fair, both algorithms use the exact same wordlist for a run.

### 2) Flask API (`backend/app.py`)

- Added endpoint `GET/POST /api/compare`:
  - `POST` accepts JSON password input.
  - `GET` supports empty input behavior for random password generation.
- Added endpoint `GET /api/health` for quick backend validation.
- Served the frontend from `frontend/index.html`.
- Added `DICT_SIZE` environment variable support for configurable dictionary size.

### 3) Frontend (`frontend/index.html`)

- Implemented a single-page UI with:
  - optional password input,
  - run button,
  - result cards for hash values and timing metrics.
- Displayed:
  - generated/entered password,
  - MD5 and SHA-256 hashes,
  - dictionary size,
  - crack time and hashes/second for both algorithms.
- Added loading and error states to improve demo reliability during presentation.

### 4) Validation approach

- Ran CLI mode to verify end-to-end behavior without UI.
- Ran API smoke checks to ensure JSON schema matched frontend expectations.
- Confirmed both typed-password and auto-generated-password paths worked.

---

## Diagram / Demonstration

### Flow diagram (logical execution)

1. User enters password (or leaves blank).  
2. Frontend sends request to `/api/compare`.  
3. Backend selects user password or generates a random 12-character password.  
4. Backend computes MD5 and SHA-256 hashes.  
5. Backend builds one dictionary containing the target password.  
6. Backend runs dictionary attack on MD5 hash and measures time/rate.  
7. Backend runs dictionary attack on SHA-256 hash and measures time/rate.  
8. Backend returns results JSON.  
9. Frontend renders side-by-side comparison and conclusion.

### How this solves the problem

This flow solves the educational problem by converting abstract security advice into observable measurements. Users can run the same attack conditions against both fast hashes and directly inspect timing and throughput outputs. The result supports the conclusion that fast hashes are unsuitable for storing passwords.

---

## Group Work

> Replace names below with your actual team member names before submission.

### Member 1 - Backend

- Implemented and maintained Flask backend routes and JSON response schema.
- Connected backend API endpoints to the cracking logic in `backend/cracker.py`.
- Added support for optional password input and random password generation path.
- Added environment-based dictionary sizing and backend health endpoint.
- Validated API behavior for both GET and POST flows.

### Member 2 - Frontend

- Implemented and refined the web UI in `frontend/index.html`.
- Built the client-side request flow to call `/api/compare`.
- Added result rendering for password, hashes, dictionary size, and timing metrics.
- Added loading and error states for better demo reliability.
- Kept UI adjustments minimal while improving clarity for presentation.

### Member 3 - Report + Integration

- Authored and finalized the project report sections and references.
- Connected frontend and backend end-to-end so UI requests returned real backend metrics.
- Resolved integration mismatches (field names/routes) between frontend and backend.
- Verified complete workflow from input to displayed comparison results.
- Updated documentation to reflect final project structure and run steps.

### Collaboration process

- Worked in parallel by module, then integrated through shared interface contracts.
- Used short test cycles after each merge to detect mismatched field names early.
- Reviewed each other's outputs to ensure consistent messaging in UI, README, and report.

---

## Challenges

A major challenge was integrating teammate code that had overlapping app entry points and partially duplicated UI/backend logic. This caused confusion about which files were active and initially produced placeholder outputs rather than real attack metrics. We solved this by selecting one canonical execution path (`backend/app.py` + `frontend/index.html` + `backend/cracker.py`), removing legacy files, and validating API responses against frontend expectations.

Another challenge was ensuring fair performance comparison. Early implementation ideas could bias results if one algorithm stopped early after finding the password. We addressed this by running full-list comparisons under identical candidate sets, then measuring elapsed time and throughput consistently.

A practical environment challenge was dependency setup on managed Python installations. We resolved this by standardizing a virtual environment workflow in setup instructions, which made local runs reproducible across machines.

If continued, next directions would include adding bcrypt/Argon2/PBKDF2 directly to the comparison, charting results across multiple dictionary sizes, and adding automated tests for attack correctness and API schema stability.

---

## References

National Institute of Standards and Technology. (2010). *Recommendation for password-based key derivation: Part 1: Storage applications* (NIST SP 800-132). https://csrc.nist.gov/publications/detail/sp/800-132/final

National Institute of Standards and Technology. (2015). *Secure hash standard (SHS)* (FIPS PUB 180-4). https://csrc.nist.gov/publications/detail/fips/180/4/final

OWASP Foundation. (n.d.). *Password Storage Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
