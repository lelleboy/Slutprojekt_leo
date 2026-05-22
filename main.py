import customtkinter as ctk
from tkcalendar import Calendar
import json
import datetime
import os
import glob

ctk.set_appearance_mode("dark")
BG_COLOR = "#0B1120"      
CARD_COLOR = "#1F2937"    
ACCENT_COLOR = "#3B82F6"  
DOT_COLOR = "#EF4444"      
TEXT_SECONDARY = "#9CA3AF"
ERROR_COLOR = "#F87171"     

WIDTH = 360
HEIGHT = 500

app = ctk.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.title("Fitness App")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

def check_float(P):
    if P == "" or P == ".": 
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

def check_int(P):
    if P == "": 
        return True
    try:
        int(P)
        return True
    except ValueError:
        return False

v_float_reg = app.register(check_float)
v_int_reg = app.register(check_int)

session = {"username": None}

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

def clear():
    for w in main_frame.winfo_children():
        w.destroy()

def load_user():
    name = session["username"]
    default_user = {"username": name, "gender": "male", "age": 30, "height": 170, "weight": 70, "workouts": [], "weight_history": []}
    if not name:
        return default_user
    try:
        if not os.path.exists(f"{name}.json"):
            return default_user
        with open(f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default_user

def save_user(data):
    name = session["username"]
    if name:
        try:
            with open(f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except:
            pass

def calculate_calories(activity, intensity, minutes):
    user = load_user()
    try:
        weight = float(user.get("weight", 70))
        age = int(user.get("age", 30))
        height = float(user.get("height", 170))
        gender = user.get("gender", "male")
        
        met = 5.0
        for a in ACTIVITIES:
            if a["activity"].lower() == activity.lower():
                met = a["met"].get(intensity, 5.0)
                
        if gender == "male":
            bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        else:
            bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
            
        return round((bmr / 1440) * met * float(minutes), 1)
    except:
        return 0.0

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
        ("❌", "Exit", app.quit)
    ]
    
    for icon, text, cmd in buttons:
        btn = ctk.CTkFrame(nav, fg_color="transparent", corner_radius=6, cursor="hand2")
        btn.pack(side="left", expand=True, pady=4, padx=1)
        
        i_lbl = ctk.CTkLabel(btn, text=icon, font=("Arial", 16), text_color="white")
        i_lbl.pack(pady=(4, 0))
        t_lbl = ctk.CTkLabel(btn, text=text, font=("Arial", 9), text_color=TEXT_SECONDARY)
        t_lbl.pack(pady=(0, 4), padx=4)
        
        btn.bind("<Button-1>", lambda e, c=cmd: c())
        i_lbl.bind("<Button-1>", lambda e, c=cmd: c())
        t_lbl.bind("<Button-1>", lambda e, c=cmd: c())

def create_card(parent, title):
    card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)
    card.pack(fill="x", padx=15, pady=5)
    label = ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color=TEXT_SECONDARY)
    label.pack(anchor="w", padx=12, pady=(8, 2))
    return card

def show_workout_details(w):
    win = ctk.CTkToplevel(app)
    win.title("Workout Details")
    win.geometry("300x350")
    win.configure(fg_color=BG_COLOR)
    win.resizable(False, False)
    win.transient(app)
    win.grab_set()
    
    ctk.CTkLabel(win, text=str(w.get('activity', 'Workout')), font=("Arial", 24, "bold"), text_color=ACCENT_COLOR).pack(pady=(20, 10))
    card = ctk.CTkFrame(win, fg_color=CARD_COLOR, corner_radius=12)
    card.pack(fill="both", expand=True, padx=20, pady=10)
    
    details = [
        ("📅 Date:", str(w.get('date', 'N/A'))),
        ("⏱️ Duration:", f"{w.get('time_in_min', 0)} min"),
        ("🔥 Calories:", f"{w.get('calories', 0)} kcal"),
        ("💪 Intensity:", str(w.get('intensity', 'medium')).capitalize())
    ]
    for lbl, val in details:
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(row, text=lbl, font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY).pack(side="left")
        ctk.CTkLabel(row, text=val, font=("Arial", 12)).pack(side="right")
        
    ctk.CTkLabel(card, text="💬 Comment:", font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(10, 2))
    txt = ctk.CTkTextbox(card, font=("Arial", 12), fg_color=BG_COLOR, corner_radius=8, height=70)
    txt.pack(fill="x", padx=15, pady=(0, 15))
    txt.insert("1.0", str(w.get('comment', 'No comment added.')))
    txt.configure(state="disabled")
    ctk.CTkButton(win, text="Close", fg_color=CARD_COLOR, command=win.destroy).pack(pady=(0, 15), padx=20, fill="x")

