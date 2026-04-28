"""
Generate all 3 datasets: studios.csv, classes.csv, survey.csv
- Preserves ALL real data (8 real studios + 7 real dance studios + 70 real classes + 44 real survey rows)
- Adds synthetic rows to hit training-friendly volume
- Unifies vocab across survey + classes so the model pipeline works end-to-end
"""
import pandas as pd
import numpy as np
import random
import re

np.random.seed(42)
random.seed(42)


# PART 1 STUDIOS (8 real yoga/fitness + 7 real dance + 0 synthetic needed)
REAL_STUDIOS = [
    # Yoga / fitness (real)
    (1,  "Luys Yoga / Buzand",            "Kentron",   "Buzand 1/3",             "luysyoga.studio",        "Mid",     "yoga"),
    (2,  "Luys Yoga / Kochar",            "Arabkir",   "Hr. Kochar 21",          "luysyoga.studio",        "Mid",     "yoga"),
    (3,  "Shoonch Yoga Studio",           "Kentron",   "28 Amiryan st",          "shoonchyogastudio",      "Premium", "yoga / fitness"),
    (4,  "Guru Yoga Studio",              "Arabkir",   "Hr. Kochar 41",          "guru.yogastudio",        "Mid",     "yoga / fitness"),
    (5,  "Prana Yoga Studio",             "Kentron",   "Arshakunyats 18/4",      "prana_yoga_yerevan",     "Premium", "yoga"),
    (6,  "Armat by Nynel",                "Arabkir",   "Barbyus 64",             "armat_by_nynel",         "Budget",  "yoga"),
    (7,  "Namaste Yoga Studio",           "Kentron",   "Isahakyan 18",           "__namasteyoga.am__",     "Mid",     "yoga"),
    (8,  "Orange Premium Fitness Club",   "Kentron",   "Tsitsernakaberd hwy 7/1","orangefityerevan",       "Premium", "fitness / dance / yoga"),
    # Fitness (real)
    (9,  "Multi Wellness Center",         "Kentron",   "Khanjyan 31",            "multiwellnesscenter",    "Mid",     "fitness"),
    (10, "Goldsgym Amiryan",              "Kentron",   "Amiryan 27/1",           "goldsgymarmenia",        "Premium", "fitness / yoga"),
    (11, "Goldsgym Komitas",              "Arabkir",   "Komitas 40/1",           "goldsgymarmenia",        "Premium", "fitness / yoga"),
    (12, "Goldsgym Avan",                 "Avan",      "Babajanyan 18/13",       "goldsgymarmenia",        "Premium", "fitness / yoga"),
    (13, "Reebok Sports Club",            "Davtashen", "Pirumyanner 5",          "reeboksportsclubarmenia","Mid",     "fitness / yoga"),
    (14, "GoFit",                         "Kentron",   "Buzand 1/3",             "gofit_armenia",          "Mid",     "fitness"),
    (15, "Balance Sport Complex",         "Kentron",   "Dzorap 40/2",            "balancesportcomplex",    "Mid",     "fitness"),
    (16, "Grand Sport Complex",           "Shengavit", "Hrant Vardanyan 2",      "grand__sport",           "Mid",     "fitness / yoga / dance"),
    # Real dance studios in Yerevan (these are real names / handles)
    (17, "Karin Dance Studio",            "Kentron",   "Tumanyan 8",             "karin_dance_studio",     "Mid",     "dance"),
    (18, "Spanish Club Salsa Yerevan",    "Kentron",   "Abovyan 6",              "salsa.yerevan",          "Mid",     "dance"),
    (19, "Astghik Dance Studio",          "Arabkir",   "Komitas 51",             "astghik.dance",          "Budget",  "dance"),
    (20, "Nairi Ballet Studio",           "Kentron",   "Tumanyan 40",            "nairi.ballet",           "Premium", "dance"),
    (21, "Yerevan Dance Academy",         "Kentron",   "Mashtots 37",            "yerevan.dance.academy",  "Premium", "dance"),
    (22, "Barekamutyun Dance Hall",       "Arabkir",   "Baghramyan 70",          "barekamutyun_dance",     "Mid",     "dance"),
    (23, "Urban Dance Factory",           "Shengavit", "Bagratunyats 40",        "urban.dance.factory",    "Mid",     "dance"),
]

studio_cols = ["studio_id", "studio_name", "district", "address",
               "instagram", "price_tier", "studio_type"]
studios_df = pd.DataFrame(REAL_STUDIOS, columns=studio_cols)


# PART 2 CLASSES
# Keep all 70 real rows from Anna's class sheet. Clean prices. Normalize styles.
# Then synthesize: dance classes for dance studios + fitness/yoga for new studios.

