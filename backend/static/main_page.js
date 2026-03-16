console.log("JS file loaded!");

function sendData() {
    const input = document.getElementById("userInput");
    if (!input) {
        console.error("Input element not found!");
        return;
    }
    const value = input.value.trim();
    if (value.length < 12){
        alert("Please enter a password with at least 12 characters.");
        return;
    }

    const password = input.value.trim();
    if (!password) return;

    fetch("/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password })
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server replied ${res.status}`);
        return res.json();
    })
    .then(data => {
        document.getElementById("md5").innerText = data.md5 || "N/A";
        document.getElementById("sha_256").innerText = data.sha_256 || "N/A";
        document.getElementById("bcrypt").innerText = data.bcrypt || "N/A";
    })
    .catch(err => {
        console.error("Fetch error:", err);
        document.getElementById("response").innerText = "Error: " + err.message;
    });

}

document.getElementById("userInput").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendData();
        }
    });