def start_page():
    clear()
    ctk.CTkLabel(main_frame, text="FITNESS", font=("Impact", 42), text_color=ACCENT_COLOR).pack(pady=(60, 20))
    ctk.CTkButton(main_frame, text="Login", fg_color=ACCENT_COLOR, command=login_page).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Create Account", fg_color=CARD_COLOR, command=register_page).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Exit App", fg_color="transparent", text_color=TEXT_SECONDARY, command=app.quit).pack(pady=10)

def login_page():
    clear()
    ctk.CTkLabel(main_frame, text="Login", font=("Arial", 22, "bold")).pack(pady=(20, 5))
    err = ctk.CTkLabel(main_frame, text="", text_color=ERROR_COLOR, font=("Arial", 11, "bold"))
    err.pack(pady=2)
    
    files = glob.glob("*.json")
    users = [os.path.splitext(f)[0] for f in files if os.path.splitext(f)[0].isalnum()]
    
    if users:
        scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=120)
        scroll.pack(fill="x", padx=40, pady=5)
        for u in users:
            ctk.CTkButton(scroll, text=f"👤 {u.capitalize()}", fg_color=CARD_COLOR, anchor="w", height=32, command=lambda name=u: [session.update({"username": name}), dashboard()]).pack(fill="x", pady=1)
            
    e = ctk.CTkEntry(main_frame, placeholder_text="Or enter name...", height=35, fg_color=CARD_COLOR, border_width=0)
    e.pack(padx=40, fill="x", pady=10)
    
    def go():
        val = e.get().strip().lower()
        if not val:
            err.configure(text="Please enter a username.")
            return
        session["username"] = val
        dashboard()
        
    ctk.CTkButton(main_frame, text="Go", fg_color=ACCENT_COLOR, height=35, command=go).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Back", fg_color="transparent", text_color=TEXT_SECONDARY, command=start_page).pack()

def dashboard():
    clear()
    user = load_user()
    ctk.CTkLabel(main_frame, text=f"Hello {str(user.get('username', '')).capitalize()}", font=("Arial", 18, "bold")).pack(pady=10)
    
    card = create_card(main_frame, "Progress")
    workouts = user.get("workouts", [])
    
    try:
        tc = sum(float(w.get("calories", 0)) for w in workouts)
        tm = sum(float(w.get("time_in_min", 0)) for w in workouts)
    except:
        tc, tm = 0, 0
        
    ctk.CTkLabel(card, text=f"{tc:.0f} kcal", font=("Arial", 28, "bold")).pack(anchor="w", padx=12)
    ctk.CTkLabel(card, text=f"{tm:.0f} total minutes", text_color=TEXT_SECONDARY, font=("Arial", 11)).pack(anchor="w", padx=12, pady=(0, 8))

    recent = create_card(main_frame, "Latest")
    if not workouts:
        ctk.CTkLabel(recent, text="No workouts yet", font=("Arial", 12, "italic")).pack(anchor="w", padx=12, pady=5)
    else:
        for w in workouts[-2:]:
            ctk.CTkLabel(recent, text=f"• {w.get('activity')} ({w.get('time_in_min')}m)", font=("Arial", 12)).pack(anchor="w", padx=12, pady=1)
    navbar()

