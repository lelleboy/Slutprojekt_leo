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
DOT_COLOR = "#EF4444"      # Changed to red for logged activities
TEXT_SECONDARY = "#9CA3AF"

WIDTH = 360
HEIGHT = 500

app = ctk.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.title("Fitness App")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

# Stores the active user session
session = {"username": None}

# =====================================================
# ACTIVITIES & MET VALUES
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
# LOGIC & HELPERS
# =====================================================

# Clears the main window components
def clear():
    for w in main_frame.winfo_children():
        w.destroy()

# Gets the filename for the current user
def get_file():
    return f"{session['username']}.json" if session.get("username") else None

# Loads user data from JSON file
def load_user():
    file = get_file()
    default_user = {"username": session.get("username"), "gender": "male", "age": 30, "height": 170, "weight": 70, "workouts": [], "weight_history": []}
    if not file or not os.path.exists(file):
        return default_user
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "workouts" not in data: data["workouts"] = []
            if "weight_history" not in data: data["weight_history"] = []
            return data
    except:
        return default_user

# Saves user data to JSON file
def save_user(data):
    file = get_file()
    if file:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

# Calculates burned calories based on BMR and MET
def calculate_calories(activity, intensity, minutes):
    user = load_user()
    try:
        weight, age, height, gender = float(user.get("weight", 70)), int(user.get("age", 30)), float(user.get("height", 170)), user.get("gender", "male")
        act = next((a for a in ACTIVITIES if a["activity"].lower() == activity.lower()), None)
        met = act["met"].get(intensity, 5.0) if act else 5.0
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age) if gender == "male" else 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
        return round((bmr / 1440) * met * float(minutes), 1)
    except: return 0

# Gets a list of all existing user profiles
def get_existing_users():
    files = glob.glob("*.json")
    return [os.path.splitext(f)[0] for f in files]

# Logs out the current user and returns to start
def logout():
    session["username"] = None
    start_page()

# Closes the application completely
def exit_app():
    app.quit()

# Displays a popup window with workout details
def show_workout_details(workout):
    detail_window = ctk.CTkToplevel(app)
    detail_window.title("Workout Details")
    detail_window.geometry("300x350")
    detail_window.configure(fg_color=BG_COLOR)
    detail_window.resizable(False, False)
    detail_window.transient(app)
    detail_window.grab_set()
    
    ctk.CTkLabel(detail_window, text=workout['activity'], font=("Arial", 24, "bold"), text_color=ACCENT_COLOR).pack(pady=(20, 10))
    
    card = ctk.CTkFrame(detail_window, fg_color=CARD_COLOR, corner_radius=12)
    card.pack(fill="both", expand=True, padx=20, pady=10)
    
    details = [
        ("📅 Date:", workout['date']),
        ("⏱️ Duration:", f"{workout['time_in_min']} min"),
        ("🔥 Calories:", f"{workout.get('calories', 0)} kcal"),
        ("💪 Intensity:", workout.get('intensity', 'medium').capitalize())
    ]
    
    for label, val in details:
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(row, text=label, font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY).pack(side="left")
        ctk.CTkLabel(row, text=val, font=("Arial", 12)).pack(side="right")
        
    ctk.CTkLabel(card, text="💬 Comment:", font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(10, 2))
    
    comment_text = workout.get('comment', '').strip() or "No comment added."
    comment_box = ctk.CTkTextbox(card, font=("Arial", 12), fg_color=BG_COLOR, border_width=0, corner_radius=8, height=70)
    comment_box.pack(fill="x", padx=15, pady=(0, 15))
    comment_box.insert("1.0", comment_text)
    comment_box.configure(state="disabled")
    
    ctk.CTkButton(detail_window, text="Close", fg_color=CARD_COLOR, hover_color="#374151", command=detail_window.destroy).pack(pady=(0, 15), padx=20, fill="x")

# =====================================================
# UI COMPONENTS
# =====================================================

main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
main_frame.pack(fill="both", expand=True)

