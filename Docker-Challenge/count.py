import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for
import redis

app = Flask(__name__)

# Config (don't forget to overwrite these envs in the compose.yml file e.g update owner env to mine.)
SITE_TITLE = os.getenv("SITE_TITLE", "Visit Tracker Pro")
OWNER_NAME = os.getenv("OWNER_NAME", "Your Name")
OWNER_TAGLINE = os.getenv("OWNER_TAGLINE", "DevOps & Cloud Enthusiast")
OWNER_BIO = os.getenv(
    "OWNER_BIO",
    ("DevOps Engineer who loves to automate with CI/CD, and containerize all the things. "
     "This tiny app tracks visits and pins random locations on a map to keep things fun.")
)
GITHUB_URL = os.getenv("GITHUB_URL", "")
LINKEDIN_URL = os.getenv("LINKEDIN_URL", "")
ENABLE_RESET = os.getenv("ENABLE_RESET", "false").lower() == "true"

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

QUOTES = [
    "Ship small, ship often.",
    "Automation is the art of not doing the same thing twice.",
    "If it hurts, do it more often — until it doesn’t.",
    "Simplicity scales.",
    "Remember Abdikarim, motivation is volatile, consistency is key." ,
    "Logs tell stories; metrics reveal truth; traces connect the dots.",
    "Containers keep it tidy. CI/CD keeps it moving.",
    "Your future self thanks you for writing docs.",
    "Good tests are a love letter to your codebase.",
    "Measure what matters, not what’s easy.",
    "Bash it till you can Python it."
]

def get_visit_count():
    try:
        return int(r.get("visits") or 0)
    except Exception:
        return 0

@app.route("/")
def home():
    count = get_visit_count()
    quote = random.choice(QUOTES)
    return render_template(
        "index.html",
        site_title=SITE_TITLE,
        owner_name=OWNER_NAME,
        owner_tagline=OWNER_TAGLINE,
        quote=quote,
        count=count,
        enable_reset=ENABLE_RESET
    )

@app.route("/visit")
def visit():
    # Increment visit count
    count = r.incr("visits")

    # Add a new random location marker
    lat = random.uniform(-70.0, 70.0)      # avoid extreme poles for better map visuals
    lng = random.uniform(-170.0, 170.0)
    marker = {
        "lat": round(lat, 4),
        "lng": round(lng, 4),
        "ts": datetime.utcnow().isoformat() + "Z",
        "note": f"Visit #{count}"
    }
    r.lpush("locations", json.dumps(marker))
    # Trim to last 200 markers to keep memory tidy
    r.ltrim("locations", 0, 199)

    return redirect(url_for("home"))

@app.route("/count")
def count():
    count = r.incr("visits")
    return f"This page has been visited {count} times."

@app.route("/api/visits")
def api_visits():
    return jsonify({"visits": get_visit_count()})

@app.route("/api/locations")
def api_locations():
    raw = r.lrange("locations", 0, 199)
    out = []
    for x in raw:
        try:
            out.append(json.loads(x))
        except Exception:
            pass
    return jsonify({"locations": out})

@app.route("/about")
def about():
    return render_template(
        "about.html",
        site_title=SITE_TITLE,
        owner_name=OWNER_NAME,
        owner_tagline=OWNER_TAGLINE,
        owner_bio=OWNER_BIO,
        github_url=GITHUB_URL,
        linkedin_url=LINKEDIN_URL,
    )

@app.route("/reset")
def reset():
    if not ENABLE_RESET:
        return "Reset disabled. Set ENABLE_RESET=true to allow.", 403
    r.delete("visits")
    r.delete("locations")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)





