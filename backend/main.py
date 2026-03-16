from flask import Flask, render_template, url_for, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a "route" (the URL path)
@app.route("/")
def index():
    # Render the index.html template when the root URL is accessed
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():

    data = request.get_json()
    password = data.get("password", "")
    
    md5_hash = password
    sha_256_hash = password
    bcrypt_hash = password
    

    return jsonify({
        "md5":     md5_hash,
        "sha_256": sha_256_hash,         
        "bcrypt":  bcrypt_hash           
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)