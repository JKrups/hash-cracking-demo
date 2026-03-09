# The Vulnerability of Plaintext and Fast Hashing

**Group [N]**  
**[Member 1 Name], [Member 2 Name], [Member 3 Name]**  

CSI 3480 Security and Privacy in Computing — Winter 2026

---

## Introduction

We picked this project because we wanted to actually *see* why fast hashes like MD5 are a bad idea for passwords. In class we talked about hashing and why plaintext is a no-go, but it felt abstract. We hadn’t watched a real attack run and compared how long it took to crack MD5 versus something slower. A lot of systems still use MD5 or unsalted SHA-256 for passwords, and we were curious what would happen if we ran the same dictionary attack against both—same password, same wordlist, same machine. Only the hash would change. That curiosity is what got us started. Once you see the timing difference on screen, the risk stops being theoretical. It’s something you can show people.

The topic matters for a few reasons. Data breaches happen all the time, and when passwords are hashed with something fast, attackers can throw billions of guesses per second at them. We’ve also noticed that people say “passwords should be hashed” without really explaining *which* hash or why speed matters. NIST and OWASP are clear about this: they recommend slow, purpose-built hashes like bcrypt or Argon2 with salt, and they explicitly say not to use MD5 or raw SHA-256 for passwords (NIST, 2010; OWASP, n.d.). We wanted to understand why by measuring it ourselves. Building a small demo that compares MD5 and SHA-256 under the same attack seemed like a good way to make that stick—for us and for anyone else who tries it.

---

## Problem Statement

**What is the problem we worked on?**  
Passwords get stored as hashes instead of plaintext, which is good, but not every hash is safe for that job. MD5 was built for things like checksums where you want speed. When you use it for passwords, an attacker who gets the hash (say, from a leaked database) can run a dictionary or brute-force attack—hash tons of guesses and compare. The faster the hash, the more guesses per second they can try. MD5 and SHA-256 are both *fast* hashes (especially compared to password-hashing algorithms like bcrypt or Argon2), so guessing attacks can run quickly in either case. On many systems MD5 will be faster than SHA-256, but the exact difference can vary by hardware and implementation; the key point is that **fast hashes are a poor choice for password storage**. So the real issue isn’t just “hash or don’t hash,” it’s “fast hash or slow hash,” and we wanted to show that difference in a way you could actually measure.

**What do we plan to achieve?**  
We wanted to build something that lets you type a password (or generate one), hash it with both MD5 and SHA-256, run the *same* dictionary attack on both, and then show how long each one took and how many hashes per second we got. The idea was to show that both are fast to compute (and therefore cheap to attack at scale), and to observe any timing difference under identical conditions on our machine. We also wanted it to run in a browser so teammates could try it without messing with the command line.

**What is the purpose of the project?**  
It’s for learning. We’re trying to make it obvious why picking the right hash matters and to back up the advice that you should use slow, salted hashes like bcrypt or Argon2 instead of MD5 or raw SHA-256 (OWASP, n.d.). This isn’t meant to be a real security tool—it’s a demo to help people see the difference.

---

## Methodology

**How we achieved our scope.**  
We kept it simple: one password, two hashes (MD5 and SHA-256), one wordlist, and a fair timing comparison. The core logic lives in Python, we wrapped it in a small Flask API, and we built a web frontend so people could run it without touching the command line. To keep things fair, we use the same password and the same wordlist for both attacks—the only thing that changes is the hash function. We also made the wordlist size configurable (via an env variable) so we could do quick demos with smaller lists or longer runs when we wanted the timing difference to really show.

**How we implemented the project.**  
We split it into three parts: the core logic, the API, and the frontend.

*Core logic.*  
The core module handles everything: generating a random 12-character password (letters and digits) when the user doesn’t type one, building a wordlist that includes the target password, and running the dictionary attack. We build the wordlist by generating random candidates the same length as the password, adding the real password to the set, filling up to our target size (default 20,000), and then shuffling so the password’s position isn’t predictable. That way we don’t accidentally bias the results. We hash the password with MD5 and SHA-256, then run the attack on each: loop through every candidate, hash it, compare to the target. We always process the full wordlist (no early exit) so both algorithms do the same amount of work—only the time differs. We use Python’s high-resolution timer so even short runs give us meaningful numbers. All of this lives in one module with separate functions for password gen, wordlist building, hashing, and the attack. A top-level function ties it together and spits out the structured result.

*API.*  
Flask serves the frontend and exposes a comparison endpoint. It accepts GET (password in the query string) or POST (password in the JSON body) so we don’t put passwords in the URL when someone types one. If no password is sent, the backend generates one. We read the dictionary size from an environment variable so we can tweak it without changing code. There’s also a health-check endpoint so we can quickly see if the server is up, and we turned on CORS so the frontend can talk to the API.

*Frontend.*  
Single HTML page with inline CSS and JS. There’s a password field (with a placeholder saying to leave it empty for a random one), a “Run comparison” button, and a results area that pops up when the request finishes. It shows the password, both hashes, the dictionary size, and for each algorithm the crack time and hashes per second. We gave MD5 and SHA-256 different colors so they’re easy to tell apart, and we added a loading spinner and error messages so you know when something goes wrong.

---

## Diagram (or Demonstration)

The demo makes the crack time visible so you can compare MD5 and SHA-256 side by side. Here’s how it works, and what the screenshots show.