def add_workout():
    clear()
    ctk.CTkLabel(main_frame, text="Log Workout", font=("Arial", 18, "bold")).pack(pady=10)
    err = ctk.CTkLabel(main_frame, text="", text_color=ERROR_COLOR, font=("Arial", 11, "bold"))
    err.pack(pady=2)
    
    box = ctk.CTkFrame(main_frame, fg_color="transparent")
    box.pack(fill="x", padx=30)
    
    act_v = ctk.StringVar(value="Running")
    ctk.CTkOptionMenu(box, values=sorted([a["activity"] for a in ACTIVITIES]), variable=act_v, fg_color=CARD_COLOR, button_color=ACCENT_COLOR, height=32).pack(fill="x", pady=5)
    
    int_v = ctk.StringVar(value="medium")
    ctk.CTkSegmentedButton(box, values=["low", "medium", "high"], variable=int_v, selected_color=ACCENT_COLOR, height=32).pack(fill="x", pady=5)
    
    # Tydlig textetikett ovanför fältet
    ctk.CTkLabel(box, text="Duration (Minutes):", font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(5, 0))
    m_entry = ctk.CTkEntry(box, placeholder_text="e.g. 45", height=35, fg_color=CARD_COLOR, border_width=0, validate="key", validatecommand=(v_float_reg, "%P"))
    m_entry.pack(fill="x", pady=(2, 5))
    
    ctk.CTkLabel(box, text="Comment:", font=("Arial", 12, "bold"), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(5, 0))
    c_entry = ctk.CTkEntry(box, placeholder_text="Optional", height=35, fg_color=CARD_COLOR, border_width=0)
    c_entry.pack(fill="x", pady=(2, 5))
    
    def save():
        try:
            m = float(m_entry.get())
        except:
            err.configure(text="Enter a valid number of minutes.")
            return
            
        user = load_user()
        user["workouts"].append({
            "activity": act_v.get(), 
            "intensity": int_v.get(), 
            "time_in_min": m,
            "calories": calculate_calories(act_v.get(), int_v.get(), m),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "comment": c_entry.get().strip()
        })
        save_user(user)
        dashboard()
        
    ctk.CTkButton(main_frame, text="Save", fg_color=ACCENT_COLOR, height=40, command=save).pack(pady=15, padx=30, fill="x")
    navbar()

def calendar_page():
    clear()
    ctk.CTkLabel(main_frame, text="Activity Calendar", font=("Arial", 18, "bold")).pack(pady=(10, 5))
    box = ctk.CTkFrame(main_frame, fg_color="transparent")
    box.pack(fill="x", padx=15)

    try:
        cal = Calendar(box, font="Arial 9", selectmode='none', background=CARD_COLOR, foreground='white', bordercolor=BG_COLOR,
                       headersbackground=BG_COLOR, headersforeground=TEXT_SECONDARY, normalbackground=CARD_COLOR, normalforeground='white',
                       weekendbackground=CARD_COLOR, weekendforeground=ACCENT_COLOR, showweeknumbers=False)
        cal.pack(pady=5, fill="x")
        
        user = load_user()
        for w in user.get("workouts", []):
            try:
                d = datetime.datetime.strptime(str(w["date"]), "%Y-%m-%d")
                cal.calevent_create(d, ".", "workout_event")
            except:
                continue
        cal.tag_config("workout_event", foreground=DOT_COLOR, font=("Arial", 14, "bold"))
    except:
        pass
        
    ctk.CTkLabel(main_frame, text="● = Activity logged", text_color=DOT_COLOR, font=("Arial", 11)).pack(pady=5)
    navbar()

def history_page():
    clear()
    ctk.CTkLabel(main_frame, text="History", font=("Arial", 18, "bold")).pack(pady=10)
    scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=280)
    scroll.pack(fill="both", expand=True, padx=10)
    
    user = load_user()
    workouts = user.get("workouts", [])
    
    for w in reversed(workouts):
        try:
            date_str = str(w.get('date', 'N/A'))
            act_str = str(w.get('activity', 'Workout'))
            try:
                cals = float(w.get('calories', 0))
            except:
                cals = 0.0
                
            item = ctk.CTkFrame(scroll, fg_color=CARD_COLOR, height=50, cursor="hand2")
            item.pack(fill="x", pady=3)
            
            lbl1 = ctk.CTkLabel(item, text=f"{date_str} - {act_str}", font=("Arial", 11, "bold"))
            lbl1.place(x=10, y=12)
            lbl2 = ctk.CTkLabel(item, text=f"+{cals:.1f} kcal", text_color="#10B981", font=("Arial", 12, "bold"))
            lbl2.place(x=200, y=12)
            
            for widget in (item, lbl1, lbl2):
                widget.bind("<Button-1>", lambda e, data=w: show_workout_details(data))
        except:
            continue
            
    navbar()

