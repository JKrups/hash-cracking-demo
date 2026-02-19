"""
Password hashing and dictionary attack comparison: MD5 vs SHA-256.
Demonstrates why fast hashes (MD5) are vulnerable to cracking.
CSI 3480 Security and Privacy in Computing - Winter 2026
"""

import hashlib
import random
import string
import time
from typing import Optional


def generate_password(length: int = 12) -> str:
    """Generate a random password of given length (letters + digits)."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def build_dictionary_with_password(password: str, size: int = 25_000) -> list[str]:
    """
    Build a list of candidate passwords that includes the target.
    Used for a fair dictionary attack comparison.
    """
    chars = string.ascii_letters + string.digits
    candidates = set()
    candidates.add(password)
    while len(candidates) < size:
        candidates.add("".join(random.choices(chars, k=len(password))))
    return list(candidates)


def hash_md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
    wordlist = build_dictionary_with_password(password, size=dict_size)

    # Shuffle so password position isn't predictable
    random.shuffle(wordlist)

    md5_hash = hash_md5(password)
    sha256_hash = hash_sha256(password)

    # Crack MD5
    md5_result, md5_time, md5_attempts = dictionary_attack(md5_hash, wordlist, hash_md5)
    # Crack SHA-256
    sha256_result, sha256_time, sha256_attempts = dictionary_attack(
        sha256_hash, wordlist, hash_sha256
    )

    return {
        "password": password,
        "md5_hash": md5_hash,
        "sha256_hash": sha256_hash,
        "dict_size": len(wordlist),
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
    }


if __name__ == "__main__":
    print("MD5 vs SHA-256 dictionary attack comparison")
    print("=" * 50)
    result = run_comparison(dict_size=25_000)
    print(f"Generated password (12 chars): {result['password']}")
    print(f"MD5 hash:    {result['md5_hash']}")
    print(f"SHA-256 hash: {result['sha256_hash'][:48]}...")
    print(f"\nDictionary size: {result['dict_size']} candidates")
    print(f"\nMD5 crack:    {result['md5']['time_seconds']} s  ({result['md5']['hashes_per_second']} hashes/s)")
    print(f"SHA-256 crack: {result['sha256']['time_seconds']} s  ({result['sha256']['hashes_per_second']} hashes/s)")
    print(f"\nConclusion: SHA-256 is slower per hash, so the same attack takes longer.")
