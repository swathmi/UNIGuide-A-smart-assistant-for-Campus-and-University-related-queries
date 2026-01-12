import pandas as pd
import re

# ================= LOAD EXCEL =================
DATA_PATH = "data/students.xlsx"
df = pd.read_excel(DATA_PATH)
EXCLUDED_KEYWORDS = [
    "counseling", "admission", "apply", "process",
    "eamcet", "ecet", "management", "quota",
    "eligibility", "seat", "allotment"
]


# ================= COLUMN RENAME (CRITICAL FIX) =================
# Excel column names → Internal standard names
COLUMN_RENAME_MAP = {
    "REGD NO": "REG_NO",
    "STDNT PH.NO": "STUDENT_PHONE",
    "PARENT PH.NO": "PARENT_PHONE",
    "PERSONAL MAIL ID": "PERSONAL_EMAIL",
    "DOMAIN MAIL-ID": "DOMAIN_EMAIL",
    "SSC %": "SSC",
    "INTER/DIPLOMA %": "INTER",
    "TOTAL BACKLOGS": "BACKLOGS",
    "B.TECH %": "BTECH"
}

df.rename(columns=COLUMN_RENAME_MAP, inplace=True)
df.columns = df.columns.str.upper()

# DEBUG (keep for first run, you can remove later)
print("FINAL COLUMNS:", df.columns.tolist())

# ================= FIELD ALIASES (11 COLUMNS) =================
FIELD_ALIASES = {

    "REG_NO": [
        "REGD NO", "REG NO", "REGISTER NUMBER", "REGISTRATION NUMBER",
        "ROLL NO", "ROLL NUMBER", "HALL TICKET", "HALL TICKET NUMBER",
        "HTNO", "HT NO"
    ],

    "NAME": [
        "NAME", "STUDENT NAME", "CANDIDATE NAME", "FULL NAME"
    ],

    "BRANCH": [
        "BRANCH", "DEPARTMENT", "DEPT", "STREAM", "COURSE",
        "SPECIALIZATION", "SPEC"
    ],

    "STUDENT_PHONE": [
        "PHONE", "PHONE NUMBER", "MOBILE", "MOBILE NUMBER",
        "CONTACT", "CONTACT NUMBER", "STUDENT PHONE",
        "STUDENT MOBILE"
    ],

    "PARENT_PHONE": [
        "PARENT PHONE", "PARENT MOBILE", "PARENT PH NO",
        "FATHER PHONE", "FATHER MOBILE",
        "MOTHER PHONE", "MOTHER MOBILE",
        "GUARDIAN PHONE"
    ],

    "PERSONAL_EMAIL": [
        "PERSONAL MAIL", "PERSONAL EMAIL", "EMAIL", "MAIL ID", "EMAIL ID",
        "GMAIL", "YAHOO MAIL", "OUTLOOK MAIL"
    ],

    "DOMAIN_EMAIL": [
        "DOMAIN MAIL", "DOMAIN EMAIL", "COLLEGE MAIL",
        "OFFICIAL MAIL", "INSTITUTIONAL MAIL", "DOMAIN MAIL ID",
        "STUDENT DOMAIN MAIL"
    ],

    "SSC": [
        "SSC", "10TH", "TENTH", "TENTH CLASS",
        "10TH MARKS", "10TH PERCENTAGE", "SSC%", "10TH%",
        "SSC MARKS", "SSC PERCENTAGE",
        "SCHOOL MARKS"
    ],

    "INTER": [
        "INTER", "INTERMEDIATE", "12TH", "TWELFTH",
        "INTER MARKS", "INTER PERCENTAGE", "INTER %",
        "12TH MARKS", "12TH PERCENTAGE",
        "DIPLOMA", "DIPLOMA MARKS"
    ],

    "BTECH": [
        "BTECH", "B.TECH", "ENGINEERING",
        "DEGREE", "GRADUATION",
        "BTECH MARKS", "BTECH PERCENTAGE",
        "DEGREE PERCENTAGE", "CGPA", "BTECH CGPA"
    ],

    "BACKLOGS": [
        "BACKLOG", "BACKLOGS", "ARREARS",
        "SUPPLIES", "SUPPLEMENTARY",
        "PENDING SUBJECTS", "FAILED SUBJECTS"
    ]
}

# ================= UTIL =================
def clean(text):
    return text.upper().strip()

# ================= WHO DETECTION =================
def detect_who(text):
    # REGD NO (example: 22221A4235)
    reg = re.search(r"\b\d{5}[A-Z]\d{4}\b", text)
    if reg:
        return {"type": "REG_NO", "value": reg.group()}

    # BRANCH
    for b in df["BRANCH"].dropna().unique():
        if b in text:
            return {"type": "BRANCH", "value": b}

    # EXACT NAME
    for n in df["NAME"].dropna().unique():
        if n in text:
            return {"type": "NAME", "value": n}

    # PARTIAL NAME (safe)
    words = text.split()
    for w in words:
        if len(w) >= 3:
            matches = df[df["NAME"].str.contains(w, case=False, na=False)]
            if not matches.empty:
                return {"type": "PARTIAL", "value": matches}

    return None

