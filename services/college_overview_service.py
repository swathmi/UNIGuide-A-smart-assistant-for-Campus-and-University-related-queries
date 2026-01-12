import json
import os
from services.response_formatter import format_lines



# ---------------- LOAD JSON DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "college_overview.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    college_data = json.load(f)

# ================= HELPER FUNCTIONS =================

def to_list(text):
    """Converts paragraph text into a list"""
    if isinstance(text, list):
        return text
    return [text]


def format_response(title, points, emoji="🔹"):
    """
    Converts any content into neat
    line-by-line emoji formatted response
    """
    response = f"{title}:\n\n"
    for point in points:
        response += f"{emoji} {point}\n"
    return response.strip()


def get_management_profile(designation):
    for member in college_data["management"]["members"]:
        if member["designation"].lower() == designation.lower():
            return {
                "type": "profile_with_text",
                "name": member["name"],
                "designation": member["designation"],
                "description": member["description"],
                "photo": member["photo"]
            }
    return None


# ================= MAIN RESPONSE FUNCTION =================

def get_college_overview_response(intent):

    # -------- BASIC DETAILS --------
    if intent == "COLLEGE_NAME":
        return format_response(
            "🏫 College Name",
            [college_data["basic_identity"]["college_name"]],
            "📘"
        )

    elif intent == "COLLEGE_SHORT_NAME":
        return format_response(
            "🏷️ College Short Name",
            [college_data["basic_identity"]["short_name"]],
            "🔤"
        )

    elif intent == "COLLEGE_CODE":
        return format_response(
            "🏷️ College Code",
            [college_data["basic_identity"]["college_code"]],
            "🔢"
        )

    elif intent == "COLLEGE_TYPE":
        return format_response(
            "🏛️ College Type",
            [college_data["basic_identity"]["college_type"]],
            "🏢"
        )

    elif intent == "ESTABLISHMENT_YEAR":
        return format_response(
            "📅 Establishment Year",
            [f"Established in {college_data['basic_identity']['established_year']}"],
            "📌"
        )

    # -------- VISION & MISSION --------
    elif intent == "COLLEGE_VISION":
        return format_response(
            "🎯 College Vision",
            to_list(college_data["vision_mission"]["vision"]),
            "✨"
        )

    elif intent == "COLLEGE_MISSION":
        return format_response(
            "🚀 College Mission",
            college_data["vision_mission"]["mission"],
            "✅"
        )

    # -------- MANAGEMENT (PHOTO CARDS) --------
    elif intent == "CHAIRMAN_DETAILS":
        return get_management_profile("Chairman")

    elif intent == "FORMER_CHAIRMAN_DETAILS":
        return get_management_profile("Former Chairman")

    elif intent == "FOUNDER_DETAILS":
        return get_management_profile("Founder")

    elif intent == "PRINCIPAL_DETAILS":
        return get_management_profile("Principal")

    elif intent == "VICE_PRINCIPAL_DETAILS":
        return get_management_profile("Vice Principal")

    elif intent == "SECRETARY_DETAILS":
        return get_management_profile("Secretary")

    # -------- LOCATION & CONTACT --------
    elif intent == "COLLEGE_LOCATION":
        loc = college_data["location"]
        return format_response(
            "📍 College Location & Address",
            [
                loc["address"],
                f"Landmark: {loc['landmark']}",
                f"Pincode: {loc['pincode']}"
            ],
            "📌"
        )

    elif intent == "COLLEGE_CONTACT":
        contact = college_data["contact"]
        return format_response(
            "📞 Contact Details",
            [
                f"Office Phone: {contact['office_phone']}",
                f"Admission Helpline: {contact['admission_helpline']}",
                f"Email: {contact['official_email']}"
            ],
            "☎️"
        )

    # -------- ACCREDITATION --------
    elif intent == "COLLEGE_ACCREDITATION":
        acc = college_data["accreditation_and_approvals"]
        return format_response(
            "🏅 Accreditation & Approvals",
            [
                acc["aicte"],
                acc["naac"],
                acc["nba"],
                acc["ugc"]
            ],
            "🎖️"
        )

    # -------- INFRASTRUCTURE --------
    elif intent == "INFRASTRUCTURE":
        return format_response(
            "🏫 Campus Infrastructure & Facilities",
            college_data["campus_and_infrastructure"]["facilities"],
            "🏢"
        )

    # -------- CULTURE --------
    elif intent == "COLLEGE_CULTURE":
        culture = college_data["culture_and_values"]
        return format_response(
            "🌱 College Culture & Values",
            [
                culture["discipline"],
                culture["ethics"]
            ],
            "🌟"
        )

    # -------- TIMINGS --------
    elif intent == "COLLEGE_TIMINGS":
        t = college_data["college_timings"]
        return format_response(
            "⏰ College Timings",
            [
                f"Working Days: {t['working_days']}",
                f"College Hours: {t['college_hours']}"
            ],
            "🕘"
        )

    # -------- WHY CHOOSE COLLEGE --------
    elif intent == "WHY_CHOOSE_COLLEGE":
        return format_response(
            "⭐ Why Choose BVCEC",
            college_data["why_choose_bvcec"]["highlights"],
            "💡"
        )

    return "Sorry, I could not find the information you requested."
