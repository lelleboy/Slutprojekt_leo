import customtkinter as ctk
from tkcalendar import Calendar
import json
import datetime
import os
import glob

# =====================================================
# SETTINGS & THEME
# =====================================================

ctk.set_appearance_mode("dark")
BG_COLOR = "#0B1120"      
CARD_COLOR = "#1F2937"    
ACCENT_COLOR = "#3B82F6"  
DOT_COLOR = "#FFD700"     # Gul färg för pricken
TEXT_SECONDARY = "#9CA3AF"

WIDTH = 360
HEIGHT = 500

app = ctk.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.title("Fitness App")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

session = {"username": None}

# =====================================================
# ACTIVITIES
# =====================================================
ACTIVITIES = [
    {"activity": "Running",         "met": {"low": 6.0,  "medium": 8.3,  "high": 12.0}},
    {"activity": "Cycling",         "met": {"low": 4.0,  "medium": 7.0,  "high": 10.5}},
    {"activity": "Swimming",        "met": {"low": 5.0,  "medium": 7.0,  "high": 10.0}},
    {"activity": "Walking",         "met": {"low": 2.5,  "medium": 3.5,  "high": 4.5}},
    {"activity": "Weights",         "met": {"low": 3.0,  "medium": 5.0,  "high": 7.0}},
    {"activity": "Yoga",            "met": {"low": 2.0,  "medium": 3.0,  "high": 4.0}},
    {"activity": "Boxing",          "met": {"low": 5.5,  "medium": 8.0,  "high": 12.0}},
    {"activity": "Football",        "met": {"low": 6.0,  "medium": 8.0,  "high": 10.0}},
    {"activity": "Tennis",          "met": {"low": 5.0,  "medium": 7.3,  "high": 9.0}},
    {"activity": "HIIT",            "met": {"low": 6.0,  "medium": 8.0,  "high": 11.0}},
    {"activity": "Climbing",        "met": {"low": 5.0,  "medium": 7.5,  "high": 10.0}},
    {"activity": "Dancing",         "met": {"low": 3.0,  "medium": 5.0,  "high": 8.0}},
]

# =====================================================
# HELPERS & LOGIC
# =====================================================

def clear():
    for w in main_frame.winfo_children():
        w.destroy()

def get_file():
    return f"{session['username']}.json" if session.get("username") else None

def load_user():
    file = get_file()
    default_user = {"username": session.get("username"), "gender": "male", "age": 30, "height": 170, "weight": 70, "workouts": []}
    if not file or not os.path.exists(file):
        return default_user
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "workouts" not in data: data["workouts"] = []
            return data
    except:
        return default_user

def save_user(data):
    file = get_file()
    if file:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_calories(activity, intensity, minutes):
    user = load_user()
    try:
        weight, age, height, gender = float(user.get("weight", 70)), int(user.get("age", 30)), float(user.get("height", 170)), user.get("gender", "male")
        act = next((a for a in ACTIVITIES if a["activity"].lower() == activity.lower()), None)
        met = act["met"].get(intensity, 5.0) if act else 5.0
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age) if gender == "male" else 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
        return round((bmr / 1440) * met * float(minutes), 1)
    except: return 0

def get_existing_users():
    files = glob.glob("*.json")
    return [os.path.splitext(f)[0] for f in files]

# =====================================================
# UI COMPONENTS
# =====================================================

main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
main_frame.pack(fill="both", expand=True)

def navbar():
    nav = ctk.CTkFrame(main_frame, height=60, fg_color="#111827", corner_radius=0)
    nav.pack(side="bottom", fill="x")
    buttons = [("🏠", dashboard), ("➕", add_workout), ("📅", calendar_page), ("👤", history_page)]
    for icon, cmd in buttons:
        btn = ctk.CTkButton(nav, text=icon, width=45, height=40, fg_color="transparent", hover_color=CARD_COLOR, font=("Arial", 18), command=cmd)
        btn.pack(side="left", expand=True, pady=5)

