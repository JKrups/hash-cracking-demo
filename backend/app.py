# """
# Flask API for MD5 vs SHA-256 dictionary attack demo.
# Serves the comparison endpoint and static frontend.
# CSI 3480 Security and Privacy in Computing - Winter 2026
# """

# import os
# from flask import Flask, jsonify, request, send_from_directory
# from flask_cors import CORS

# from cracker import run_comparison

# app = Flask(__name__, static_folder="../frontend", static_url_path="")
# CORS(app)

# # Optional: limit dict size for faster demo (e.g. 10_000). Use 25_000 for clearer difference.
# DEFAULT_DICT_SIZE = 20_000


# @app.route("/")
# def index():
#     """Serve the frontend."""
#     return send_from_directory(app.static_folder, "index.html")


# @app.route("/api/compare", methods=["GET", "POST"])
# def compare():
#     """
#     Run one comparison: use provided password or generate one, hash with MD5 and SHA-256,
#     run dictionary attack on both, return timings and results.
#     """
#     dict_size = int(os.environ.get("DICT_SIZE", DEFAULT_DICT_SIZE))
#     password = None
#     if request.method == "POST" and request.is_json:
#         password = (request.get_json() or {}).get("password") or None
#     if password is None:
#         password = request.args.get("password")
#     if password is not None and isinstance(password, str) and not password.strip():
#         password = None
#     result = run_comparison(dict_size=dict_size, password=password)
#     return jsonify(result)


# @app.route("/api/health")
# def health():
#     return jsonify({"status": "ok"})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
