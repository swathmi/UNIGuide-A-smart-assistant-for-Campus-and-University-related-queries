from sentence_transformers import SentenceTransformer, util

# ================= LOAD MODEL =================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ================= EVENTS & ACTIVITIES INTENTS =================

EVENTS_INTENTS = {

    # ==================================================
    # 🔹 GENERAL EVENTS LIST
    # ==================================================
    "EVENTS_LIST": [
        "list of events",
        "events in our college",
        "what events are conducted",
        "college events list",
        "events and activities",
        "activities in bvcec"
    ],

    # ==================================================
    # 🔹 ACADEMIC & TECHNICAL
    # ==================================================
    "TECHNICAL_EVENTS": [
        "technical events",
        "academic events",
        "technical activities",
        "technical competitions",
        "technical events in our college"
    ],

    "HACKATHONS": [
        "hackathon",
        "hackathons in our college",
        "do you conduct hackathons",
        "what is hackathon",
        "hackathon benefits",
        "hackathon student activities",
        "hackathon faculty role"
    ],

    "WORKSHOPS": [
        "workshop",
        "workshops in our college",
        "what is workshop",
        "workshop benefits",
        "faculty role in workshop",
        "student activities in workshop"
    ],

    "SEMINARS": [
        "seminar",
        "seminars in our college",
        "what is seminar",
        "seminar benefits",
        "faculty role in seminars"
    ],

    "GUEST_LECTURES": [
        "guest lecture",
        "guest lectures in college",
        "industry expert lectures",
        "guest lecture benefits"
    ],

    "CODING_COMPETITIONS": [
        "coding competition",
        "coding contests",
        "programming competitions",
        "coding events in college"
    ],

    "PAPER_PRESENTATIONS": [
        "paper presentation",
        "research paper presentation",
        "technical paper presentation"
    ],

    "PROJECT_EXPOS": [
        "project expo",
        "project exhibition",
        "student project expo"
    ],

    "INDUSTRIAL_VISITS": [
        "industrial visit",
        "industry visit",
        "company visits for students"
    ],

    "SKILL_DEVELOPMENT_PROGRAMS": [
        "skill development programs",
        "skill training",
        "employability skills programs"
    ],

    "CERTIFICATION_PROGRAMS": [
        "certification programs",
        "certification courses",
        "professional certifications"
    ],

    # ==================================================
    # 🔹 CULTURAL & SOCIAL
    # ==================================================
    "CULTURAL_EVENTS": [
        "cultural events",
        "cultural activities",
        "dance music events",
        "college cultural programs"
    ],

    "COLLEGE_FESTS": [
        "college fest",
        "annual day",
        "college festival",
        "freshers day",
        "farewell event"
    ],

    "LITERARY_EVENTS": [
        "literary events",
        "debate competition",
        "essay writing",
        "elocution"
    ],

    "PHOTOGRAPHY_MEDIA_EVENTS": [
        "photography events",
        "media club activities",
        "photography competitions"
    ],

    # ==================================================
    # 🔹 SPORTS & FITNESS
    # ==================================================
    "SPORTS_EVENTS": [
        "sports events",
        "sports activities",
        "indoor games",
        "outdoor games"
    ],

    "ANNUAL_SPORTS_MEET": [
        "annual sports meet",
        "college sports day"
    ],

    "INTERCOLLEGE_SPORTS": [
        "inter college sports",
        "sports tournaments",
        "inter college tournaments"
    ],

    "YOGA_FITNESS": [
        "yoga activities",
        "fitness programs",
        "health and fitness events"
    ],

    # ==================================================
    # 🔹 CLUBS & STUDENT BODIES
    # ==================================================
    "CLUB_ACTIVITIES": [
        "club activities",
        "student clubs",
        "technical clubs",
        "non technical clubs"
    ],

    "CODING_CLUBS": [
        "coding clubs",
        "programming clubs",
        "coding community"
    ],

    "ROBOTICS_AI_CLUBS": [
        "robotics club",
        "ai club",
        "robotics and ai activities"
    ],

    "CULTURAL_CLUBS": [
        "dance club",
        "music club",
        "drama club"
    ],

    "ENTREPRENEURSHIP_CELL": [
        "entrepreneurship cell",
        "e cell activities",
        "startup club"
    ],

    "PROFESSIONAL_SOCIETIES": [
        "professional societies",
        "csi activities",
        "ieee activities",
        "iste activities"
    ],

    # ==================================================
    # 🔹 SOCIAL RESPONSIBILITY & LEADERSHIP
    # ==================================================
    "NSS_ACTIVITIES": [
        "nss activities",
        "nss programs",
        "social service activities"
    ],

    "NCC_ACTIVITIES": [
        "ncc activities",
        "ncc training",
        "national cadet corps"
    ],

    "COMMUNITY_SERVICE": [
        "community service",
        "village development programs"
    ],

    "BLOOD_DONATION": [
        "blood donation camp",
        "blood donation activities"
    ],

    "ENVIRONMENTAL_AWARENESS": [
        "environment awareness",
        "swachh bharat",
        "cleanliness drives"
    ],

    # ==================================================
    # 🔹 INNOVATION, CAREER & EXPOSURE
    # ==================================================
    "STARTUP_INNOVATION": [
        "startup events",
        "innovation events",
        "startup programs"
    ],

    "CAREER_GUIDANCE": [
        "career guidance",
        "career counseling",
        "career development programs"
    ],

    "PLACEMENT_TRAINING": [
        "placement training",
        "aptitude training",
        "soft skills training"
    ],

    "ALUMNI_INTERACTION": [
        "alumni interaction",
        "alumni meet",
        "interaction with alumni"
    ],

    "INDUSTRY_INTERACTION": [
        "industry interaction",
        "industry experts interaction",
        "industry collaboration"
    ],

    # ==================================================
    # 🔹 RECOGNITION & PARTICIPATION
    # ==================================================
    "STUDENT_ACHIEVEMENTS": [
        "student achievements",
        "student awards",
        "student recognitions"
    ],

    "FACULTY_ACHIEVEMENTS": [
        "faculty achievements",
        "faculty awards",
        "faculty recognitions"
    ],

    "EXTERNAL_COMPETITIONS": [
        "external competitions",
        "outside college competitions"
    ],

    "NATIONAL_PARTICIPATION": [
        "national level events",
        "state level events",
        "national competitions"
    ]
}

# ================= INTENT DETECTION FUNCTION =================

def detect_events_intent(user_query, threshold=0.55):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in EVENTS_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        similarity_scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = similarity_scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent

    return None
