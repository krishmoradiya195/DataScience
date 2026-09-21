"""
Data Science Portfolio - Flask app
Entry point for Vercel's Python serverless runtime.
Vercel auto-detects any file under /api that exposes a WSGI `app`
object and turns it into a serverless function.
"""
import os
import json
import datetime
import urllib.request
from flask import Flask, render_template, request, jsonify

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="..",
    static_url_path="",
)

PROFILE = {
    "name": "Krish Moradiya",
    "role": "Python for data science",
    "institute": "New L.J Institute of Technology",
    "tagline": "Turning data into decisions, one model at a time.",
    "about": (
        "I'm currently pursuing my degree with a focus on Data Science. "
        "I'm interested in statistics, machine learning and building "
        "end-to-end pipelines that turn raw data into something useful."
    ),
}

SKILL_GROUPS = [
    {
        "id": "01",
        "category": "LANGUAGES & CORE",
        "title": "Programming & Math",
        "desc": "Core languages and the statistics that sit underneath every model.",
        "tags": ["Python", "SQL", "R", "Statistics", "Linear Algebra"],
    },
    {
        "id": "02",
        "category": "DATA STACK",
        "title": "Data Analysis",
        "desc": "Cleaning, exploring and visualizing data before modeling it.",
        "tags": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Power BI"],
    },
    {
        "id": "03",
        "category": "MACHINE LEARNING",
        "title": "Modeling & ML",
        "desc": "Building, evaluating and deploying predictive models.",
        "tags": ["Scikit-learn", "TensorFlow", "PyTorch", "XGBoost"],
    },
    {
        "id": "04",
        "category": "TOOLS",
        "title": "Dev & MLOps Tools",
        "desc": "The tooling used to ship data science work like real software.",
        "tags": ["Git", "Jupyter", "Docker", "Flask", "Vercel"],
    },
]

PROJECTS = [
    {
        "title": "Customer Churn Predictor",
        "desc": "An end-to-end pipeline that cleans customer data, engineers "
        "features and predicts churn probability with a gradient-boosted model.",
        "tags": ["Python", "Pandas", "Scikit-learn", "Flask"],
    },
    {
        "title": "Sales Forecast Dashboard",
        "desc": "A time-series forecasting app that projects next-quarter "
        "revenue from historical sales data, with an interactive chart view.",
        "tags": ["Python", "Prophet", "Plotly", "Pandas"],
    },
    {
        "title": "Image Classifier API",
        "desc": "A small CNN trained to classify product images, wrapped in a "
        "REST API so other apps can send an image and get a label back.",
        "tags": ["TensorFlow", "Flask", "REST API"],
    },
]

JOURNEY = [
    {"label": "CURRENT", "title": "Data Science Coursework", "desc": "Building a foundation in statistics, Python and machine learning."},
    {"label": "2026", "title": "Applied ML Projects", "desc": "Working through real datasets end-to-end: cleaning, modeling, deploying."},
    {"label": "NEXT GOAL", "title": "Deploy Production ML", "desc": "Ship a model behind an API that real users can call."},
]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=PROFILE,
        skill_groups=SKILL_GROUPS,
        projects=PROJECTS,
        journey=JOURNEY,
        year=datetime.datetime.utcnow().year,
    )


@app.route("/api/contact", methods=["POST"])
def contact():
    """Receives the contact form. Wire this up to an email service
    (e.g. Resend, SendGrid) or a database once you're ready."""
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    # TODO: send an email or store this in a database.
    print(f"New contact message from {name} <{email}>: {message}")

    return jsonify({"status": "ok", "message": "Thanks! I'll get back to you soon."})


@app.route("/api/track", methods=["POST"])
def track():
    """
    Logs one page-view event, keyed by an anonymous visitor id, to Supabase.
    This is what makes user-wise (per-visitor) usage monitoring possible --
    see the README for setup. If SUPABASE_URL / SUPABASE_KEY aren't set,
    this silently no-ops so the app still works without a database.
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    payload = request.get_json(silent=True) or {}
    event = {
        "visitor_id": payload.get("visitor_id"),
        "page": payload.get("page", "/"),
        "referrer": request.headers.get("Referer", ""),
        "user_agent": request.headers.get("User-Agent", ""),
        "ip": request.headers.get("x-forwarded-for", request.remote_addr),
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    if not supabase_url or not supabase_key:
        return jsonify({"status": "skipped", "reason": "analytics not configured"}), 200

    try:
        req = urllib.request.Request(
            f"{supabase_url}/rest/v1/page_views",
            data=json.dumps(event).encode(),
            headers={
                "Content-Type": "application/json",
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Prefer": "return=minimal",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
        return jsonify({"status": "logged"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500


# Vercel's Python runtime looks for a module-level WSGI `app` -- nothing
# else needed here. Locally, run with: python api/index.py
if __name__ == "__main__":
    app.run(debug=True, port=5000)