def create_card(parent, title):
    card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)
    card.pack(fill="x", padx=15, pady=5)
    label = ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color=TEXT_SECONDARY)
    label.pack(anchor="w", padx=12, pady=(8, 2))
    return card

# =====================================================
# PAGES
# =====================================================

def start_page():
    clear()
    ctk.CTkLabel(main_frame, text="FITNESS", font=("Impact", 42), text_color=ACCENT_COLOR).pack(pady=(60, 20))
    ctk.CTkButton(main_frame, text="Login", fg_color=ACCENT_COLOR, command=login_page).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Create Account", fg_color=CARD_COLOR, command=register_page).pack(pady=10, padx=40, fill="x")

def login_page():
    clear()
    ctk.CTkLabel(main_frame, text="Login", font=("Arial", 22, "bold")).pack(pady=(20, 5))
    users = get_existing_users()
    if users:
        scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=120)
        scroll.pack(fill="x", padx=40, pady=5)
        for user_name in users:
            def select_user(name=user_name):
                session["username"] = name; dashboard()
            ctk.CTkButton(scroll, text=f"👤 {user_name.capitalize()}", fg_color=CARD_COLOR, anchor="w", height=32, command=select_user).pack(fill="x", pady=1)
    e = ctk.CTkEntry(main_frame, placeholder_text="Or enter name...", height=35, fg_color=CARD_COLOR, border_width=0)
    e.pack(padx=40, fill="x", pady=10)
    def manual_login():
        val = e.get().strip().lower(); session["username"] = val; dashboard() if val else None
    ctk.CTkButton(main_frame, text="Go", fg_color=ACCENT_COLOR, height=35, command=manual_login).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Back", fg_color="transparent", text_color=TEXT_SECONDARY, font=("Arial", 11), command=start_page).pack()

def dashboard():
    clear()
    user = load_user()
    workouts = user.get("workouts", [])
    ctk.CTkLabel(main_frame, text=f"Hello {user['username'].capitalize()}", font=("Arial", 18, "bold")).pack(pady=10)
    
    stats_card = create_card(main_frame, "Progress")
    total_cal = sum(float(w.get("calories", 0)) for w in workouts)
    total_min = sum(float(w.get("time_in_min", 0)) for w in workouts)
    ctk.CTkLabel(stats_card, text=f"{total_cal:.0f} kcal", font=("Arial", 28, "bold")).pack(anchor="w", padx=12)
    ctk.CTkLabel(stats_card, text=f"{total_min:.0f} total minutes", text_color=TEXT_SECONDARY, font=("Arial", 11)).pack(anchor="w", padx=12, pady=(0, 8))

    recent = create_card(main_frame, "Latest")
    display_workouts = workouts[-2:]
    if not display_workouts:
        ctk.CTkLabel(recent, text="No workouts yet", font=("Arial", 12, "italic")).pack(anchor="w", padx=12, pady=5)
    else:
        for w in display_workouts:
            ctk.CTkLabel(recent, text=f"• {w['activity']} ({w['time_in_min']}m)", font=("Arial", 12)).pack(anchor="w", padx=12, pady=1)
    navbar()

