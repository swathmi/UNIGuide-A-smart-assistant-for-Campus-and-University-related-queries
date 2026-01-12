from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# ================= STUDENTS SERVICE =================
from services.students_service import handle_student_query

# ================= INTENT DETECTORS =================
from services.programs_intents import detect_courses_programs_intent
from services.college_overview_intents import detect_college_overview_intent
from services.admissions_intents import detect_admission_intent
from services.events_intents import detect_events_intent

# ================= SERVICE FUNCTIONS =================
from services.programs_service import get_courses_programs_response
from services.college_overview_service import get_college_overview_response
from services.admissions_service import get_admissions_response
from services.events_services import get_events_response

# ================= FLASK APP =================
app = Flask(__name__)
CORS(app)

# ================= DOMAIN KEYWORDS =================
PROGRAM_KEYWORDS = [
    "course", "courses", "program", "programs",
    "ug", "pg", "btech", "mtech",
    "intake", "seats", "capacity",
    "fees", "fee", "package", "salary", "lpa",
    "eligibility", "internship", "placement",
    "code", "syllabus", "curriculum"
]

EVENT_KEYWORDS = [
    "event", "events", "activities",
    "technical", "cultural", "sports",
    "workshop", "seminar", "guest lecture",
    "hackathon", "symposium",
    "club", "nss", "ncc",
    "career", "alumni"
]

ADMISSION_KEYWORDS = [
    "admission", "apply", "join",
    "eamcet", "ecet", "management quota",
    "lateral entry", "documents",
    "counseling", "seat allotment",
    "reservation", "degree"
]

# ================= HOME ROUTE =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= CHAT ROUTE =================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"answer": "Please ask a valid question."})

    lower_query = user_query.lower()

    # ==================================================
    # 🔥 1️⃣ COLLEGE OVERVIEW DOMAIN (MANAGEMENT FIRST)
    # ==================================================
    intent = detect_college_overview_intent(lower_query)
    if intent:
        return jsonify({"answer": get_college_overview_response(intent)})

    # ==================================================
    # 🔥 2️⃣ STUDENTS DOMAIN
    # ==================================================
    student_response = handle_student_query(user_query)
    if student_response is not None:
        return jsonify({"answer": student_response})

    # ==================================================
    # 🔥 3️⃣ PROGRAMS DOMAIN
    # ==================================================
    if any(k in lower_query for k in PROGRAM_KEYWORDS):
        intent = detect_courses_programs_intent(lower_query)
        if intent:
            return jsonify({"answer": get_courses_programs_response(intent)})

    # ==================================================
    # 🔥 4️⃣ EVENTS DOMAIN
    # ==================================================
    if any(k in lower_query for k in EVENT_KEYWORDS):
        intent = detect_events_intent(lower_query)
        if intent:
            return jsonify({"answer": get_events_response(intent)})

    # ==================================================
    # 🔥 5️⃣ ADMISSIONS DOMAIN
    # ==================================================
    if any(k in lower_query for k in ADMISSION_KEYWORDS):
        intent = detect_admission_intent(lower_query)
        if intent:
            return jsonify({"answer": get_admissions_response(intent)})

    # ==================================================
    # 🧠 SMART FALLBACK
    # ==================================================
    return jsonify({
        "answer": (
            "🤖 I can help you with:\n\n"
            "👨‍🎓 Student Details & Analysis\n"
            "🎓 Courses & Programs\n"
            "🎉 Events & Activities\n"
            "📝 Admissions & Eligibility\n"
            "🏫 College Information\n\n"
            "👉 Please ask your question clearly."
        )
    })


# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True)