# Generates the bottom navigation bar
def navbar():
    nav = ctk.CTkFrame(main_frame, height=65, fg_color="#111827", corner_radius=0)
    nav.pack(side="bottom", fill="x")
    
    buttons = [
        ("🏠", "Home", dashboard), 
        ("➕", "New", add_workout), 
        ("📅", "Calendar", calendar_page), 
        ("👤", "History", history_page),
        ("⚖️", "Weight", weight_page), 
        ("🚪", "Out", logout),
        ("❌", "Exit", exit_app)
    ]
    
    for icon, text_under, cmd in buttons:
        btn_container = ctk.CTkFrame(nav, fg_color="transparent", corner_radius=6, cursor="hand2")
        btn_container.pack(side="left", expand=True, pady=4, padx=1)
        
        lbl_icon = ctk.CTkLabel(btn_container, text=icon, font=("Arial", 16), text_color="white")
        lbl_icon.pack(pady=(4, 0))
        
        lbl_text = ctk.CTkLabel(btn_container, text=text_under, font=("Arial", 9), text_color=TEXT_SECONDARY)
        lbl_text.pack(pady=(0, 4), padx=4)
        
        btn_container.bind("<Button-1>", lambda e, c=cmd: c())
        lbl_icon.bind("<Button-1>", lambda e, c=cmd: c())
        lbl_text.bind("<Button-1>", lambda e, c=cmd: c())
        
        btn_container.bind("<Enter>", lambda e, b=btn_container: b.configure(fg_color=CARD_COLOR))
        btn_container.bind("<Leave>", lambda e, b=btn_container: b.configure(fg_color="transparent"))

# Standardized information card
def create_card(parent, title):
    card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)
    card.pack(fill="x", padx=15, pady=5)
    label = ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color=TEXT_SECONDARY)
    label.pack(anchor="w", padx=12, pady=(8, 2))
    return card

# =====================================================
# PAGES / VIEWS
# =====================================================

# Main landing screen
def start_page():
    clear()
    ctk.CTkLabel(main_frame, text="FITNESS", font=("Impact", 42), text_color=ACCENT_COLOR).pack(pady=(60, 20))
    ctk.CTkButton(main_frame, text="Login", fg_color=ACCENT_COLOR, command=login_page).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Create Account", fg_color=CARD_COLOR, command=register_page).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Exit App", fg_color="transparent", text_color=TEXT_SECONDARY, font=("Arial", 11), command=exit_app).pack(pady=10)

# Profile selection / login screen
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

# Dashboard overview screen
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

# Screen to log a new workout activity
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
    
    comment_entry = ctk.CTkEntry(container, placeholder_text="Comment (optional)", height=35, fg_color=CARD_COLOR, border_width=0)
    comment_entry.pack(fill="x", pady=5)
    
    def save():
        try:
            m = float(mins_entry.get()); user = load_user()
            user["workouts"].append({
                "activity": act_var.get(), "intensity": int_var.get(), "time_in_min": m,
                "calories": calculate_calories(act_var.get(), int_var.get(), m),
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "comment": comment_entry.get().strip()
            })
            save_user(user); dashboard()
        except: pass
    ctk.CTkButton(main_frame, text="Save", fg_color=ACCENT_COLOR, height=40, command=save).pack(pady=15, padx=30, fill="x")
    navbar()

# Calendar layout tracking logged workouts
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
            cal.calevent_create(d, ".", "workout_event")
        except: continue
    
    # Highlights logged workout dates in RED (DOT_COLOR)
    cal.tag_config("workout_event", foreground=DOT_COLOR, font=("Arial", 14, "bold"))
    
    ctk.CTkLabel(main_frame, text="● = Activity logged", text_color=DOT_COLOR, font=("Arial", 11)).pack(pady=5)
    navbar()