def add_workout():
    clear()
    ctk.CTkLabel(main_frame, text="Log Workout", font=("Arial", 18, "bold")).pack(pady=10)
    container = ctk.CTkFrame(main_frame, fg_color="transparent")
    container.pack(fill="x", padx=30)
    act_var = ctk.StringVar(value="Running")
    ctk.CTkOptionMenu(container, values=sorted([a["activity"] for a in ACTIVITIES]), variable=act_var, fg_color=CARD_COLOR, button_color=ACCENT_COLOR, height=32).pack(fill="x", pady=5)
    int_var = ctk.StringVar(value="medium")
    ctk.CTkSegmentedButton(container, values=["low", "medium", "high"], variable=int_var, selected_color=ACCENT_COLOR, height=32).pack(fill="x", pady=5)
    mins_entry = ctk.CTkEntry(container, placeholder_text="Minutes", height=35, fg_color=CARD_COLOR, border_width=0)
    mins_entry.pack(fill="x", pady=5)
    def save():
        try:
            m = float(mins_entry.get()); user = load_user()
            user["workouts"].append({
                "activity": act_var.get(), "intensity": int_var.get(), "time_in_min": m,
                "calories": calculate_calories(act_var.get(), int_var.get(), m),
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
            save_user(user); dashboard()
        except: pass
    ctk.CTkButton(main_frame, text="Save", fg_color=ACCENT_COLOR, height=40, command=save).pack(pady=15, padx=30, fill="x")
    navbar()

def calendar_page():
    clear()
    ctk.CTkLabel(main_frame, text="Activity Calendar", font=("Arial", 18, "bold")).pack(pady=(10, 5))
    cal_container = ctk.CTkFrame(main_frame, fg_color="transparent")
    cal_container.pack(fill="x", padx=15)

    cal = Calendar(cal_container, font="Arial 9", selectmode='none', background=CARD_COLOR, foreground='white', bordercolor=BG_COLOR,
                   headersbackground=BG_COLOR, headersforeground=TEXT_SECONDARY, normalbackground=CARD_COLOR, normalforeground='white',
                   weekendbackground=CARD_COLOR, weekendforeground=ACCENT_COLOR, showweeknumbers=False)
    cal.pack(pady=5, fill="x")
    
    user = load_user()
    for w in user.get("workouts", []):
        try:
            d = datetime.datetime.strptime(w["date"], "%Y-%m-%d")
            # Skapar en liten gul prick (.) för varje träningsdag
            cal.calevent_create(d, ".", "workout_event")
        except: continue
    
    # Pricken blir gul och bakgrunden förblir mörk för att poppa ut
    cal.tag_config("workout_event", foreground=DOT_COLOR, font=("Arial", 14, "bold"))
    
    ctk.CTkLabel(main_frame, text="● = Activity logged", text_color=DOT_COLOR, font=("Arial", 11)).pack(pady=5)
    navbar()

def history_page():
    clear()
    ctk.CTkLabel(main_frame, text="History", font=("Arial", 18, "bold")).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=280)
    scroll.pack(fill="both", expand=True, padx=10)
    user = load_user()
    for w in reversed(user.get("workouts", [])):
        item = ctk.CTkFrame(scroll, fg_color=CARD_COLOR, height=50)
        item.pack(fill="x", pady=3)
        ctk.CTkLabel(item, text=f"{w['date']} - {w['activity']}", font=("Arial", 11, "bold")).place(x=10, y=5)
        ctk.CTkLabel(item, text=f"+{w.get('calories', 0)} kcal", text_color="#10B981", font=("Arial", 12, "bold")).place(x=200, y=15)
    navbar()

def register_page():
    clear(); ctk.CTkLabel(main_frame, text="New Profile", font=("Arial", 22, "bold")).pack(pady=10)
    fields = {}
    for p in ["Username", "Age", "Height", "Weight"]:
        e = ctk.CTkEntry(main_frame, placeholder_text=p, height=35, fg_color=CARD_COLOR, border_width=0)
        e.pack(padx=40, fill="x", pady=3); fields[p] = e
    gender_var = ctk.StringVar(value="male")
    ctk.CTkSegmentedButton(main_frame, values=["male", "female"], variable=gender_var, height=30).pack(pady=5)
    def do_reg():
        u = fields["Username"].get().strip().lower()
        try:
            if u:
                session["username"] = u
                data = {"username": u, "gender": gender_var.get(), "age": int(fields["Age"].get() or 30),
                        "height": float(fields["Height"].get() or 170), "weight": float(fields["Weight"].get() or 70), "workouts": []}
                save_user(data); dashboard()
        except: pass
    ctk.CTkButton(main_frame, text="Create", fg_color=ACCENT_COLOR, height=40, command=do_reg).pack(pady=10, padx=40, fill="x")

start_page()
app.mainloop()