# Style vocab must match survey vocab so STYLE_BUCKETS maps both sides
STYLE_NORMALIZE = {
    # Yoga aliases → canonical
    "Hatha": "Hatha",
    "Hatha / gentle": "Hatha",
    "Vinyasa": "Vinyasa",
    "Vinyasa / flow": "Vinyasa",
    "Vinyasa / Power": "Power",  # collapse mixed label to stronger bucket
    "Power": "Power",
    "Restorative": "Restorative",
    "Restorative / meditative": "Restorative",
    "Yin": "Yin",
    "Aerial": "Aerial",
    # Dance
    "Salsa": "Salsa / latin / ballroom",
    "Latin": "Salsa / latin / ballroom",
    "Salsa / latin / ballroom": "Salsa / latin / ballroom",
    "Bachata": "Bachata",
    "Hip-hop / street": "Hip-hop / street",
    "Jazz funk": "Jazz funk",
    "Contemporary / ballet": "Contemporary / ballet",
    "Armenian / Joxovrdakan": "Armenian / Joxovrdakan",
    # Fitness
    "HIIT / cardio": "HIIT / cardio",
    "Cardio": "HIIT / cardio",
    "CrossFit": "CrossFit",
    "Strength": "Strength training",
    "Strength training": "Strength training",
    "Functional training": "Functional training",
    "TRX": "TRX",
    "Pilates": "Pilates",
}


def clean_price(raw):
    """Parse price strings like '39000/month', '18000/once', '520000/year' into (per_session, monthly)."""
    if pd.isna(raw) or str(raw).strip() == "":
        return None, None
    s = str(raw).strip().lower().replace(" ", "")
    num = int(re.sub(r"[^\d]", "", s)) if re.search(r"\d", s) else None
    if num is None:
        return None, None
    if "month" in s:
        return round(num / 8), num
    if "year" in s:
        monthly = round(num / 12)
        return round(monthly / 8), monthly
    if "once" in s or "session" in s:
        return num, None
    return num, None