# Interactive clickable workout list screen
def history_page():
    clear()
    ctk.CTkLabel(main_frame, text="History", font=("Arial", 18, "bold")).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=280)
    scroll.pack(fill="both", expand=True, padx=10)
    user = load_user()
    for w in reversed(user.get("workouts", [])):
        item = ctk.CTkFrame(scroll, fg_color=CARD_COLOR, height=50, cursor="hand2")
        item.pack(fill="x", pady=3)
        
        lbl_info = ctk.CTkLabel(item, text=f"{w['date']} - {w['activity']}", font=("Arial", 11, "bold"))
        lbl_info.place(x=10, y=12)
        
        lbl_cal = ctk.CTkLabel(item, text=f"+{w.get('calories', 0)} kcal", text_color="#10B981", font=("Arial", 12, "bold"))
        lbl_cal.place(x=200, y=12)
        
        item.bind("<Button-1>", lambda e, workout=w: show_workout_details(workout))
        lbl_info.bind("<Button-1>", lambda e, workout=w: show_workout_details(workout))
        lbl_cal.bind("<Button-1>", lambda e, workout=w: show_workout_details(workout))
        
        item.bind("<Enter>", lambda e, i=item: i.configure(fg_color="#374151"))
        item.bind("<Leave>", lambda e, i=item: i.configure(fg_color=CARD_COLOR))
        
    navbar()

# Weight logger & customized canvas line graph screen
def weight_page():
    clear()
    user = load_user()
    
    ctk.CTkLabel(main_frame, text="Weight Tracker", font=("Arial", 18, "bold")).pack(pady=10)
    
    input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=30, pady=5)
    
    w_entry = ctk.CTkEntry(input_frame, placeholder_text="Weight (kg)", height=35, fg_color=CARD_COLOR, border_width=0)
    w_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    def save_weight():
        try:
            w_val = float(w_entry.get())
            user["weight"] = w_val  # Updates core user weight metadata
            user["weight_history"].append({
                "date": datetime.datetime.now().strftime("%m-%d"),
                "weight": w_val
            })
            save_user(user)
            weight_page()  # Refreshes the view to load the newly updated graph lines
        except: pass
        
    ctk.CTkButton(input_frame, text="Log", fg_color=ACCENT_COLOR, width=70, height=35, command=save_weight).pack(side="right")
    
    history = user.get("weight_history", [])
    if len(history) >= 2:
        # Generates the manual line graph onto a clean Tkinter Canvas box
        canvas = ctk.CTkCanvas(main_frame, width=300, height=180, bg=CARD_COLOR, highlightthickness=0)
        canvas.pack(pady=15)
        
        weights = [h["weight"] for h in history[-6:]] # Captures up to the 6 most recent logs
        labels = [h["date"] for h in history[-6:]]
        max_w, min_w = max(weights) + 2, min(weights) - 2
        if max_w == min_w: max_w += 1
        
        graph_w, graph_h = 260, 130
        points = []
        for i, w in enumerate(weights):
            x = 30 + (i * (graph_w / (len(weights) - 1)))
            y = 140 - ((w - min_w) / (max_w - min_w) * graph_h)
            points.append((x, y))
            canvas.create_oval(x-3, y-3, x+3, y+3, fill=ACCENT_COLOR, outline="")
            canvas.create_text(x, y-12, text=f"{w}", fill="white", font=("Arial", 8))
            canvas.create_text(x, 160, text=labels[i], fill=TEXT_SECONDARY, font=("Arial", 8))
            
        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill=ACCENT_COLOR, width=2)
    else:
        ctk.CTkLabel(main_frame, text="Log at least 2 weight entries\nto generate progress graph.", font=("Arial", 12, "italic"), text_color=TEXT_SECONDARY).pack(pady=40)
        
    navbar()

# Profile creation / account registration screen
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
                        "height": float(fields["Height"].get() or 170), "weight": float(fields["Weight"].get() or 70), "workouts": [], "weight_history": []}
                save_user(data); dashboard()
        except: pass
    ctk.CTkButton(main_frame, text="Create", fg_color=ACCENT_COLOR, height=40, command=do_reg).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Back", fg_color="transparent", text_color=TEXT_SECONDARY, font=("Arial", 11), command=start_page).pack()

# Launches application loop and renders first screen
start_page()
app.mainloop()