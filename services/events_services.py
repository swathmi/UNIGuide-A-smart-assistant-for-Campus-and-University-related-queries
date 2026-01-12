import json
import os
from services.response_formatter import format_lines

# ================= LOAD JSON DATA =================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "event_activities.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    events_data = json.load(f)


# ================= HELPER =================
def section(title, points, emoji="🔹"):
    return format_lines(title, points, emoji)


# ================= MAIN SERVICE FUNCTION =================
def get_events_response(intent):

    # ==================================================
    # 🔹 GENERAL EVENTS LIST
    # ==================================================
    if intent == "EVENTS_LIST":
        return section(
            "🎉 Events & Activities at BVCEC",
            events_data["events_overview"],
            "🔹"
        )

    # ==================================================
    # 🔹 ACADEMIC & TECHNICAL
    # ==================================================
    elif intent == "TECHNICAL_EVENTS":
        d = events_data["technical_events"]
        return section("💻 Technical Events – Overview", d["definition"]) + "\n\n" + \
               section("🎯 Purpose", d["purpose"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent == "HACKATHONS":
        d = events_data["hackathons"]
        return section("🚀 Hackathons – What & Why", d["definition"]) + "\n\n" + \
               section("🎯 Purpose", d["purpose"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"]) + "\n\n" + \
               section("🎓 Benefits for Students", d["benefits_for_students"]) + "\n\n" + \
               section("📘 Benefits for Faculty", d["benefits_for_faculty"])

    elif intent == "WORKSHOPS":
        d = events_data["workshops"]
        return section("🛠️ Workshops – Overview", d["definition"]) + "\n\n" + \
               section("🎯 Purpose", d["purpose"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent == "SEMINARS":
        d = events_data["seminars"]
        return section("🎤 Seminars – Overview", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent == "GUEST_LECTURES":
        d = events_data["guest_lectures"]
        return section("👨‍💼 Guest Lectures – Overview", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    # 🔹 CULTURAL & SOCIAL
    # ==================================================
    elif intent == "CULTURAL_EVENTS":
        d = events_data["cultural_events"]
        return section("🎭 Cultural Events", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent == "COLLEGE_FESTS":
        d = events_data["college_fests"]
        return section("🎉 College Fests", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    # 🔹 SPORTS & FITNESS
    # ==================================================
    elif intent in ["SPORTS_EVENTS", "ANNUAL_SPORTS_MEET", "INTERCOLLEGE_SPORTS", "YOGA_FITNESS"]:
        d = events_data["sports_events"]
        return section("🏅 Sports & Fitness Activities", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    # 🔹 CLUBS & STUDENT BODIES
    # ==================================================
    elif intent in [
        "CLUB_ACTIVITIES", "CODING_CLUBS", "ROBOTICS_AI_CLUBS",
        "CULTURAL_CLUBS", "ENTREPRENEURSHIP_CELL", "PROFESSIONAL_SOCIETIES"
    ]:
        d = events_data["club_activities"]
        return section("🎯 Club Activities", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    # 🔹 SOCIAL RESPONSIBILITY & LEADERSHIP
    # ==================================================
    elif intent == "NSS_ACTIVITIES":
        d = events_data["nss_activities"]
        return section("🤝 NSS Activities", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent == "NCC_ACTIVITIES":
        d = events_data["ncc_activities"]
        return section("🎖️ NCC Activities", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    elif intent in ["COMMUNITY_SERVICE", "BLOOD_DONATION", "ENVIRONMENTAL_AWARENESS"]:
        d = events_data["nss_activities"]
        return section("🌱 Social Responsibility Activities", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"])

    # ==================================================
    # 🔹 INNOVATION, CAREER & EXPOSURE
    # ==================================================
    elif intent in [
        "STARTUP_INNOVATION", "CAREER_GUIDANCE",
        "PLACEMENT_TRAINING", "ALUMNI_INTERACTION",
        "INDUSTRY_INTERACTION"
    ]:
        d = events_data["innovation_and_career_programs"]
        return section("🚀 Innovation & Career Programs", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    # 🔹 RECOGNITION & PARTICIPATION
    # ==================================================
    elif intent in [
        "STUDENT_ACHIEVEMENTS", "FACULTY_ACHIEVEMENTS",
        "EXTERNAL_COMPETITIONS", "NATIONAL_PARTICIPATION"
    ]:
        d = events_data["recognition_and_participation"]
        return section("🏆 Achievements & Participation", d["definition"]) + "\n\n" + \
               section("👨‍🎓 Student Activities", d["student_activities"]) + "\n\n" + \
               section("👩‍🏫 Faculty Activities", d["faculty_activities"])

    # ==================================================
    return "Sorry, I could not find the event information you requested."