# ================= WHAT DETECTION (USES FIELD_ALIASES) =================
def detect_what(text):

    if "HOW MANY" in text or "COUNT" in text:
        return {"type": "COUNT"}

    if "TOPPER" in text or "HIGHEST" in text or "LOWEST" in text:
        return {"type": "RANK"}

    for field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            if alias in text:
                return {"type": "FIELD", "value": field}

    return {"type": "FULL"}

# ================= CONDITIONS =================
def detect_conditions(text):
    cond = {}

    if "NO BACKLOG" in text or "ZERO BACKLOG" in text:
        cond["BACKLOGS_EQ"] = 0

    if "MORE THAN" in text:
        m = re.search(r"MORE THAN\s+(\d+)", text)
        if m:
            cond["BACKLOGS_GT"] = int(m.group(1))

    if "ABOVE" in text:
        m = re.search(r"ABOVE\s+(\d+)", text)
        if m:
            cond["BTECH_GT"] = int(m.group(1))

    if "BELOW" in text:
        m = re.search(r"BELOW\s+(\d+)", text)
        if m:
            cond["BTECH_LT"] = int(m.group(1))

    if "BETWEEN" in text:
        nums = re.findall(r"\d+", text)
        if len(nums) == 2:
            cond["BTECH_BETWEEN"] = (int(nums[0]), int(nums[1]))

    return cond

# ================= FORMAT =================
def format_student(s):
    return (
        f"👤 Name: {s['NAME']}\n"
        f"🆔 Regd No: {s['REG_NO']}\n"
        f"🏫 Branch: {s['BRANCH']}\n"
        f"📞 Student Phone: {s['STUDENT_PHONE']}\n"
        f"📞 Parent Phone: {s['PARENT_PHONE']}\n"
        f"📧 Personal Email: {s['PERSONAL_EMAIL']}\n"
        f"📧 Domain Email: {s['DOMAIN_EMAIL']}\n"
        f"📊 SSC %: {s['SSC']}\n"
        f"📊 Inter %: {s['INTER']}\n"
        f"📊 B.Tech %: {s['BTECH']}\n"
        f"📚 Backlogs: {s['BACKLOGS']}"
    )

# ================= MASTER ENGINE =================
def handle_student_query(query):
    q = query.lower()

    # ❌ DO NOT treat admission/counseling queries as student queries
    if any(word in q for word in EXCLUDED_KEYWORDS):
        return None   # 🔥 IMPORTANT FIX

    # existing student logic continues below
    ...

    text = clean(query)
    data = df.copy()

    who = detect_who(text)
    what = detect_what(text)
    cond = detect_conditions(text)

    if not who:
        return None

    # WHO FILTER
    if who["type"] == "REG_NO":
        data = data[data["REG_NO"] == who["value"]]
        if data.empty:
            return "❌ No student found with this register number."

    elif who["type"] == "BRANCH":
        data = data[data["BRANCH"] == who["value"]]

    elif who["type"] == "NAME":
        data = data[data["NAME"] == who["value"]]
        if len(data) > 1:
            return "⚠ Multiple students found. Please specify register number."

    elif who["type"] == "PARTIAL":
        if len(who["value"]) > 1:
            return "⚠ Multiple matches found:\n" + "\n".join(
                f"{r['NAME']} ({r['REG_NO']})"
                for _, r in who["value"].iterrows()
            )
        data = who["value"]

    # CONDITIONS FILTER
    if "BACKLOGS_EQ" in cond:
        data = data[data["BACKLOGS"] == cond["BACKLOGS_EQ"]]

    if "BACKLOGS_GT" in cond:
        data = data[data["BACKLOGS"] > cond["BACKLOGS_GT"]]

    if "BTECH_GT" in cond:
        data = data[data["BTECH"] > cond["BTECH_GT"]]

    if "BTECH_LT" in cond:
        data = data[data["BTECH"] < cond["BTECH_LT"]]

    if "BTECH_BETWEEN" in cond:
        lo, hi = cond["BTECH_BETWEEN"]
        data = data[(data["BTECH"] >= lo) & (data["BTECH"] <= hi)]

    if data.empty:
        return "⚠ No data found for this condition."

    # WHAT EXECUTION
    if what["type"] == "COUNT":
        return f"📊 Count: {len(data)}"

    if what["type"] == "RANK":
        top = data.sort_values("BTECH", ascending=False).iloc[0]
        return f"🏆 Topper: {top['NAME']} ({top['BTECH']}%)"

    if what["type"] == "FIELD":
        value = data.iloc[0][what["value"]]
        return f"{what['value'].replace('_',' ')}: {value}"

    return format_student(data.iloc[0])
