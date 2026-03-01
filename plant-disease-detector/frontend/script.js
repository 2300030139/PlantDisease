// Show preview when image selected
document.getElementById("imageInput").addEventListener("change", function() {
    const file = this.files[0];
    const preview = document.getElementById("preview");

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }
});

// Send image to backend
function uploadImage() {
    let input = document.getElementById("imageInput");
    let file = input.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "🦠 Disease: " + data.disease +
            "<br>📊 Confidence: " + data.confidence + "%";
    })
    .catch(error => {
        alert("Error connecting to backend!");
        console.error(error);
    });
}