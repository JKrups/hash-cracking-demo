"""
Password hashing and dictionary attack comparison: MD5 vs SHA-256 vs bcrypt.
Demonstrates why fast hashes (MD5) are vulnerable to cracking, and why bcrypt
is intentionally slow for password storage.
CSI 3480 Security and Privacy in Computing - Winter 2026
"""

import hashlib
import itertools
import os
from pathlib import Path
import random
import string
import time
from typing import Optional

import bcrypt

def generate_password(length: int = 12) -> str:
    """Generate a random password of given length (letters + digits)."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def load_dictionary_file(filename: str = "dictionary_12.txt") -> list[str]:
    """
    Load optional dictionary_12.txt from inside the project.
    If not found, caller can fall back to generated candidates.
    """
    here = Path(__file__).resolve()
    candidate_paths = [
        here.parent / filename,  # backend/
        here.parent.parent / filename,  # project root
    ]
    for path in candidate_paths:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
    return []


def generate_dictionary_candidates() -> list[str]:
    """
    Adapted from teammates' dictonary_genrator.py.
    Produces 12-char style candidates.
    """
    words_8 = [
        "password",
        "standard",
        "security",
        "learning",
        "computer",
        "november",
        "kittycat",
        "february",
        "december",
        "holidays",
    ]
    digits = [f"{i:04}" for i in range(100)]
    words_5 = ["green", "grass"]
    words_7 = ["october", "quarter"]
    words_4 = [
        "blue",
        "bolt",
        "fire",
        "cold",
        "kind",
        "fast",
        "feet",
        "dogs",
        "june",
        "july",
        "cats",
        "grow",
    ]

    out: list[str] = []
    for w, d in itertools.product(words_8, digits):
        out.append(f"{w}{d}")
    for i, s in itertools.product(words_5, words_7):
        out.append(f"{i}{s}")
    for combo in itertools.product(words_4, repeat=3):
        out.append("".join(combo))
    return out


def build_dictionary_with_password(password: str, size: int = 25_000) -> list[str]:
    """
    Build a list of candidate passwords that includes the target.
    Used for a fair dictionary attack comparison.
    """
    chars = string.ascii_letters + string.digits
    candidates = set(load_dictionary_file())
    candidates.update(generate_dictionary_candidates())
    candidates.add(password)
    while len(candidates) < size:
        candidates.add("".join(random.choices(chars, k=len(password))))
    return list(candidates)


def hash_md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_bcrypt(password: str) -> bytes:
    """
    Teammate-style bcrypt hash from provided password.py:
    bcrypt.hashpw(password_bytes, bcrypt.gensalt(...))
    """
    rounds = int(os.environ.get("BCRYPT_ROUNDS", "6"))
    rounds = max(4, min(rounds, 31))
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=rounds))


def build_bcrypt_wordlist(full_wordlist: list[str], password: str) -> tuple[list[str], Optional[int]]:
    """
    bcrypt.checkpw is intentionally slow. Running tens of thousands of checks can take minutes.
    By default we use a random subset of the full candidate list that still contains the
    real password (same idea as a partial dictionary sweep).

    Set BCRYPT_ATTACK_CAP=0 to use the full wordlist (slow). Default cap keeps the web UI responsive.
    """
    raw = os.environ.get("BCRYPT_ATTACK_CAP", "1200").strip().lower()
    if raw in ("", "full", "all"):
        return full_wordlist, None
    cap = int(raw)
    if cap <= 0 or cap >= len(full_wordlist):
        return full_wordlist, None
    others = [w for w in full_wordlist if w != password]
    need = min(cap - 1, len(others))
    sample = random.sample(others, need)
    out = sample + [password]
    random.shuffle(out)
    return out, cap


def dictionary_attack(
    target_hash: str,
    wordlist: list[str],
    hash_func,
) -> tuple[Optional[str], float, int]:
    """
    Run a dictionary attack: hash every candidate and compare to target.
    Always hashes the full list so timing is comparable between algorithms.
    Returns (cracked_password or None, elapsed_seconds, attempts).
    """
    start = time.perf_counter()
    cracked = None
    for word in wordlist:
        if hash_func(word) == target_hash:
            cracked = word
    elapsed = time.perf_counter() - start
    return cracked, elapsed, len(wordlist)


def dictionary_attack_bcrypt(
    password_bcrypt: bytes,
    wordlist: list[str],
) -> tuple[Optional[str], float, int]:
    """
    Teammate-style bcrypt dictionary attack from provided password.py:
    for each candidate, bcrypt.checkpw(candidate_bytes, password_bcrypt).
    Stops at first match (realistic for guessing attacks).
    """
    start = time.perf_counter()
    cracked = None
    attempts = 0
    for i in wordlist:
        attempts += 1
        if bcrypt.checkpw(i.encode("utf-8"), password_bcrypt):
            cracked = i
            break
    elapsed = time.perf_counter() - start
    return cracked, elapsed, attempts


def run_comparison(
    dict_size: int = 25_000,
    password: Optional[str] = None,
) -> dict:
    """
    Hash the given password (or generate one) with MD5 and SHA-256,
    then run dictionary attacks and compare times.
    """
    if password is None or not password.strip():
        password = generate_password(12)
    else:
        password = password.strip()
        # Keep demo behavior simple and aligned with assignment requirement.
        if len(password) < 12:
            password = generate_password(12)
    wordlist = build_dictionary_with_password(password, size=dict_size)

    # Shuffle so password position isn't predictable
    random.shuffle(wordlist)

    bcrypt_wordlist, bcrypt_cap = build_bcrypt_wordlist(wordlist, password)

    md5_hash = hash_md5(password)
    sha256_hash = hash_sha256(password)
    bcrypt_hash_bytes = hash_bcrypt(password)
    bcrypt_hash_str = bcrypt_hash_bytes.decode("utf-8")

    # Crack MD5
    md5_result, md5_time, md5_attempts = dictionary_attack(md5_hash, wordlist, hash_md5)
    # Crack SHA-256
    sha256_result, sha256_time, sha256_attempts = dictionary_attack(
        sha256_hash, wordlist, hash_sha256
    )
    # Crack bcrypt (teammate loop: checkpw per candidate until match)
    bcrypt_result, bcrypt_time, bcrypt_attempts = dictionary_attack_bcrypt(
        bcrypt_hash_bytes, bcrypt_wordlist
    )

    return {
        "password": password,
        "md5_hash": md5_hash,
        "sha256_hash": sha256_hash,
        "bcrypt_hash": bcrypt_hash_str,
        "bcrypt_rounds": int(os.environ.get("BCRYPT_ROUNDS", "6")),
        "dict_size": len(wordlist),
        "bcrypt_wordlist_size": len(bcrypt_wordlist),
        "bcrypt_attack_cap": bcrypt_cap,
        "md5": {
            "cracked": md5_result is not None,
            "cracked_password": md5_result,
            "time_seconds": round(md5_time, 4),
            "attempts": md5_attempts,
            "hashes_per_second": round(md5_attempts / md5_time, 1) if md5_time > 0 else 0,
        },
        "sha256": {
            "cracked": sha256_result is not None,
            "cracked_password": sha256_result,
            "time_seconds": round(sha256_time, 4),
            "attempts": sha256_attempts,
            "hashes_per_second": round(sha256_attempts / sha256_time, 1) if sha256_time > 0 else 0,
        },
        "bcrypt": {
            "cracked": bcrypt_result is not None,
            "cracked_password": bcrypt_result,
            "time_seconds": round(bcrypt_time, 4),
            "attempts": bcrypt_attempts,
            "hashes_per_second": round(bcrypt_attempts / bcrypt_time, 1) if bcrypt_time > 0 else 0,
        },
    }


if __name__ == "__main__":
    print("MD5 vs SHA-256 vs bcrypt dictionary attack comparison")
    print("=" * 50)
    result = run_comparison(dict_size=25_000)
    print(f"Generated password (12 chars): {result['password']}")
    print(f"MD5 hash:    {result['md5_hash']}")
    print(f"SHA-256 hash: {result['sha256_hash'][:48]}...")
    print(f"bcrypt hash: {result['bcrypt_hash'][:56]}...")
    print(f"\nDictionary size: {result['dict_size']} candidates")
    print(f"\nMD5 crack:    {result['md5']['time_seconds']} s  ({result['md5']['hashes_per_second']} hashes/s)")
    print(f"SHA-256 crack: {result['sha256']['time_seconds']} s  ({result['sha256']['hashes_per_second']} hashes/s)")
    print(
        f"bcrypt crack: {result['bcrypt']['time_seconds']} s  "
        f"({result['bcrypt']['attempts']} checkpw calls, {result['bcrypt']['hashes_per_second']} checks/s)"
    )
    print("\nConclusion: MD5 and SHA-256 are fast hashes, so offline guessing can try many candidates per second.")
    print("bcrypt is intentionally slow (cost factor); use it (or Argon2/PBKDF2) for password storage, not raw MD5/SHA-256.")
