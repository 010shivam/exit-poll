from flask import Blueprint, render_template, request, redirect,make_response, flash,get_flashed_messages
import requests

from app.db import get_connection
from .utils import get_hash

main = Blueprint("main", __name__)

@main.route("/")
def home():
    messages = get_flashed_messages(with_categories=True)
    print("Messages:", messages)
    mix_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = mix_ip.split(",")[0].strip()
    print("IP",ip)
    ua = request.user_agent
    ip_hash = get_hash(ip, str(ua))
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM responses WHERE ip_hash = ?", (ip_hash,))
    if cursor.fetchone():
        return render_template("form.html", message="You have already submitted your vote!", message_type="error")
    return render_template("form.html",messages=messages)
@main.route("/submit", methods=["POST"])
def submit():
    mix_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = mix_ip.split(",")[0].strip()
    ua = request.user_agent
    ip_hash = get_hash(ip, str(ua))
    ppp = requests.get(f"http://ip-api.com/json/{ip}")
    location = "Unknown"
    print(ppp.json())
    if ppp.status_code == 200:
        if ppp.json().get("status") == "success":
            location = ppp.json()["regionName"]
    print("Location:", location)
    vote = request.form.get("vote")
    district = request.form.get("district")
    age_group = request.form.get("age_group")
    gender = request.form.get("gender")

    if not all([vote, district, age_group, gender]):
        flash("All fields are required!", "error")
        return redirect("/")
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM responses WHERE ip_hash = ?", (ip_hash,))
    if cursor.fetchone():
        flash("Duplicate Voting", "warning")
        return redirect("/")
    
    cursor.execute("""
        INSERT INTO responses (ip_hash, vote, age_group,district, gender,voter_location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ip_hash, vote, age_group, district, gender, location))
    conn.commit()
    conn.close()

    flash("Vote submitted successfully", "success")
    return redirect("/")
    response.set_cookie(
        "voted",
        "true",
        max_age=60*60*24*365  # 1 year
    )

@main.route("/results")
def results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM responses")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return { "results": result }