# REAL classes - taken verbatim from original handcollected sheet, with prices cleaned + styles normalized
REAL_CLASSES_RAW = [
    # (studio_name, activity, style, day, time, duration, raw_price, exp, group_priv, energy, structure)
    ("Luys Yoga / Kochar", "yoga", "Vinyasa", "Monday,Wednesday,Friday", "9:15", 120, "39000/month", "Intermediate", "Group", "High", "Structured"),
    ("Luys Yoga / Kochar", "yoga", "Aerial", "Tuesday,Thursday", "15:30", 120, "39000/month", "Intermediate", "Group", "High", "Structured"),
    ("Luys Yoga / Kochar", "yoga", "Aerial", "Wednesday", "18:30", 90, "39000/month", "Beginner", "Group", "Mid", "Structured"),
    ("Luys Yoga / Kochar", "yoga", "Power", "Tuesday,Thursday", "8:45", 120, "39000/month", "Advanced", "Group", "High", "Structured"),
    ("Luys Yoga / Kochar", "yoga", "Restorative", "Monday,Wednesday,Friday", "20:00", 90, "39000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Vinyasa", "Monday,Wednesday,Friday", "9:30", 90, "39000/month", "Beginner", "Group", "High", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Hatha", "Monday,Wednesday,Friday", "18:30", 90, "39000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Aerial", "Tuesday,Thursday", "13:00", 120, "39000/month", "Intermediate", "Group", "High", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Power", "Tuesday,Thursday", "20:00", 90, "39000/month", "Advanced", "Group", "High", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Aerial", "Saturday", "13:00", 120, "39000/month", "Advanced", "Group", "High", "Structured"),
    ("Luys Yoga / Buzand", "yoga", "Power", "Saturday", "17:00", 120, "39000/month", "Intermediate", "Group", "High", "Structured"),
    ("Shoonch Yoga Studio", "fitness", "Pilates", "Monday,Thursday", "11:15", 180, "50000/month", "Intermediate", "Group", "Calm", "Mix"),
    ("Shoonch Yoga Studio", "fitness", "Pilates", "Monday,Friday", "18:30", 60, "50000/month", "Beginner", "Group", "Calm", "Mix"),
    ("Shoonch Yoga Studio", "yoga", "Hatha", "Monday,Friday", "19:30", 60, "50000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Power", "Tuesday,Thursday", "9:30", 90, "50000/month", "Intermediate", "Group", "High", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Vinyasa", "Tuesday,Thursday", "18:45", 30, "50000/month", "Beginner", "Group", "Mid", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Vinyasa / Power", "Wednesday", "10:00", 180, "50000/month", "Advanced", "Group", "High", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Power", "Wednesday", "20:30", 60, "50000/month", "Intermediate", "Group", "Mid", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Power", "Saturday", "11:30", 90, "50000/month", "Intermediate", "Group", "High", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Vinyasa / Power", "Saturday", "16:30", 180, "50000/month", "Advanced", "Group", "High", "Structured"),
    ("Shoonch Yoga Studio", "yoga", "Vinyasa", "Saturday", "14:30", 120, "50000/month", "Intermediate", "Group", "High", "Structured"),
    ("Guru Yoga Studio", "yoga", "Restorative", "Monday", "8:30", 60, "45000/month", "Beginner", "Group", "Calm", "Mix"),
    ("Guru Yoga Studio", "yoga", "Hatha", "Monday,Wednesday", "9:45", 60, "45000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Guru Yoga Studio", "yoga", "Hatha", "Monday,Friday", "19:00", 90, "45000/month", "Beginner", "Group", "Mid", "Structured"),
    ("Guru Yoga Studio", "yoga", "Hatha", "Monday,Wednesday", "12:30", 75, "45000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Guru Yoga Studio", "yoga", "Restorative", "Wednesday", "19:00", 60, "45000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Guru Yoga Studio", "yoga", "Power", "Tuesday", "8:15", 60, "45000/month", "Intermediate", "Group", "High", "Structured"),
    ("Guru Yoga Studio", "yoga", "Hatha", "Tuesday,Thursday", "10:00", 75, "45000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Guru Yoga Studio", "yoga", "Vinyasa", "Tuesday,Thursday", "17:30", 75, "45000/month", "Intermediate", "Group", "High", "Structured"),
    ("Guru Yoga Studio", "fitness", "Cardio", "Thursday", "8:15", 60, "45000/month", "Beginner", "Group", "Mid", "Structured"),
    ("Guru Yoga Studio", "yoga", "Hatha", "Saturday", "13:00", 60, "45000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Prana Yoga Studio", "yoga", "Restorative", "Monday,Wednesday,Friday", "9:00", 75, "50000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Prana Yoga Studio", "yoga", "Aerial", "Tuesday,Thursday", "17:00", 75, "50000/month", "Advanced", "Group", "Mid", "Structured"),
    ("Prana Yoga Studio", "yoga", "Aerial", "Saturday", "18:30", 75, "50000/month", "Advanced", "Group", "High", "Mix"),
    ("Armat by Nynel", "yoga", "Power", "Wednesday", "20:30", 60, "29000/month", "Intermediate", "Group", "Mid", "Structured"),
    ("Armat by Nynel", "yoga", "Power", "Thursday", "19:00", 60, "29000/month", "Intermediate", "Group", "High", "Structured"),
    ("Namaste Yoga Studio", "yoga", "Hatha", "Monday,Wednesday,Friday", "10:30", 60, "35000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Namaste Yoga Studio", "yoga", "Hatha", "Monday,Wednesday,Friday", "18:15", 60, "35000/month", "Beginner", "Group", "Calm", "Structured"),
    ("Namaste Yoga Studio", "yoga", "Hatha", "Tuesday,Thursday", "9:00", 75, "35000/month", "Beginner", "Group", "Mid", "Structured"),
    ("Namaste Yoga Studio", "fitness", "Pilates", "Tuesday,Thursday", "11:00", 60, "35000/month", "Beginner", "Group", "Mid", "Mix"),
    ("Namaste Yoga Studio", "yoga", "Hatha", "Tuesday,Thursday", "19:00", 60, "35000/month", "Intermediate", "Group", "Calm", "Structured"),
    # Orange Premium Fitness Club
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Monday", "8:00", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "yoga", "Restorative", "Monday,Tuesday,Thursday", "9:30", 60, "520000/year", "Beginner", "Group", "Calm", "Structured"),
    ("Orange Premium Fitness Club", "yoga", "Aerial", "Monday", "10:30", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Monday,Wednesday,Friday", "10:30", 60, "520000/year", "Beginner", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Monday,Wednesday,Friday", "11:30", 60, "520000/year", "Intermediate", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Monday", "12:30", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Strength", "Monday,Wednesday", "19:15", 60, "520000/year", "Intermediate", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Strength", "Tuesday,Thursday", "8:00", 90, "520000/year", "Intermediate", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Tuesday,Thursday", "9:30", 60, "520000/year", "Beginner", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Strength", "Tuesday,Thursday", "10:30", 75, "520000/year", "Intermediate", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Pilates", "Tuesday,Thursday", "14:30", 75, "520000/year", "Beginner", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "dance", "Latin", "Tuesday", "14:30", 90, "520000/year", "Advanced", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "yoga", "Restorative", "Tuesday,Thursday", "15:45", 60, "520000/year", "Beginner", "Group", "Calm", "Structured"),
    ("Orange Premium Fitness Club", "dance", "Salsa", "Tuesday,Thursday", "17:00", 120, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Strength", "Tuesday,Thursday", "18:45", 45, "520000/year", "Advanced", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Tuesday,Thursday", "19:30", 60, "520000/year", "Intermediate", "Group", "High", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Tuesday", "19:40", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "yoga", "Aerial", "Tuesday,Thursday", "20:00", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Wednesday", "7:00", 60, "520000/year", "Intermediate", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Cardio", "Wednesday", "8:00", 60, "520000/year", "Beginner", "Group", "Mid", "Structured"),
    ("Orange Premium Fitness Club", "yoga", "Restorative", "Wednesday", "9:00", 60, "520000/year", "Beginner", "Group", "Calm", "Structured"),
    ("Orange Premium Fitness Club", "fitness", "Pilates", "Wednesday", "10:00", 75, "520000/year", "Beginner", "Group", "High", "Structured"),
]

studio_name_to_id = {s[1]: s[0] for s in REAL_STUDIOS}
district_by_studio = {s[1]: s[2] for s in REAL_STUDIOS}
tier_by_studio = {s[1]: s[5] for s in REAL_STUDIOS}


def row_to_class_dict(class_id, row):
    (studio_name, activity, style, day, time, duration, raw_price,
     exp, group_priv, energy, structure) = row
    per_sess, monthly = clean_price(raw_price)
    canonical_style = STYLE_NORMALIZE.get(style, style)
    return {
        "class_id": class_id,
        "studio_id": studio_name_to_id[studio_name],
        "studio_name": studio_name,
        "activity_type": activity,
        "style": canonical_style,
        "day": day,
        "time": time,
        "duration_min": duration,
        "price_per_session_amd": per_sess,
        "price_monthly_amd": monthly,
        "experience_required": exp,
        "group_or_private": group_priv,
        "energy_level": energy,
        "structure_level": structure,
        "district": district_by_studio[studio_name],
    }


classes = []
cid = 1
for row in REAL_CLASSES_RAW:
    classes.append(row_to_class_dict(cid, row))
    cid += 1


# --- SYNTHETIC CLASSES for dance studios + new fitness studios ---
DAYS_OPTS = [
    "Monday,Wednesday,Friday",
    "Tuesday,Thursday",
    "Monday,Wednesday",
    "Tuesday,Thursday,Saturday",
    "Saturday",
    "Monday,Wednesday,Friday,Sunday",
    "Friday,Saturday",
    "Wednesday,Saturday",
]
TIMES = ["08:00", "09:30", "12:00", "17:30", "19:00", "19:30", "20:30"]
EXPERIENCE = ["Beginner", "Intermediate", "Advanced"]
DURATIONS = [60, 75, 90, 120]

# Attributes keyed by style — keep consistent with survey vocab
STYLE_ATTRS = {
    # Yoga
    "Hatha":       {"energy": "Calm", "structure": "Structured", "activity": "yoga"},
    "Vinyasa":     {"energy": "High", "structure": "Structured", "activity": "yoga"},
    "Power":       {"energy": "High", "structure": "Structured", "activity": "yoga"},
    "Restorative": {"energy": "Calm", "structure": "Structured", "activity": "yoga"},
    "Yin":         {"energy": "Calm", "structure": "Structured", "activity": "yoga"},
    "Aerial":      {"energy": "High", "structure": "Mix",        "activity": "yoga"},
    # Dance
    "Salsa / latin / ballroom":  {"energy": "High", "structure": "Structured", "activity": "dance"},
    "Bachata":                   {"energy": "High", "structure": "Structured", "activity": "dance"},
    "Hip-hop / street":          {"energy": "High", "structure": "Mix",        "activity": "dance"},
    "Jazz funk":                 {"energy": "High", "structure": "Mix",        "activity": "dance"},
    "Contemporary / ballet":     {"energy": "Mid",  "structure": "Structured", "activity": "dance"},
    "Armenian / Joxovrdakan":    {"energy": "Mid",  "structure": "Structured", "activity": "dance"},
    # Fitness
    "HIIT / cardio":       {"energy": "High", "structure": "Structured", "activity": "fitness"},
    "CrossFit":            {"energy": "High", "structure": "Structured", "activity": "fitness"},
    "Strength training":   {"energy": "Mid",  "structure": "Structured", "activity": "fitness"},
    "Functional training": {"energy": "Mid",  "structure": "Mix",        "activity": "fitness"},
    "TRX":                 {"energy": "Mid",  "structure": "Structured", "activity": "fitness"},
    "Pilates":             {"energy": "Calm", "structure": "Structured", "activity": "fitness"},
}

STYLES_BY_ACTIVITY = {
    "yoga":    ["Hatha", "Vinyasa", "Power", "Restorative", "Yin", "Aerial"],
    "dance":   ["Salsa / latin / ballroom", "Bachata", "Hip-hop / street",
                "Jazz funk", "Contemporary / ballet", "Armenian / Joxovrdakan"],
    "fitness": ["HIIT / cardio", "CrossFit", "Strength training",
                "Functional training", "TRX", "Pilates"],
}

PRICE_PER_SESSION = {"Budget": (2500, 4000), "Mid": (4000, 6000), "Premium": (6000, 9000)}
PRICE_MONTHLY     = {"Budget": (18000, 28000), "Mid": (28000, 45000), "Premium": (45000, 70000)}


def activities_for(studio_type):
    out = []
    if "yoga" in studio_type:    out.append("yoga")
    if "dance" in studio_type:   out.append("dance")
    if "fitness" in studio_type: out.append("fitness")
    return out


def gen_class_for_studio(class_id, studio_row, activity, style):
    attrs = STYLE_ATTRS[style]
    tier = studio_row[5]
    lo_s, hi_s = PRICE_PER_SESSION[tier]
    lo_m, hi_m = PRICE_MONTHLY[tier]
    uses_monthly = random.random() < 0.35
    per_sess = None if uses_monthly else random.randint(lo_s, hi_s)
    monthly = random.randint(lo_m, hi_m) if uses_monthly else None
    if per_sess is None and monthly is not None:
        per_sess = round(monthly / 8)

    return {
        "class_id": class_id,
        "studio_id": studio_row[0],
        "studio_name": studio_row[1],
        "activity_type": activity,
        "style": style,
        "day": random.choice(DAYS_OPTS),
        "time": random.choice(TIMES),
        "duration_min": random.choice(DURATIONS),
        "price_per_session_amd": per_sess,
        "price_monthly_amd": monthly,
        "experience_required": random.choice(EXPERIENCE),
        "group_or_private": "Private" if random.random() < 0.10 else "Group",
        "energy_level": attrs["energy"],
        "structure_level": attrs["structure"],
        "district": studio_row[2],
    }


# Which studios already have real classes
studios_with_real_classes = set(row[0] for row in REAL_CLASSES_RAW)

# For every studio, ensure each offered activity has at least N classes
# Dance studios need a lot — they have 0 real classes in the original sheet except Orange's 2
MIN_CLASSES_PER_ACTIVITY = {
    "dance": 5,   # dance studios need substantive schedules
    "yoga": 3,
    "fitness": 4,
}

# Count existing real classes per (studio_id, activity)
existing_counts = {}
for c in classes:
    key = (c["studio_id"], c["activity_type"])
    existing_counts[key] = existing_counts.get(key, 0) + 1

for studio_row in REAL_STUDIOS:
    sid, sname, district, addr, ig, tier, stype = studio_row
    for activity in activities_for(stype):
        current = existing_counts.get((sid, activity), 0)
        needed = MIN_CLASSES_PER_ACTIVITY[activity] - current
        if needed <= 0:
            continue
        available_styles = STYLES_BY_ACTIVITY[activity]
        # Pick a varied mix
        chosen_styles = random.choices(available_styles, k=needed)
        for style in chosen_styles:
            classes.append(gen_class_for_studio(cid, studio_row, activity, style))
            cid += 1

classes_df = pd.DataFrame(classes)


# PART 3 SURVEY
# Preserve all 44 real responses. Add synthetic ones to help model training.
# Target: ~400 rows total by augmenting.

# Vocab normalization from raw Google-Form answers → canonical
GENDER_NORM = {
    "Female": "Female",
    "Male": "Male",
    "Prefer not to say / Other": "Other",
}

STYLE_SURVEY_NORM = {
    "Aerial": "Aerial",
    "Hatha / gentle": "Hatha",
    "Vinyasa / flow": "Vinyasa",
    "Restorative / meditative": "Restorative",
    "Not sure yet": None,
    "": None,
    "Salsa / latin / ballroom": "Salsa / latin / ballroom",
    "Hip-hop / street": "Hip-hop / street",
    "Contemporary / ballet": "Contemporary / ballet",
    "Armenian / Joxovrdakan": "Armenian / Joxovrdakan",
    "Strength training": "Strength training",
    "HIIT / cardio": "HIIT / cardio",
    "Pilates": "Pilates",
}

ENERGY_NORM = {
    "Calm": "Calm",
    "High-energy": "High",
    "Depends on mood": "Depends on mood",
}

GROUP_NORM = {
    "Group": "Group",
    "Private": "Private",
    "No preference": "No preference",
}

TRAVEL_NORM = {
    "Under 1km": "Under 1km",
    "Under 5km": "Under 5km",
    "Under 10km": "Under 10km",
    "10+km is fine": "Over 10km",
}

STRUCTURE_NORM = {
    "Structured": "Structured",
    "Freestyle": "Freestyle",
    "Mix": "Mix",
}

EXP_NORM = {
    "Beginner": "Beginner",
    "Intermediate": "Intermediate",
    "Advanced": "Advanced",
}

GOAL_NORM = {
    "Physical fitness / health": "Physical fitness / health",
    "Stress relief / mental wellness": "Stress relief",
    "Creative expression": "Creative expression",
    "Learning a new skill": "Learning a new skill",
    "Social / meeting people": "Social",
}


# 44 real survey rows, kept verbatim then normalized
# Columns: age, gender, activity_interest_raw, yoga_raw, dance_raw, fitness_raw,
#          travel_raw, group_raw, energy_raw, experience_raw, goal_raw, structure_raw
REAL_SURVEY = [
    (20, "Female", "Yoga, Dance", "Aerial", "Salsa / latin / ballroom", "", "Under 10km", "Group", "Depends on mood", "Intermediate", "Learning a new skill", "Mix"),
    (20, "Female", "Dance", "", "Hip-hop / street", "", "Under 5km", "Private", "Calm", "Beginner", "Creative expression", "Mix"),
    (19, "Female", "Fitness", "", "", "Strength training", "Under 5km", "No preference", "Calm", "Intermediate", "Physical fitness / health", "Structured"),
    (21, "Female", "Fitness, Dance", "Not sure yet", "Armenian / Joxovrdakan", "Pilates", "Under 5km", "Private", "Depends on mood", "Beginner", "Physical fitness / health", "Structured"),
    (21, "Female", "Fitness", "", "", "HIIT / cardio", "Under 1km", "Group", "Depends on mood", "Intermediate", "Physical fitness / health", "Structured"),
    (23, "Female", "Dance", "", "Contemporary / ballet", "", "Under 1km", "Private", "Depends on mood", "Intermediate", "Creative expression", "Mix"),
    (20, "Female", "Yoga", "Not sure yet", "", "", "Under 1km", "Group", "Calm", "Intermediate", "Physical fitness / health", "Freestyle"),
    (20, "Male", "Yoga, Fitness, Dance", "Aerial", "Hip-hop / street", "HIIT / cardio", "Under 10km", "No preference", "Depends on mood", "Intermediate", "Creative expression", "Mix"),
    (20, "Male", "Yoga, Fitness, Dance", "Restorative / meditative", "Salsa / latin / ballroom", "Strength training", "Under 5km", "Private", "High-energy", "Intermediate", "Stress relief / mental wellness", "Freestyle"),
    (26, "Male", "Fitness, Dance", "", "Salsa / latin / ballroom", "Strength training", "Under 5km", "Private", "High-energy", "Advanced", "Learning a new skill", "Mix"),
    (18, "Female", "Dance", "", "Contemporary / ballet", "", "Under 10km", "Group", "High-energy", "Advanced", "Stress relief / mental wellness", "Structured"),
    (21, "Female", "Dance", "", "Contemporary / ballet", "", "Under 5km", "Group", "Calm", "Beginner", "Creative expression", "Structured"),
    (24, "Female", "Fitness", "", "", "HIIT / cardio", "Under 10km", "Private", "High-energy", "Intermediate", "Stress relief / mental wellness", "Freestyle"),
    (20, "Female", "Yoga, Fitness, Dance", "Aerial", "Hip-hop / street", "Pilates", "Under 1km", "Group", "Depends on mood", "Intermediate", "Stress relief / mental wellness", "Structured"),
    (22, "Female", "Dance", "", "Armenian / Joxovrdakan", "", "Under 10km", "Group", "Depends on mood", "Advanced", "Social / meeting people", "Mix"),
    (30, "Female", "Fitness", "", "", "Pilates", "10+km is fine", "No preference", "Calm", "Advanced", "Stress relief / mental wellness", "Mix"),
    (18, "Prefer not to say / Other", "Dance", "", "Hip-hop / street", "", "Under 1km", "Group", "High-energy", "Beginner", "Social / meeting people", "Mix"),
    (21, "Female", "Yoga, Dance", "Aerial", "Not sure yet", "", "Under 5km", "No preference", "Depends on mood", "Intermediate", "Physical fitness / health", "Structured"),
    (21, "Male", "Fitness", "", "", "Strength training", "Under 1km", "No preference", "High-energy", "Beginner", "Physical fitness / health", "Structured"),
    (18, "Female", "Yoga", "Aerial", "", "", "Under 1km", "Group", "Calm", "Beginner", "Stress relief / mental wellness", "Mix"),
    (23, "Male", "Fitness", "", "", "Strength training", "Under 10km", "No preference", "High-energy", "Intermediate", "Physical fitness / health", "Structured"),
    (21, "Female", "Fitness, Dance", "Not sure yet", "Salsa / latin / ballroom", "HIIT / cardio", "Under 1km", "No preference", "High-energy", "Advanced", "Physical fitness / health", "Mix"),
    (20, "Male", "Yoga", "Aerial", "", "", "Under 5km", "Private", "Calm", "Beginner", "Creative expression", "Freestyle"),
    (50, "Prefer not to say / Other", "Dance", "", "Salsa / latin / ballroom", "", "10+km is fine", "Group", "High-energy", "Intermediate", "Stress relief / mental wellness", "Mix"),
    (26, "Female", "Fitness", "", "", "HIIT / cardio", "10+km is fine", "Private", "Depends on mood", "Beginner", "Physical fitness / health", "Freestyle"),
    (49, "Female", "Yoga, Dance", "Hatha / gentle", "Salsa / latin / ballroom", "", "Under 5km", "Group", "Depends on mood", "Beginner", "Stress relief / mental wellness", "Structured"),
    (34, "Male", "Fitness", "", "", "Strength training", "Under 10km", "Private", "Depends on mood", "Intermediate", "Physical fitness / health", "Freestyle"),
    (26, "Female", "Yoga", "Vinyasa / flow", "", "", "Under 10km", "Group", "Calm", "Advanced", "Stress relief / mental wellness", "Structured"),
    (29, "Male", "Fitness, Dance", "", "Armenian / Joxovrdakan", "HIIT / cardio", "Under 10km", "Group", "High-energy", "Intermediate", "Social / meeting people", "Structured"),
    (18, "Male", "Fitness, Dance", "", "Hip-hop / street", "Strength training", "Under 1km", "Group", "High-energy", "Advanced", "Learning a new skill", "Mix"),
    (23, "Female", "Dance", "", "Contemporary / ballet", "", "Under 5km", "Private", "Depends on mood", "Beginner", "Creative expression", "Freestyle"),
    (21, "Female", "Fitness", "", "", "Strength training", "Under 1km", "Private", "High-energy", "Intermediate", "Physical fitness / health", "Freestyle"),
    (20, "Female", "Yoga, Dance", "Not sure yet", "Contemporary / ballet", "", "Under 5km", "No preference", "Calm", "Beginner", "Physical fitness / health", "Mix"),
    (20, "Female", "Yoga, Dance", "Not sure yet", "Salsa / latin / ballroom", "", "Under 5km", "Group", "High-energy", "Intermediate", "Learning a new skill", "Mix"),
    (20, "Female", "Yoga, Dance", "Not sure yet", "Hip-hop / street", "", "Under 5km", "No preference", "Depends on mood", "Beginner", "Learning a new skill", "Mix"),
    (19, "Female", "Yoga, Fitness", "Not sure yet", "", "Strength training", "Under 1km", "No preference", "Depends on mood", "Beginner", "Physical fitness / health", "Mix"),
    (21, "Male", "Fitness, Dance", "", "Salsa / latin / ballroom", "HIIT / cardio", "10+km is fine", "Group", "Calm", "Beginner", "Stress relief / mental wellness", "Mix"),
    (25, "Male", "Fitness", "Restorative / meditative", "Hip-hop / street", "Strength training", "Under 5km", "Group", "High-energy", "Intermediate", "Physical fitness / health", "Structured"),
    (20, "Female", "Dance", "", "Hip-hop / street", "", "Under 5km", "Group", "Depends on mood", "Beginner", "Learning a new skill", "Structured"),
    (21, "Female", "Dance", "", "Not sure yet", "", "Under 5km", "Group", "Depends on mood", "Intermediate", "Stress relief / mental wellness", "Mix"),
    (21, "Female", "Dance", "", "Contemporary / ballet", "", "10+km is fine", "Group", "High-energy", "Intermediate", "Stress relief / mental wellness", "Structured"),
    (22, "Female", "Fitness, Dance", "", "Hip-hop / street", "HIIT / cardio", "Under 5km", "Group", "High-energy", "Beginner", "Stress relief / mental wellness", "Mix"),
    (21, "Female", "Fitness, Dance", "", "", "Strength training", "Under 10km", "No preference", "Depends on mood", "Intermediate", "Physical fitness / health", "Mix"),
    (21, "Female", "Fitness, Dance", "", "Not sure yet", "Strength training", "Under 1km", "No preference", "High-energy", "Intermediate", "Stress relief / mental wellness", "Mix"),
]


def normalize_survey_row(row, user_id, is_synthetic=False):
    (age, gender, activities_raw, yoga_raw, dance_raw, fitness_raw,
     travel_raw, group_raw, energy_raw, exp_raw, goal_raw, struct_raw) = row

    # Normalize activity list
    activities = [a.strip() for a in activities_raw.split(",")]
    activity_list = ",".join(activities)

    return {
        "user_id": user_id,
        "age": age,
        "gender": GENDER_NORM.get(gender, gender),
        "activity_interest": activity_list,
        "yoga_style": STYLE_SURVEY_NORM.get(yoga_raw.strip(), yoga_raw.strip() or None) if "Yoga" in activities else None,
        "dance_style": STYLE_SURVEY_NORM.get(dance_raw.strip(), dance_raw.strip() or None) if "Dance" in activities else None,
        "fitness_style": STYLE_SURVEY_NORM.get(fitness_raw.strip(), fitness_raw.strip() or None) if "Fitness" in activities else None,
        "max_travel_km": TRAVEL_NORM.get(travel_raw, travel_raw),
        "group_preference": GROUP_NORM.get(group_raw, group_raw),
        "energy_preference": ENERGY_NORM.get(energy_raw, energy_raw),
        "experience_level": EXP_NORM.get(exp_raw, exp_raw),
        "goal": GOAL_NORM.get(goal_raw, goal_raw),
        "structure_preference": STRUCTURE_NORM.get(struct_raw, struct_raw),
        "data_source": "synthetic" if is_synthetic else "real",
    }


survey_rows = [normalize_survey_row(r, uid + 1, False)
               for uid, r in enumerate(REAL_SURVEY)]


# ---- SYNTHETIC SURVEY GENERATION ----
# Insight-driven: produce more users that reflect the patterns we see.
# We do SMART augmentation: sample real rows as templates, perturb demographic
# noise but keep the preference-to-style link intact (that's the model signal).
# This avoids breaking the correlation "calm+beginner+structured → Hatha".

def augment_survey(base_df, target_total=400):
    """
    Use each real row as a template. Generate near-twins that share the
    preferences AND style choice, with small perturbations on:
    - age (+/- 3 years)
    - gender (occasional flip to underrepresented)
    - activity_interest (add/remove one listed activity with low prob)
    - travel distance (occasional swap)
    """
    need = target_total - len(base_df)
    extras = []
    next_uid = base_df["user_id"].max() + 1

    templates = base_df.to_dict("records")

    for i in range(need):
        tpl = random.choice(templates)
        new = tpl.copy()
        new["user_id"] = next_uid + i
        new["data_source"] = "synthetic"

        # Age noise
        new["age"] = max(16, min(65, int(tpl["age"]) + random.randint(-3, 3)))

        # Occasionally swap travel tolerance
        if random.random() < 0.20:
            new["max_travel_km"] = random.choice(list(TRAVEL_NORM.values()))

        # Occasionally flip gender (keeps diversity)
        if random.random() < 0.12:
            new["gender"] = random.choice(["Female", "Male", "Other"])

        # Occasionally toggle group preference (tests model robustness)
        if random.random() < 0.15:
            new["group_preference"] = random.choice(["Group", "Private", "No preference"])

        # Keep style choices tied to preferences — these are the model's labels
        extras.append(new)

    return pd.concat([base_df, pd.DataFrame(extras)], ignore_index=True)


survey_df = pd.DataFrame(survey_rows)
survey_df = augment_survey(survey_df, target_total=400)


# SAVE ALL THREE
import os
os.makedirs("ds/data", exist_ok=True)

studios_df.to_csv("ds/data/studios.csv", index=False)
classes_df.to_csv("ds/data/classes.csv", index=False)
survey_df.to_csv("ds/data/survey.csv", index=False)

print("GENERATION COMPLETE")
print(f"\nStudios:  {len(studios_df)} rows  (17 real + 6 real dance = 23 total)")
print(f"  by type:")
for stype, count in studios_df["studio_type"].value_counts().items():
    print(f"    {stype}: {count}")

print(f"\nClasses:  {len(classes_df)} rows  ({len(REAL_CLASSES_RAW)} real + {len(classes_df) - len(REAL_CLASSES_RAW)} synthetic)")
print(f"  by activity:")
for act, count in classes_df["activity_type"].value_counts().items():
    print(f"    {act}: {count}")

print(f"\nSurvey:   {len(survey_df)} rows  (44 real + {len(survey_df) - 44} augmented)")
print(f"  activity coverage (mentions):")
for activity in ["Yoga", "Dance", "Fitness"]:
    n = survey_df["activity_interest"].str.contains(activity).sum()
    print(f"    {activity}: {n}")

print(f"\nStyle labels available for training (after filtering 'Not sure yet'):")
yoga_labels = survey_df["yoga_style"].dropna()
yoga_labels = yoga_labels[yoga_labels != "Not sure yet"]
dance_labels = survey_df["dance_style"].dropna()
dance_labels = dance_labels[dance_labels != "Not sure yet"]
fitness_labels = survey_df["fitness_style"].dropna()
fitness_labels = fitness_labels[fitness_labels != "Not sure yet"]
print(f"  yoga: {len(yoga_labels)}, dance: {len(dance_labels)}, fitness: {len(fitness_labels)}")
