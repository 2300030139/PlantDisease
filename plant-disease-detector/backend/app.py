from flask import Flask, render_template, request
import os
from predict import predict_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===============================
# Disease Information + Severity
# ===============================
disease_info = {
    "Tomato Early blight leaf": {
        "cause": "Fungal infection caused by Alternaria solani in warm and humid conditions.",
        "treatment": "Remove infected leaves and spray Mancozeb or Chlorothalonil fungicide every 7–10 days.",
        "severity": 2
    },
    "Tomato leaf late blight": {
        "cause": "Caused by Phytophthora infestans in cool and wet weather conditions.",
        "treatment": "Use copper-based fungicide and remove infected plants immediately.",
        "severity": 3
    },
    "Tomato leaf": {
        "cause": "Healthy tomato leaf. No disease detected.",
        "treatment": "Maintain proper watering, sunlight and balanced fertilizer.",
        "severity": 0
    },
    "Wheat leaf Healthy": {
        "cause": "Healthy wheat leaf. No disease detected.",
        "treatment": "Maintain good irrigation and field sanitation.",
        "severity": 0
    },
    "Wheat leaf septoria": {
        "cause": "Fungal disease caused by Zymoseptoria tritici in cool and wet climate.",
        "treatment": "Apply Azoxystrobin or Propiconazole fungicide.",
        "severity": 2
    },
    "Wheat leaf stripe_rust": {
        "cause": "Fungal disease caused by Puccinia striiformis in cool temperatures with high humidity.",
        "treatment": "Spray Tebuconazole or Propiconazole fungicide.",
        "severity": 3
    }
}

# ===============================
# Organic vs Chemical Treatments
# ===============================
treatment_options = {
    "Tomato Early blight leaf": {
        "organic": "Neem oil spray every 7 days; remove infected leaves.",
        "chemical": "Mancozeb or Chlorothalonil fungicide spray.",
        "cost": "Organic: ₹250/acre | Chemical: ₹600/acre",
        "eco": "Organic: Eco-friendly | Chemical: Moderate impact"
    },
    "Tomato leaf late blight": {
        "organic": "Garlic extract + baking soda spray.",
        "chemical": "Copper-based fungicide spray.",
        "cost": "Organic: ₹300/acre | Chemical: ₹700/acre",
        "eco": "Organic: Eco-friendly | Chemical: Higher impact"
    },
    "Wheat leaf septoria": {
        "organic": "Trichoderma bio-fungicide spray.",
        "chemical": "Azoxystrobin or Propiconazole spray.",
        "cost": "Organic: ₹280/acre | Chemical: ₹650/acre",
        "eco": "Organic: Eco-friendly | Chemical: Moderate impact"
    },
    "Wheat leaf stripe_rust": {
        "organic": "Cow urine + neem leaf extract spray.",
        "chemical": "Tebuconazole or Propiconazole spray.",
        "cost": "Organic: ₹200/acre | Chemical: ₹600/acre",
        "eco": "Organic: Eco-friendly | Chemical: Moderate impact"
    }
}

# ===============================
# Yield Loss Logic
# ===============================
def predict_yield_loss(severity):
    if severity == 0:
        return 0
    elif severity == 1:
        return 10
    elif severity == 2:
        return 25
    elif severity == 3:
        return 45

# ===============================
# Routes
# ===============================
@app.route("/", methods=["GET", "POST"])
def home():

    # ---------- FIRST PAGE LOAD ----------
    if request.method == "GET":
        return render_template(
            "index.html",
            treatments={}   # IMPORTANT: prevents Jinja error
        )

    # ---------- AFTER IMAGE UPLOAD ----------
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    disease, confidence = predict_image(filepath)

    info = disease_info.get(disease, {
        "cause": "Information not available.",
        "treatment": "Consult agricultural expert.",
        "severity": 1
    })

    severity = info["severity"]
    yield_loss = predict_yield_loss(severity)
    recovery = 100 - yield_loss

    treatments = treatment_options.get(disease, {})

    return render_template(
        "index.html",
        prediction=disease,
        confidence=confidence,
        cause=info["cause"],
        treatment=info["treatment"],
        yield_loss=yield_loss,
        recovery=recovery,
        treatments=treatments,
        image_path=filepath
    )

# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    app.run(debug=True)