def weight_page():
    clear()
    user = load_user()
    ctk.CTkLabel(main_frame, text="Weight Tracker", font=("Arial", 18, "bold")).pack(pady=10)
    err = ctk.CTkLabel(main_frame, text="", text_color=ERROR_COLOR, font=("Arial", 11, "bold"))
    err.pack(pady=2)
    
    box = ctk.CTkFrame(main_frame, fg_color="transparent")
    box.pack(fill="x", padx=30, pady=5)
    
    w_entry = ctk.CTkEntry(box, placeholder_text="Weight (kg)", height=35, fg_color=CARD_COLOR, border_width=0, validate="key", validatecommand=(v_float_reg, "%P"))
    w_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    def save():
        try:
            v = float(w_entry.get())
        except:
            err.configure(text="Enter a valid weight value.")
            return
            
        user["weight"] = v  
        user["weight_history"].append({"date": datetime.datetime.now().strftime("%m-%d"), "weight": v})
        save_user(user)
        weight_page()  
        
    ctk.CTkButton(box, text="Log", fg_color=ACCENT_COLOR, width=70, height=35, command=save).pack(side="right")
    
    history = user.get("weight_history", [])
    if len(history) >= 2:
        try:
            canvas = ctk.CTkCanvas(main_frame, width=300, height=180, bg=CARD_COLOR, highlightthickness=0)
            canvas.pack(pady=15)
            
            logs = history[-6:]
            weights = [float(h["weight"]) for h in logs]
            labels = [str(h["date"]) for h in logs]
            
            max_w, min_w = max(weights) + 2, min(weights) - 2
            if max_w == min_w: max_w += 1
            
            points = []
            for i, w in enumerate(weights):
                x = 30 + (i * (260 / (len(weights) - 1)))
                y = 140 - ((w - min_w) / (max_w - min_w) * 130)
                points.append((x, y))
                canvas.create_oval(x-3, y-3, x+3, y+3, fill=ACCENT_COLOR, outline="")
                canvas.create_text(x, y-12, text=f"{w:.1f}", fill="white", font=("Arial", 8))
                canvas.create_text(x, 160, text=labels[i], fill=TEXT_SECONDARY, font=("Arial", 8))
                
            for i in range(len(points) - 1):
                canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill=ACCENT_COLOR, width=2)
        except:
            pass
    else:
        ctk.CTkLabel(main_frame, text="Log at least 2 entries to see the graph.", font=("Arial", 12, "italic"), text_color=TEXT_SECONDARY).pack(pady=40)
        
    navbar()

def register_page():
    clear()
    ctk.CTkLabel(main_frame, text="New Profile", font=("Arial", 22, "bold")).pack(pady=10)
    err = ctk.CTkLabel(main_frame, text="", text_color=ERROR_COLOR, font=("Arial", 11, "bold"))
    err.pack(pady=2)
    
    fields = {}
    for p in ["Username", "Age", "Height", "Weight"]:
        # Tydlig ledtext ovanför varje fält vid registrering
        ctk.CTkLabel(main_frame, text=f"{p}:" if p == "Username" else f"{p} (numbers only):", font=("Arial", 11, "bold"), text_color=TEXT_SECONDARY, anchor="w").pack(padx=40, fill="x", pady=(4, 0))
        
        if p == "Age":
            e = ctk.CTkEntry(main_frame, placeholder_text="e.g. 25", height=35, fg_color=CARD_COLOR, border_width=0, validate="key", validatecommand=(v_int_reg, "%P"))
        elif p in ["Height", "Weight"]:
            unit = "cm" if p == "Height" else "kg"
            e = ctk.CTkEntry(main_frame, placeholder_text=f"e.g. 175 ({unit})", height=35, fg_color=CARD_COLOR, border_width=0, validate="key", validatecommand=(v_float_reg, "%P"))
        else:
            e = ctk.CTkEntry(main_frame, placeholder_text="Enter name", height=35, fg_color=CARD_COLOR, border_width=0)
            
        e.pack(padx=40, fill="x", pady=(1, 4))
        fields[p] = e
        
    g_var = ctk.StringVar(value="male")
    ctk.CTkSegmentedButton(main_frame, values=["male", "female"], variable=g_var, height=30).pack(pady=5)
    
    def create():
        u = fields["Username"].get().strip().lower()
        if not u:
            err.configure(text="Username cannot be empty.")
            return
        try:
            age = int(fields["Age"].get())
            h = float(fields["Height"].get())
            w = float(fields["Weight"].get())
        except:
            err.configure(text="Please fill all fields with valid numbers.")
            return
            
        session["username"] = u
        data = {
            "username": u, "gender": g_var.get(), "age": age, "height": h, "weight": w, 
            "workouts": [], "weight_history": [{"date": datetime.datetime.now().strftime("%m-%d"), "weight": w}]
        }
        save_user(data)
        dashboard()
        
    ctk.CTkButton(main_frame, text="Create", fg_color=ACCENT_COLOR, height=40, command=create).pack(pady=10, padx=40, fill="x")
    ctk.CTkButton(main_frame, text="Back", fg_color="transparent", text_color=TEXT_SECONDARY, command=start_page).pack()

def logout():
    session["username"] = None
    start_page()

main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
main_frame.pack(fill="both", expand=True)

start_page()
app.mainloop()