*Flow of the demo.*  
You open the page and either type a password or leave the field blank. Click “Run comparison,” and the frontend sends your input (or nothing) to the backend. The backend uses your password or generates a random one, builds a wordlist that includes it, shuffles it, and hashes the password with both MD5 and SHA-256. Then it runs the dictionary attack on the MD5 hash—hash every candidate, compare, record the time—and does the same for SHA-256 with the exact same wordlist. It sends back a JSON object with the password, both hashes, and the timing for each. The frontend shows everything in two boxes (one for MD5, one for SHA-256) so you can compare hashes-per-second and elapsed time side by side. On some machines MD5 will be faster; on others the gap can be smaller. Either way, the demo makes the key lesson visible: **both MD5 and SHA-256 are fast**, which is exactly why they’re not ideal for password storage.

*Screenshot.*  
We’ve included two screenshots: one before clicking “Run comparison” (title, description, password field, button) and one after (results with the password, both hashes, dictionary size, and the two timing boxes). The before-and-after makes it clear that anyone can run this and see for themselves how quickly guessing attacks can run against fast hashes, and how the observed speeds compare on the same machine.

---

## Group Work

We split things up by component and kept in touch so everything fit together.

**Member 1** took the core cracking logic. That meant writing the password generator (random 12 chars from letters and digits), the wordlist builder (candidates that include the target, right size and length, then shuffle), and the MD5/SHA-256 hashing helpers. They also wrote the dictionary-attack function—takes a target hash, wordlist, and hash function, returns the cracked password (if found), elapsed time, and attempt count—and the top-level `run_comparison` that wires it all together. They tested it from the command line to make sure both hashes got cracked and the timing looked right. For the report, they wrote the Methodology and Diagram sections and checked that the backend matched what the comparison actually does.

**Member 2** handled the Flask backend and docs. They set up the app, the route that serves the frontend, and the comparison endpoint (GET with optional password in the query, POST with optional password in the body). They made sure that when no password comes in, we pass nothing to the core so it generates one, and that the dictionary size comes from the environment. They also set up CORS and static file serving so the frontend could load and talk to the API. For the README they wrote the “How to test” steps (venv, install, run server, open browser, etc.), the note about port 5000 and how to use a different port, and the “Sharing on GitHub” section. They wrote the Problem Statement for the report and double-checked that the frontend was calling the API correctly.

**Member 3** built the frontend. They designed the layout and styling—dark theme, readable fonts, different colors for MD5 vs SHA-256 so the results are easy to scan. They added the password input, the “Run comparison” button, and the results area that shows the password, both hashes, dictionary size, and timing for each algorithm. They wrote the JavaScript that hits the comparison endpoint (POST when there’s a password, GET when the field is empty) and added the loading spinner and error messages for when the server’s down. For the report they wrote the Introduction and References, pulled in the NIST and OWASP citations in APA format, and took the before-and-after screenshots.

We all reviewed each other’s code and report sections, pushed changes through the shared repo, and ran through the full flow together to make sure everything worked end to end.

---

## Challenges

We hit a few snags along the way. Here’s what happened and how we dealt with it.

**Port 5000 was already taken.**  
When one of us tried to run the Flask server, we got “address already in use.” Turns out on macOS, AirPlay Receiver grabs port 5000 by default. We didn’t want teammates to get stuck on that, so we put it in the README: you can either turn off AirPlay in System Settings (General → AirDrop & Handoff) or run the server on a different port like 5001 and open that URL instead. We also mentioned it in the report so if someone hits the same error they know it’s a Mac thing, not our code. Didn’t change what we built, but it did change how we wrote the setup instructions.

**We only had random passwords at first.**  
Originally the demo only generated a random password. While testing we realized it would be way more useful to let people type their own—like “password123”—so you could follow along and the hashes would be reproducible. Adding that meant touching all three layers: the core needed to accept an optional password, the API needed to take it from GET or POST and pass it through, and the frontend needed the input field and the logic to send it. We did the backend first (core + API), then the frontend, and tested both paths. Made the demo a lot better for live demos.

**Making the comparison actually fair.**  
We wanted the timing to be apples-to-apples: same password, same wordlist, same number of hashes. At first we thought about stopping the attack as soon as we found the password, but that would skew things—if the password was near the start for one run and near the end for another, the times wouldn’t be comparable. So we decided to always run through the full wordlist and measure total time. We also shuffle the list so the password’s position is random. That meant our attack function can’t short-circuit on a match when we’re measuring (we still record the cracked password for the output). Took a bit of thinking to nail down what “fair” meant before we coded it, but it was important for the demo to actually show what we wanted.

**What we’d do next.**  
If we kept going, we’d add bcrypt or Argon2 to show how much slower a real password hash is. A simple chart of the timing difference would be nice too. We could also let people upload or pick different wordlists to see how size affects crack time, or add pytest so we don’t break things when we change the code.

---

## References

National Institute of Standards and Technology. (2010). *Recommendation for password-based key derivation: Part 1: Storage applications* (NIST Special Publication 800-132). U.S. Department of Commerce. https://csrc.nist.gov/publications/detail/sp/800-132/final

National Institute of Standards and Technology. (2015). *Secure hash standard (SHS)* (FIPS 180-4). U.S. Department of Commerce. https://csrc.nist.gov/publications/detail/fips/180/4/final

OWASP. (n.d.). *Password storage cheat sheet*. OWASP Foundation. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
