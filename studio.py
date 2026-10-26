#!/usr/bin/env python3
"""
PracticAI 365: Native Desktop Studio
A complete standalone windowed desktop application featuring:
- Collapsible Curriculum Tree Menu (52 Weeks, 365 Days)
- Rich Styled Document Viewer (Markdown)
- Syntax-Highlighted Code Editor & Viewer
- Interactive Visual Architecture Canvas (Nodes, Sets & Feedback Loops)
- Built-in Execution Console to run experiments in real time
"""

import os
import sys
import re
import json
import time
import subprocess
import threading
import webbrowser
import textwrap
import queue
import wave
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import notebooklm_studio
import curriculum_generator

# Try importing matplotlib mathtext and PIL for math formula rendering
try:
    import io
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import mathtext
    from PIL import Image, ImageTk, ImageSequence
    HAS_MATHTEXT = True
except ImportError:
    HAS_MATHTEXT = False

# Try importing google.genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# Regex pattern for parsing inline markdown tokens
INLINE_PATTERN = re.compile(
    r'(?P<code_span>`(?P<c_text>[^`\n]+)`)'
    r'|(?P<bold_italic>\*\*\*(?P<bi_text>[^\*\n]+)\*\*\*)'
    r'|(?P<bold>\*\*(?P<b_text>[^\*\n]+)\*\*)'
    r'|(?P<bold_u>__(?P<b_text_u>[^_\n]+)__)'
    r'|(?P<italic>(?<!\w)\*(?P<i_text>[^\*\n]+)\*(?!\w))'
    r'|(?P<italic_u>(?<!\w)_(?P<i_text_u>[^_\n]+)_(?!\w))'
    r'|(?P<math>\$(?P<m_text>[^\$\n]+?)\$)'
    r'|(?P<link>\[(?P<l_text>[^\]\n]+)\]\((?P<l_url>[^\)\n]+)\))'
    r'|(?P<checkbox>\[(?P<chk_val>[ xX])\])'
)

ROOT_DIR = Path(__file__).resolve().parent
LEARNED_DIR = ROOT_DIR / "learned"
LESSONS_DIR = ROOT_DIR / "lessons"
CONFIG_FILE = ROOT_DIR / ".aviation_config.json"
PROGRESS_FILE = ROOT_DIR / ".aviation_progress.json"
PROFILE_FILE = ROOT_DIR / ".aviation_profile.json"

DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
AVAILABLE_GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro-preview"
]

# Color Palette (Deep Modern Dark Theme)
BG_CANVAS = "#090d16"
BG_PANEL = "#0f172a"
BG_SIDEBAR = "#090e1a"
BG_CODE = "#020617"
BORDER = "#1e293b"
BORDER_BRIGHT = "#334155"
TEXT_MAIN = "#f1f5f9"
TEXT_MUTED = "#94a3b8"
TEXT_ACCENT = "#38bdf8"
ACCENT_CYAN = "#06b6d4"
ACCENT_EMERALD = "#10b981"
ACCENT_AMBER = "#f59e0b"
ACCENT_PURPLE = "#a855f7"
ACCENT_PINK = "#ec4899"
ACCENT_RED = "#ef4444"

class PracticAIStudio(tk.Tk):
    def __init__(self, initial_day: int = 1):
        super().__init__()
        self.title("Aviation 365 Studio · The Complete Aviation Ecosystem")
        self.geometry("1400x900")
        self.minsize(1050, 680)
        self.configure(bg=BG_CANVAS)

        # State
        self.current_day = initial_day
        self.current_source = "learned" # "learned" or "lessons"
        self.current_files = {} # filename -> content
        self.active_file = ""
        self.learned_days = set()
        self._link_callbacks = {}
        self._link_counter = 0
        self.active_process = None
        self.console_queue = queue.Queue()

        # Gemini AI Tutor & Code Generation State
        self.gemini_key = ""
        self.gemini_model = DEFAULT_GEMINI_MODEL
        self.gemini_client = None
        self.gemini_queue = queue.Queue()
        self.gemini_worker_thread = None
        self.gemini_stop_requested = False
        self.gemini_chats = {} # day_num -> chat object
        self.gemini_histories = {} # day_num -> list of {"role": "user"|"ai", "text": "...", "code": "..."}
        self.last_generated_code = ""
        self.curriculum_catalog = {}

        # Gamified Knowledge Assessment & Progress Tracking
        self.completed_days = {} # day_num (int) -> dict(stars, score, date, feedback)
        self.total_stars = 0
        self.test_vars = {} # q_idx -> tk.StringVar
        self.test_reasoning_entries = {} # q_idx -> tk.Entry
        self.test_result_banner = None
        self._math_image_cache = {}

        # Student Profile & Learning Style Personalisation
        self.student_profile = {}
        self._load_student_profile()

        # NotebookLM Studio Artifacts & Player State
        self.slides_data = None
        self.current_slide_idx = 0
        self.infographic_data = None
        self.infographic_raw_pil = None
        self.infographic_photo = None
        self.infographic_zoom = 0.75
        self.video_data = None
        self.video_frames = []
        self.video_frame_durations = []
        self.video_frame_idx = 0
        self.video_is_playing = False
        self.video_play_job = None
        self.video_playback_speed = 1.0
        self.video_wav_path = None
        self.video_audio_available = False
        self.video_audio_playing = False
        self.video_audio_muted = False
        self.video_audio_duration_sec = 0.0
        self.video_start_time = 0.0

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._load_gemini_config()
        self._build_curriculum_catalog()
        self._load_progress()
        self._setup_styles()
        self._build_ui()
        self.load_day(initial_day)

        # Start persistent queue consumers on main Tk thread
        self.after(20, self._check_console_queue)
        self.after(30, self._check_gemini_queue)

        self._gen_cancel_requested = False

        # Keyboard shortcuts
        self.bind("<Control-g>", lambda e: self._open_gemini_key_dialog())
        self.bind("<Control-k>", lambda e: self._open_gemini_key_dialog())
        self.bind("<Control-l>", lambda e: self._open_lesson_generator_dialog())
        self.bind("<Control-L>", lambda e: self._open_lesson_generator_dialog())
        self.bind("<F1>", lambda e: self._open_about_dialog())
        self.bind("<Control-h>", lambda e: self._open_about_dialog())
        self.bind("<F2>", lambda e: self._open_personalisation_dialog())
        self.bind("<Control-p>", lambda e: self._open_personalisation_dialog())


    def _scan_learned_days(self):
        """Scans completed days based strictly on passing the Knowledge Assessment test (stars >= 1)."""
        self.learned_days = {d for d, info in self.completed_days.items() if info.get("stars", 0) >= 1}

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Configure generic colors
        self.style.configure(".", background=BG_PANEL, foreground=TEXT_MAIN, bordercolor=BORDER)

        # Treeview styling
        self.style.configure(
            "Treeview",
            background=BG_SIDEBAR,
            foreground=TEXT_MAIN,
            fieldbackground=BG_SIDEBAR,
            rowheight=26,
            font=("Segoe UI", 9)
        )
        self.style.map("Treeview", background=[("selected", "#1e293b")], foreground=[("selected", ACCENT_CYAN)])

        # Notebook tabs styling
        self.style.configure(
            "TNotebook",
            background=BG_PANEL,
            tabmargins=[2, 5, 2, 0]
        )
        self.style.configure(
            "TNotebook.Tab",
            background="#1e293b",
            foreground=TEXT_MUTED,
            padding=[16, 8],
            font=("Segoe UI", 9, "bold")
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", BG_PANEL)],
            foreground=[("selected", ACCENT_CYAN)]
        )

        # Buttons
        self.style.configure(
            "Toolbar.TButton",
            background="#1e293b",
            foreground=TEXT_MAIN,
            font=("Segoe UI", 9, "bold"),
            padding=[10, 5],
            borderwidth=1,
            relief="flat"
        )
        self.style.map("Toolbar.TButton", background=[("active", "#334155")])

        self.style.configure(
            "Run.TButton",
            background=ACCENT_EMERALD,
            foreground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padding=[14, 5],
            relief="flat"
        )
        self.style.map("Run.TButton", background=[("active", "#059669")])

    def _build_ui(self):
        # 1. TOP TOOLBAR
        toolbar = tk.Frame(self, bg=BG_PANEL, height=52, bd=0, highlightthickness=1, highlightbackground=BORDER)
        toolbar.pack(side="top", fill="x")

        # Brand
        brand_frame = tk.Frame(toolbar, bg=BG_PANEL)
        brand_frame.pack(side="left", padx=16, pady=8)
        tk.Label(brand_frame, text="✈️ Aviation 365", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg=BG_PANEL).pack(side="left")
        badge = tk.Label(brand_frame, text="STUDIO", font=("Segoe UI", 7, "bold"), fg="#090d16", bg=ACCENT_CYAN, padx=6, pady=1, cursor="hand2")
        badge.pack(side="left", padx=8)
        badge.bind("<Button-1>", lambda e: self._open_about_dialog())

        # Day Navigator
        nav_frame = tk.Frame(toolbar, bg=BG_PANEL)
        nav_frame.pack(side="left", padx=20)

        btn_prev = tk.Button(nav_frame, text="◀ Prev", font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg="#1e293b",
                             activebackground="#334155", activeforeground="#ffffff", bd=1, relief="solid",
                             command=lambda: self.navigate_day(-1))
        btn_prev.pack(side="left", padx=4)

        tk.Label(nav_frame, text="Day", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=2)
        self.spin_day = tk.Spinbox(nav_frame, from_=1, to=365, width=5, font=("Segoe UI", 10, "bold"),
                                   bg=BG_CODE, fg=ACCENT_CYAN, buttonbackground="#1e293b",
                                   command=self._on_spin_change, bd=1, relief="solid")
        self.spin_day.bind("<Return>", lambda e: self.load_day(int(self.spin_day.get())))
        self.spin_day.pack(side="left", padx=4)

        btn_next = tk.Button(nav_frame, text="Next ▶", font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg="#1e293b",
                             activebackground="#334155", activeforeground="#ffffff", bd=1, relief="solid",
                             command=lambda: self.navigate_day(1))
        btn_next.pack(side="left", padx=4)

        # Source Switcher
        src_frame = tk.Frame(toolbar, bg=BG_PANEL)
        src_frame.pack(side="left", padx=15)
        self.btn_src_learned = tk.Button(src_frame, text="✓ Learned Work", font=("Segoe UI", 8, "bold"),
                                         fg="#090d16", bg=ACCENT_CYAN, bd=1, relief="solid",
                                         command=lambda: self.set_source("learned"))
        self.btn_src_learned.pack(side="left")
        self.btn_src_lessons = tk.Button(src_frame, text="📘 Syllabus Plan", font=("Segoe UI", 8),
                                         fg=TEXT_MUTED, bg="#1e293b", bd=1, relief="solid",
                                         command=lambda: self.set_source("lessons"))
        self.btn_src_lessons.pack(side="left")

        # Action: Run Experiment
        self.btn_run = tk.Button(toolbar, text="▶ Run Experiment", font=("Segoe UI", 9, "bold"),
                                 fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669",
                                 activeforeground="#ffffff", bd=0, padx=14, pady=5, cursor="hand2",
                                 command=self.run_active_experiment)
        self.btn_run.pack(side="left", padx=(16, 6))

        # Action: Set Gemini API Key
        self.btn_gemini_key = tk.Button(toolbar, text="🔑 Set Gemini Key", font=("Segoe UI", 9, "bold"),
                                        fg=ACCENT_AMBER, bg="#1e293b", activebackground="#334155",
                                        activeforeground="#ffffff", bd=1, relief="solid", padx=12, pady=5, cursor="hand2",
                                        command=self._open_gemini_key_dialog)
        self.btn_gemini_key.pack(side="left", padx=4)

        # Action: AI Tutor Quick Jump
        self.btn_open_tutor = tk.Button(toolbar, text="🤖 AI Tutor", font=("Segoe UI", 9, "bold"),
                                        fg="#ffffff", bg=ACCENT_PURPLE, activebackground="#9333ea",
                                        activeforeground="#ffffff", bd=0, padx=12, pady=5, cursor="hand2",
                                        command=lambda: self.notebook.select(self.tab_gemini))
        self.btn_open_tutor.pack(side="left", padx=4)

        # Action: Knowledge Test Quick Jump
        self.btn_take_test = tk.Button(toolbar, text="🎯 Take Test", font=("Segoe UI", 9, "bold"),
                                      fg="#ffffff", bg="#0284c7", activebackground="#0369a1",
                                      activeforeground="#ffffff", bd=0, padx=12, pady=5, cursor="hand2",
                                      command=lambda: self.notebook.select(self.tab_test))
        self.btn_take_test.pack(side="left", padx=4)

        # Action: NotebookLM Studio Modal
        self.btn_notebooklm = tk.Button(toolbar, text="⚡ NotebookLM", font=("Segoe UI", 9, "bold"),
                                       fg="#ffffff", bg="#7c3aed", activebackground="#6d28d9",
                                       activeforeground="#ffffff", bd=0, padx=12, pady=5, cursor="hand2",
                                       command=self._open_notebooklm_dialog)
        self.btn_notebooklm.pack(side="left", padx=4)

        # Action: Lesson & Curriculum Generator Modal
        self.btn_gen_lesson = tk.Button(toolbar, text="🌱 Generate Lesson", font=("Segoe UI", 9, "bold"),
                                       fg="#ffffff", bg="#059669", activebackground="#047857",
                                       activeforeground="#ffffff", bd=0, padx=12, pady=5, cursor="hand2",
                                       command=self._open_lesson_generator_dialog)
        self.btn_gen_lesson.pack(side="left", padx=4)

        # Gamification Badges (Total Stars & Completed Days)
        badge_frame = tk.Frame(toolbar, bg=BG_PANEL)
        badge_frame.pack(side="left", padx=10)
        self.lbl_tb_stars = tk.Label(badge_frame, text=f"⭐ {self.total_stars} Stars", font=("Segoe UI", 8, "bold"),
                                     fg=ACCENT_AMBER, bg="#1e293b", padx=8, pady=3, bd=1, relief="solid")
        self.lbl_tb_stars.pack(side="left", padx=3)
        self.lbl_tb_progress = tk.Label(badge_frame, text=f"🏆 {len(self.learned_days)}/365 Done", font=("Segoe UI", 8, "bold"),
                                        fg=ACCENT_EMERALD, bg="#1e293b", padx=8, pady=3, bd=1, relief="solid")
        self.lbl_tb_progress.pack(side="left", padx=3)

        # Action: About Modal Dialog
        self.btn_about = tk.Button(toolbar, text="ℹ️ About", font=("Segoe UI", 9, "bold"),
                                   fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155",
                                   activeforeground="#ffffff", bd=1, relief="solid", padx=10, pady=4,
                                   cursor="hand2", command=self._open_about_dialog)
        self.btn_about.pack(side="right", padx=(4, 16))

        # Action: Personalisation Modal Dialog (Learning Style, Insights & Profile)
        self.btn_personal = tk.Button(toolbar, text="🎓 Personalisation", font=("Segoe UI", 9, "bold"),
                                      fg="#ffffff", bg="#4f46e5", activebackground="#4338ca",
                                      activeforeground="#ffffff", bd=0, padx=11, pady=4,
                                      cursor="hand2", command=self._open_personalisation_dialog)
        self.btn_personal.pack(side="right", padx=(4, 4))

        # Search Bar
        search_frame = tk.Frame(toolbar, bg=BG_PANEL)
        search_frame.pack(side="right", padx=(16, 0))
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=4)
        self.entry_search = tk.Entry(search_frame, width=22, font=("Segoe UI", 9), bg=BG_CODE, fg=TEXT_MAIN,
                                     insertbackground=TEXT_ACCENT, bd=1, relief="solid")
        self.entry_search.pack(side="left")
        self.entry_search.bind("<KeyRelease>", self._on_search_filter)

        # 2. MAIN HORIZONTAL PANED WINDOW (Sidebar + Content)
        main_pane = tk.PanedWindow(self, orient="horizontal", bg=BORDER, sashwidth=4, bd=0)
        main_pane.pack(fill="both", expand=True)

        # LEFT SIDEBAR FRAME
        sidebar_frame = tk.Frame(main_pane, bg=BG_SIDEBAR, width=320)
        main_pane.add(sidebar_frame, minsize=240)

        # Current Day Files Section
        tk.Label(sidebar_frame, text="CURRENT ARTIFACTS", font=("Segoe UI", 7, "bold"), fg=TEXT_MUTED, bg=BG_SIDEBAR,
                 anchor="w").pack(fill="x", padx=12, pady=(10, 4))
        self.list_files = tk.Listbox(sidebar_frame, height=4, font=("Segoe UI", 9), bg=BG_CODE, fg=TEXT_MAIN,
                                     selectbackground="#1e293b", selectforeground=ACCENT_CYAN, bd=1, relief="solid",
                                     highlightthickness=0)
        self.list_files.pack(fill="x", padx=10, pady=(0, 10))
        self.list_files.bind("<<ListboxSelect>>", self._on_file_select)

        # Curriculum Tree Section
        tk.Label(sidebar_frame, text="52-WEEK CURRICULUM TREE", font=("Segoe UI", 7, "bold"), fg=TEXT_MUTED, bg=BG_SIDEBAR,
                 anchor="w").pack(fill="x", padx=12, pady=(4, 4))
        
        tree_container = tk.Frame(sidebar_frame, bg=BG_SIDEBAR)
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        tree_scroll = ttk.Scrollbar(tree_container)
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_container, selectmode="browse", yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)
        self.tree.heading("#0", text="Curriculum Hierarchy", anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Button-3>", self._on_tree_right_click)

        self._populate_curriculum_tree()

        # RIGHT WORKSPACE (Notebook Tabs)
        workspace = tk.Frame(main_pane, bg=BG_PANEL)
        main_pane.add(workspace, minsize=600)

        self.notebook = ttk.Notebook(workspace)
        self.notebook.pack(fill="both", expand=True)

        # TAB 1: Markdown Document Viewer (Intuitive Lesson)
        self.tab_doc = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_doc, text="  📖 Lesson Document  ")
        self._build_doc_tab(self.tab_doc)

        # TAB 2: Technical Walkthrough (Aviation Physics, Economics & Metrics)
        self.tab_math = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_math, text="  📊 Technical Walkthrough  ")
        self._build_math_tab(self.tab_math)

        # TAB 3: Operational Python Tool & Experiment
        self.tab_code = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_code, text="  🐍 Operational Python Tool  ")
        self._build_code_tab(self.tab_code)

        # TAB 4: Visual Architecture & System Topology Canvas
        self.tab_canvas = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_canvas, text="  🗺️ System Topology & Canvas  ")
        self._build_canvas_tab(self.tab_canvas)

        # TAB 5: Execution Console
        self.tab_console = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_console, text="  💻 Execution Console  ")
        self._build_console_tab(self.tab_console)

        # TAB 6: Aviation AI Specialist & Regulatory Mentor
        self.tab_gemini = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_gemini, text="  🤖 Aviation AI Specialist  ")
        self._build_gemini_tab(self.tab_gemini)

        # TAB 7: Operational Scenario Assessment & Rating
        self.tab_test = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_test, text="  🎯 Scenario Assessment  ")
        self._build_test_tab(self.tab_test)

        # TAB 8: NotebookLM Slide Deck Presentation
        self.tab_slides = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_slides, text="  📽️ Slide Deck  ", state="disabled")
        self._build_slides_tab(self.tab_slides)

        # TAB 9: NotebookLM Executive Infographic
        self.tab_infographic = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_infographic, text="  🖼️ Infographic  ", state="disabled")
        self._build_infographic_tab(self.tab_infographic)

        # TAB 10: NotebookLM Dual-Host Video Overview
        self.tab_video = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(self.tab_video, text="  🎬 Video Overview  ", state="disabled")
        self._build_video_tab(self.tab_video)

        # Tab change listener to keep Canvas, Test & NotebookLM synced when switched
        self.notebook.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed)

        # Tab Switching Shortcuts (Ctrl+1 to Ctrl+0)
        self.bind("<Control-Key-1>", lambda e: self.notebook.select(self.tab_doc))
        self.bind("<Control-Key-2>", lambda e: self.notebook.select(self.tab_math))
        self.bind("<Control-Key-3>", lambda e: self.notebook.select(self.tab_code))
        self.bind("<Control-Key-4>", lambda e: self.notebook.select(self.tab_canvas))
        self.bind("<Control-Key-5>", lambda e: self.notebook.select(self.tab_console))
        self.bind("<Control-Key-6>", lambda e: self.notebook.select(self.tab_gemini))
        self.bind("<Control-Key-7>", lambda e: self.notebook.select(self.tab_test))
        self.bind("<Control-Key-8>", lambda e: self._select_tab_if_enabled(self.tab_slides))
        self.bind("<Control-Key-9>", lambda e: self._select_tab_if_enabled(self.tab_infographic))
        self.bind("<Control-Key-0>", lambda e: self._select_tab_if_enabled(self.tab_video))

        # 3. BOTTOM STATUS BAR
        self.statusbar = tk.Frame(self, bg="#020617", height=24, bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.statusbar.pack(side="bottom", fill="x")
        self.lbl_status = tk.Label(self.statusbar, text="Ready", font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#020617")
        self.lbl_status.pack(side="left", padx=12)

        self.lbl_progress = tk.Label(self.statusbar, text=f"Mastery: {len(self.learned_days)}/365 Days Completed · ⭐ {self.total_stars} Stars",
                                     font=("Segoe UI", 8, "bold"), fg=ACCENT_EMERALD, bg="#020617")
        self.lbl_progress.pack(side="right", padx=12)

        self.lbl_gemini_status = tk.Label(self.statusbar, text="⚡ Gemini: Not Configured", font=("Segoe UI", 8),
                                          fg=ACCENT_AMBER, bg="#020617", cursor="hand2")
        self.lbl_gemini_status.pack(side="right", padx=12)
        self.lbl_gemini_status.bind("<Button-1>", lambda e: self._open_gemini_key_dialog())

        self._update_gemini_ui_status()

    def _build_doc_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#0f172a", height=38, highlightthickness=1, highlightbackground=BORDER)
        top_bar.pack(fill="x")

        self.lbl_doc_title = tk.Label(top_bar, text="📖 Lesson Document", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#0f172a")
        self.lbl_doc_title.pack(side="left", padx=12, pady=6)

        self.lbl_doc_profile_badge = tk.Label(
            top_bar, text="🎯 Profile: Default", font=("Segoe UI", 8),
            fg=ACCENT_CYAN, bg="#1e293b", padx=8, pady=2, bd=1, relief="solid"
        )
        self.lbl_doc_profile_badge.pack(side="left", padx=6, pady=6)

        self.btn_recreate_lesson = tk.Button(
            top_bar,
            text="✨ Recreate with Gemini (Personalized)",
            font=("Segoe UI", 8, "bold"),
            fg="#ffffff",
            bg="#4f46e5",
            activebackground="#4338ca",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.recreate_day_with_gemini
        )
        self.btn_recreate_lesson.pack(side="right", padx=12, pady=6)

        self.lbl_doc_recreate_status = tk.Label(
            top_bar, text="", font=("Segoe UI", 8, "italic"), fg=ACCENT_AMBER, bg="#0f172a"
        )
        self.lbl_doc_recreate_status.pack(side="right", padx=8, pady=6)

        scroll = ttk.Scrollbar(parent)
        scroll.pack(side="right", fill="y")

        self.txt_doc = tk.Text(
            parent,
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            insertbackground=ACCENT_CYAN,
            font=("Segoe UI", 10),
            padx=28,
            pady=20,
            wrap="word",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set
        )
        self.txt_doc.pack(fill="both", expand=True)
        scroll.config(command=self.txt_doc.yview)

        # Configure rich markdown & typography tags
        self._configure_markdown_tags(self.txt_doc)

    def _build_math_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#0f172a", height=38, highlightthickness=1, highlightbackground=BORDER)
        top_bar.pack(fill="x")

        self.lbl_math_title = tk.Label(top_bar, text="📊 Technical Walkthrough · Quantitative Models & Physics", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#0f172a")
        self.lbl_math_title.pack(side="left", padx=12, pady=6)

        scroll = ttk.Scrollbar(parent)
        scroll.pack(side="right", fill="y")

        self.txt_math = tk.Text(
            parent,
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            insertbackground=ACCENT_CYAN,
            font=("Segoe UI", 10),
            padx=28,
            pady=20,
            wrap="word",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set
        )
        self.txt_math.pack(fill="both", expand=True)
        scroll.config(command=self.txt_math.yview)

        # Configure rich markdown & typography tags
        self._configure_markdown_tags(self.txt_math)

    def _build_code_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=32)
        top_bar.pack(fill="x")
        self.lbl_code_filename = tk.Label(top_bar, text="script.py", font=("Consolas", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b")
        self.lbl_code_filename.pack(side="left", padx=12, pady=6)

        btn_run_tab = tk.Button(top_bar, text="▶ Run This Code", font=("Segoe UI", 8, "bold"), fg="#fff", bg=ACCENT_EMERALD,
                                bd=0, padx=10, pady=2, command=self.run_active_experiment)
        btn_run_tab.pack(side="right", padx=12, pady=4)

        scroll = ttk.Scrollbar(parent)
        scroll.pack(side="right", fill="y")

        self.txt_code = tk.Text(
            parent,
            bg=BG_CODE,
            fg="#7dd3fc",
            insertbackground=ACCENT_CYAN,
            font=("Consolas", 10),
            padx=16,
            pady=16,
            wrap="none",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set
        )
        self.txt_code.pack(fill="both", expand=True)
        scroll.config(command=self.txt_code.yview)

    def _build_canvas_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=32)
        top_bar.pack(fill="x")
        tk.Label(top_bar, text="Architecture Diagram & System Topology", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b").pack(side="left", padx=12, pady=6)

        self.canvas = tk.Canvas(parent, bg=BG_CODE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_architecture_canvas())

    def _build_console_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=32)
        top_bar.pack(fill="x")
        self.lbl_console_title = tk.Label(top_bar, text="Execution Output", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b")
        self.lbl_console_title.pack(side="left", padx=12, pady=6)

        btn_stop = tk.Button(top_bar, text="⏹ Stop", font=("Segoe UI", 8, "bold"), fg="#ef4444", bg="#1e293b", bd=0,
                             cursor="hand2", command=self._stop_active_process)
        btn_stop.pack(side="right", padx=(4, 12), pady=4)

        btn_clear = tk.Button(top_bar, text="Clear", font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b", bd=0,
                              cursor="hand2", command=lambda: self.txt_console.delete("1.0", "end"))
        btn_clear.pack(side="right", padx=4, pady=4)

        # Bottom Interactive Input Bar
        input_bar = tk.Frame(parent, bg="#1e293b", height=42, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        input_bar.pack(side="bottom", fill="x")

        self.lbl_input_prompt = tk.Label(input_bar, text="Console Input ↵:", font=("Segoe UI", 9, "bold"), fg=TEXT_ACCENT, bg="#1e293b")
        self.lbl_input_prompt.pack(side="left", padx=(12, 6), pady=6)

        self.entry_console_in = tk.Entry(input_bar, font=("Consolas", 10), bg=BG_CODE, fg="#ffffff", insertbackground="#38bdf8", bd=1, relief="solid")
        self.entry_console_in.pack(side="left", fill="x", expand=True, padx=4, pady=6)
        self.entry_console_in.bind("<Return>", lambda e: self._send_console_input())

        btn_send = tk.Button(input_bar, text="Send ↵", font=("Segoe UI", 8, "bold"), fg="#ffffff", bg=ACCENT_CYAN,
                             activebackground="#0891b2", activeforeground="#ffffff", bd=0, padx=14, pady=3,
                             cursor="hand2", command=self._send_console_input)
        btn_send.pack(side="right", padx=12, pady=6)

        scroll = ttk.Scrollbar(parent)
        scroll.pack(side="right", fill="y")

        self.txt_console = tk.Text(
            parent,
            bg="#020617",
            fg="#38bdf8",
            insertbackground="#ffffff",
            font=("Consolas", 9),
            padx=16,
            pady=16,
            wrap="word",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set
        )
        self.txt_console.pack(fill="both", expand=True)
        scroll.config(command=self.txt_console.yview)

        # Route keypresses in the console text area to the interactive input entry
        self.txt_console.bind("<Key>", self._on_console_text_key)
        self.txt_console.bind("<Button-1>", lambda e: self.entry_console_in.focus_set())

    def _populate_curriculum_tree(self):
        self.tree.delete(*self.tree.get_children())
        
        # Load all 52 weeks
        if not LESSONS_DIR.exists():
            return

        weeks = sorted(list(LESSONS_DIR.glob("week-*")))
        for w in weeks:
            w_name = w.name.replace("week-", "Week ")
            w_num = int(w.name.split("-")[1]) if "-" in w.name else 1
            w_id = self.tree.insert("", "end", text=f"📁 {w_name}", values=(f"week-{w_num:02d}", w_num), open=(w.name == "week-01"))

            days = sorted(list(w.glob("day-*.md")))
            for d in days:
                try:
                    d_num = int(d.stem.split("-")[1])
                    info = self.completed_days.get(d_num)
                    stars = info.get("stars", 0) if info else 0
                    if stars == 3:
                        icon = "⭐⭐⭐"
                    elif stars == 2:
                        icon = "⭐⭐"
                    elif stars == 1:
                        icon = "⭐"
                    else:
                        icon = "⚪"
                    d_id = self.tree.insert(w_id, "end", text=f"{icon} Day {d_num:03d}", values=(d_num,))
                except Exception:
                    pass

    def _on_search_filter(self, event):
        query = self.entry_search.get().strip().lower()
        if not query:
            self._populate_curriculum_tree()
            return

        self.tree.delete(*self.tree.get_children())
        results_id = self.tree.insert("", "end", text=f"🔍 Results for '{query}'", open=True)

        for d in range(1, 366):
            w = ((d - 1) // 7) + 1
            if w > 52: w = 52
            target_f = LESSONS_DIR / f"week-{w:02d}" / f"day-{d:03d}.md"
            if target_f.exists():
                text = target_f.read_text(encoding="utf-8", errors="ignore")
                if query in text.lower():
                    info = self.completed_days.get(d)
                    stars = info.get("stars", 0) if info else 0
                    if stars == 3:
                        icon = "⭐⭐⭐"
                    elif stars == 2:
                        icon = "⭐⭐"
                    elif stars == 1:
                        icon = "⭐"
                    else:
                        icon = "⚪"
                    self.tree.insert(results_id, "end", text=f"{icon} Day {d:03d} (W{w:02d})", values=(d,))

    def _on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item.get("values")
        if values and len(values) > 0:
            val_str = str(values[0])
            if val_str.isdigit():
                day_num = int(val_str)
                self.load_day(day_num)

    def _on_spin_change(self):
        try:
            val = int(self.spin_day.get())
            self.load_day(val)
        except ValueError:
            pass

    def navigate_day(self, delta):
        new_day = self.current_day + delta
        if 1 <= new_day <= 365:
            self.load_day(new_day)

    def set_source(self, src):
        self.current_source = src
        self.btn_src_learned.config(bg=ACCENT_CYAN if src == "learned" else "#1e293b",
                                    fg="#090d16" if src == "learned" else TEXT_MUTED)
        self.btn_src_lessons.config(bg=ACCENT_CYAN if src == "lessons" else "#1e293b",
                                    fg="#090d16" if src == "lessons" else TEXT_MUTED)
        self.load_day(self.current_day)

    def load_day(self, day_num: int):
        self.current_day = day_num
        self.spin_day.delete(0, "end")
        self.spin_day.insert(0, str(day_num))

        # Preserve currently active tab (Canvas, Code, Console, Tutor, Test)
        try:
            active_tab_id = self.notebook.select()
        except Exception:
            active_tab_id = None

        # Check directories
        target_name = f"day-{day_num:03d}"
        learned_dir = None
        for p in LEARNED_DIR.glob(f"**/{target_name}"):
            if p.is_dir():
                learned_dir = p
                break

        w_num = ((day_num - 1) // 7) + 1
        if w_num > 52: w_num = 52
        lesson_file = LESSONS_DIR / f"week-{w_num:02d}" / f"day-{day_num:03d}.md"

        self.current_files = {}
        self.list_files.delete(0, "end")

        use_learned = (self.current_source == "learned" and learned_dir is not None)

        if use_learned and learned_dir:
            self.lbl_status.config(text=f"Loaded from learned/{learned_dir.parent.name}/{learned_dir.name}")
            for f in sorted(learned_dir.glob("*")):
                if f.is_file():
                    self.current_files[f.name] = f.read_text(encoding="utf-8", errors="replace")
                    if f.name in ("analysis.md", "math.md"):
                        self.list_files.insert("end", f"📊 {f.name}")
                    elif f.name.endswith(".py"):
                        self.list_files.insert("end", f"⚡ {f.name}")
                    elif f.name.endswith(".mermaid"):
                        self.list_files.insert("end", f"🗺️ {f.name}")
                    elif f.name in ("slides.json", "slides.md"):
                        self.list_files.insert("end", f"📽️ {f.name}")
                    elif f.name.startswith("infographic."):
                        self.list_files.insert("end", f"🖼️ {f.name}")
                    elif f.name.startswith("video_overview."):
                        self.list_files.insert("end", f"🎬 {f.name}")
                    else:
                        self.list_files.insert("end", f"📄 {f.name}")
        elif lesson_file.exists():
            self.lbl_status.config(text=f"Loaded syllabus from lessons/{lesson_file.parent.name}/{lesson_file.name}")
            self.current_files[lesson_file.name] = lesson_file.read_text(encoding="utf-8", errors="replace")
            self.list_files.insert("end", f"📘 {lesson_file.name}")
            if hasattr(self, "btn_recreate_lesson"):
                self.btn_recreate_lesson.config(text="🌱 Generate Suite from Plan", bg="#059669")
        else:
            self.lbl_status.config(text=f"No artifacts found for Day {day_num:03d}")

        if use_learned and learned_dir and hasattr(self, "btn_recreate_lesson"):
            self.btn_recreate_lesson.config(text="✨ Recreate with Gemini", bg="#334155")

        # Populate viewers
        fnames = list(self.current_files.keys())
        has_py = any(f.endswith(".py") for f in fnames)
        self.btn_run.config(state="normal" if has_py else "disabled")

        if fnames:
            self.list_files.selection_set(0)
            default_f = "README.md" if "README.md" in fnames else fnames[0]
            # Switch tab only if no active tab was previously chosen
            self.display_file(default_f, switch_tab=(active_tab_id is None))

            # Populate Technical Walkthrough Tab
            analysis_f = "analysis.md" if "analysis.md" in self.current_files else ("math.md" if "math.md" in self.current_files else None)
            if analysis_f:
                self._render_markdown_in_text(self.current_files[analysis_f], target_widget=self.txt_math, clear=True)
            else:
                self.txt_math.delete("1.0", "end")
                self.txt_math.insert("1.0", f"# Technical Walkthrough: Day {day_num:03d}\n\nToday's study focuses on qualitative institutional, regulatory, or operational workflows.\nRefer to the Lesson Document and System Architecture Canvas for core ecosystem principles.")

            # If python file exists, show on Code Tab
            py_file = next((f for f in fnames if f.endswith(".py")), None)
            if py_file:
                self.txt_code.delete("1.0", "end")
                self.txt_code.insert("1.0", self.current_files[py_file])
                self.lbl_code_filename.config(text=py_file)
            else:
                self.txt_code.delete("1.0", "end")
                self.txt_code.insert("1.0", "# No Python code artifact for this day.")
                self.lbl_code_filename.config(text="None")
        else:
            self.txt_doc.delete("1.0", "end")
            self.txt_doc.insert("1.0", f"No documents found for Day {day_num:03d}.")
            self.txt_math.delete("1.0", "end")
            self.txt_math.insert("1.0", f"No technical walkthrough found for Day {day_num:03d}.")

        # Check and gate NotebookLM tabs (strictly enabled only when supporting files exist)
        has_slides = (
            "slides.json" in self.current_files
            or "slides.md" in self.current_files
            or (learned_dir and ((learned_dir / "slides.json").exists() or (learned_dir / "slides.md").exists()))
        )
        has_infographic = (
            (learned_dir and (learned_dir / "infographic.svg").exists())
            or (learned_dir and (learned_dir / "infographic.png").exists())
            or "infographic.json" in self.current_files
            or (learned_dir and (learned_dir / "infographic.json").exists())
        )
        has_video = (
            (learned_dir and (learned_dir / "video_overview.wav").exists())
            or (learned_dir and (learned_dir / "video_overview.json").exists())
            or (learned_dir and (learned_dir / "video_overview.webp").exists())
        )

        if hasattr(self, "tab_slides"):
            self.notebook.tab(self.tab_slides, state="normal" if has_slides else "disabled")
            if has_slides:
                self._render_slides_view(learned_dir)
            else:
                self._reset_slides_view()

        if hasattr(self, "tab_infographic"):
            self.notebook.tab(self.tab_infographic, state="normal" if has_infographic else "disabled")
            if has_infographic:
                self._render_infographic_view(learned_dir)
            else:
                self._reset_infographic_view()

        if hasattr(self, "tab_video"):
            self.notebook.tab(self.tab_video, state="normal" if has_video else "disabled")
            if has_video:
                self._render_video_view(learned_dir)
            else:
                self._reset_video_view()

        current_info = self.curriculum_catalog.get(day_num, {})
        day_title = current_info.get("title", f"Day {day_num:03d}")

        if hasattr(self, "lbl_doc_title"):
            self.lbl_doc_title.config(text=f"📖 Day {day_num:03d}: {day_title}")

        if hasattr(self, "lbl_doc_profile_badge"):
            arch = self.student_profile.get("archetype", "🛠️ Hands-On Systems Builder")
            self.lbl_doc_profile_badge.config(text=f"🎯 Customised: {arch}")

        if hasattr(self, "lbl_doc_recreate_status"):
            self.lbl_doc_recreate_status.config(text="")

        if hasattr(self, "lbl_math_title"):
            self.lbl_math_title.config(text=f"📊 Technical Walkthrough · Day {day_num:03d}: {day_title}")

        self._draw_architecture_canvas()
        self._update_gemini_tab_header()
        self._load_day_chat_history(day_num)
        self._render_day_chat(day_num)
        self._update_test_tab_header()
        self._render_test_view()

    def _on_file_select(self, event):
        sel = self.list_files.curselection()
        if not sel: return
        item_text = self.list_files.get(sel[0])
        fname = item_text
        for prefix in ("📄 ", "📘 ", "📐 ", "📊 ", "⚡ ", "🗺️ ", "📽️ ", "🖼️ ", "🎬 "):
            fname = fname.replace(prefix, "")
        fname = fname.strip()
        self.display_file(fname, switch_tab=True)

    def display_file(self, filename, switch_tab=True):
        self.active_file = filename
        content = self.current_files.get(filename, "")

        if filename in ("slides.json", "slides.md"):
            if switch_tab and hasattr(self, "tab_slides") and self.notebook.tab(self.tab_slides, "state") == "normal":
                self.notebook.select(self.tab_slides)
                return
        elif filename.startswith("infographic."):
            if switch_tab and hasattr(self, "tab_infographic") and self.notebook.tab(self.tab_infographic, "state") == "normal":
                self.notebook.select(self.tab_infographic)
                return
        elif filename.startswith("video_overview."):
            if switch_tab and hasattr(self, "tab_video") and self.notebook.tab(self.tab_video, "state") == "normal":
                self.notebook.select(self.tab_video)
                return

        if filename in ("analysis.md", "math.md"):
            if switch_tab:
                self.notebook.select(self.tab_math)
            self._render_markdown_in_text(content, target_widget=self.txt_math, clear=True)
        elif filename.endswith(".md"):
            if switch_tab:
                self.notebook.select(self.tab_doc)
            self._render_markdown_in_text(content, target_widget=self.txt_doc, clear=True)
        elif filename.endswith(".py"):
            if switch_tab:
                self.notebook.select(self.tab_code)
            self.txt_code.delete("1.0", "end")
            self.txt_code.insert("1.0", content)
            self.lbl_code_filename.config(text=filename)
        elif filename.endswith(".mermaid"):
            if switch_tab:
                self.notebook.select(self.tab_canvas)
        else:
            if switch_tab:
                self.notebook.select(self.tab_doc)
            self.txt_doc.delete("1.0", "end")
            self.txt_doc.insert("1.0", content)

    def _on_link_click(self, url: str):
        """Interactive link handler for relative docs, day navigation, scripts, and web links."""
        url = url.strip()
        if not url:
            return

        # Web URLs
        if url.startswith("http://") or url.startswith("https://"):
            try:
                webbrowser.open(url)
                self.lbl_status.config(text=f"Opened in browser: {url}")
            except Exception as e:
                self.lbl_status.config(text=f"Could not open link: {e}")
            return

        # Day link: e.g. day-002.md, ../../lessons/week-01/day-002.md, day-003
        day_match = re.search(r'day-(\d+)', url)
        if day_match:
            target_day = int(day_match.group(1))
            self.load_day(target_day)
            self.lbl_status.config(text=f"Navigated to Day {target_day:03d}")
            return

        # Python experiment / script: e.g. experiment.py, ./experiment.py
        if url.endswith(".py"):
            fname = Path(url).name
            if fname in self.current_files:
                self.display_file(fname)
                self.lbl_status.config(text=f"Viewing code: {fname}")
            else:
                self.notebook.select(self.tab_code)
            return

        # Syllabus / master index: e.g. ../../lessons/README.md or lessons/README.md
        if "lessons" in url and "README.md" in url:
            self.set_source("lessons")
            return

        # Learned index: learned/README.md
        if "learned" in url and "README.md" in url:
            self.set_source("learned")
            return

        # Generic file
        fname = Path(url).name
        if fname in self.current_files:
            self.display_file(fname)
        else:
            self.lbl_status.config(text=f"Link target: {url}")

    def _format_markdown_table(self, table_lines, max_col_width=24):
        """
        Parses markdown table lines (| col 1 | col 2 |), normalizes column widths,
        wraps long cells, and produces aligned Unicode box table output with tags.
        """
        raw_rows = []
        for l in table_lines:
            line_clean = l.strip()
            if not line_clean:
                continue
            parts = [p.strip() for p in line_clean.split('|')]
            if line_clean.startswith('|') and len(parts) > 1:
                parts = parts[1:]
            if line_clean.endswith('|') and len(parts) > 0 and parts[-1] == '':
                parts = parts[:-1]
            raw_rows.append(parts)

        if not raw_rows:
            return []

        header_row = raw_rows[0]
        data_rows = []
        start_idx = 1
        if len(raw_rows) > 1 and all(set(c.replace(':', '').replace('-', '').strip()) == set() for c in raw_rows[1] if c):
            start_idx = 2
        for r in raw_rows[start_idx:]:
            data_rows.append(r)

        num_cols = len(header_row)
        if num_cols == 0:
            return []

        def clean_cell_text(text):
            return re.sub(r'[*_`$]', '', text).strip()

        col_widths = []
        for c_idx in range(num_cols):
            h_text = clean_cell_text(header_row[c_idx]) if c_idx < len(header_row) else ""
            max_len = len(h_text)
            for r in data_rows:
                if c_idx < len(r):
                    max_len = max(max_len, len(clean_cell_text(r[c_idx])))
            w = max(min(max_len + 2, max_col_width), 8)
            col_widths.append(w)

        output_chunks = []
        top_border = "┌" + "┬".join("─" * w for w in col_widths) + "┐\n"
        mid_border = "├" + "┼".join("─" * w for w in col_widths) + "┤\n"
        bot_border = "└" + "┴".join("─" * w for w in col_widths) + "┘\n"

        output_chunks.append((top_border, ("table_border",)))

        clean_h = [clean_cell_text(header_row[i]) if i < len(header_row) else "" for i in range(num_cols)]
        h_wrapped = [textwrap.wrap(clean_h[i], width=col_widths[i] - 2) or [""] for i in range(num_cols)]
        max_h_lines = max(len(w) for w in h_wrapped)
        for s in range(max_h_lines):
            line_str = "│" + "│".join(
                f" {(h_wrapped[i][s] if s < len(h_wrapped[i]) else ''):<{col_widths[i]-2}} "
                for i in range(num_cols)
            ) + "│\n"
            output_chunks.append((line_str, ("table_head",)))

        output_chunks.append((mid_border, ("table_border",)))

        for r_idx, r in enumerate(data_rows):
            clean_cells = [clean_cell_text(r[i]) if i < len(r) else "" for i in range(num_cols)]
            cell_wrapped = [textwrap.wrap(clean_cells[i], width=col_widths[i] - 2) or [""] for i in range(num_cols)]
            max_lines = max(len(w) for w in cell_wrapped)
            row_tag = "table_cell" if r_idx % 2 == 0 else "table_cell_alt"
            for s in range(max_lines):
                line_str = "│" + "│".join(
                    f" {(cell_wrapped[i][s] if s < len(cell_wrapped[i]) else ''):<{col_widths[i]-2}} "
                    for i in range(num_cols)
                ) + "│\n"
                output_chunks.append((line_str, (row_tag,)))

        output_chunks.append((bot_border, ("table_border",)))
        output_chunks.append(("\n", ()))
        return output_chunks

    def _configure_markdown_tags(self, text_widget):
        """Configures the complete rich typography and markdown styling on a Tkinter Text widget."""
        text_widget.tag_configure("h1", font=("Segoe UI", 16, "bold"), foreground="#38bdf8", spacing1=14, spacing3=6)
        text_widget.tag_configure("h2", font=("Segoe UI", 12, "bold"), foreground="#34d399", spacing1=12, spacing3=4)
        text_widget.tag_configure("h3", font=("Segoe UI", 10, "bold"), foreground="#f8fafc", spacing1=10, spacing3=3)
        text_widget.tag_configure("h4", font=("Segoe UI", 9, "bold"), foreground="#94a3b8", spacing1=8, spacing3=2)

        text_widget.tag_configure("normal", font=("Segoe UI", 10), foreground="#cbd5e1", spacing1=2, spacing3=2)
        text_widget.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground="#ffffff")
        text_widget.tag_configure("italic", font=("Segoe UI", 10, "italic"), foreground="#94a3b8")
        text_widget.tag_configure("bold_italic", font=("Segoe UI", 10, "bold", "italic"), foreground="#ffffff")

        text_widget.tag_configure("code", font=("Consolas", 9), background="#1e293b", foreground="#38bdf8")
        text_widget.tag_configure("codeblock", font=("Consolas", 9), background=BG_CODE, foreground="#7dd3fc", lmargin1=24, lmargin2=24, spacing1=2, spacing3=2)

        text_widget.tag_configure("math", font=("Consolas", 9, "italic"), foreground=ACCENT_AMBER, background="#171923")
        text_widget.tag_configure("math_block", font=("Consolas", 10, "italic"), foreground=ACCENT_AMBER, background="#0b1120", lmargin1=28, lmargin2=28, spacing1=6, spacing3=6)

        text_widget.tag_configure("quote", font=("Segoe UI", 9, "italic"), foreground=TEXT_MUTED, lmargin1=24, lmargin2=24)
        text_widget.tag_configure("quote_bar", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN)

        text_widget.tag_configure("bullet", font=("Segoe UI", 10), foreground="#cbd5e1", lmargin1=20, lmargin2=36, spacing1=2, spacing3=2)
        text_widget.tag_configure("bullet_sym", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN)
        text_widget.tag_configure("num_sym", font=("Segoe UI", 9, "bold"), foreground="#60a5fa")

        text_widget.tag_configure("check_todo", font=("Segoe UI", 10), foreground="#64748b")
        text_widget.tag_configure("check_done", font=("Segoe UI", 10, "bold"), foreground=ACCENT_EMERALD)

        text_widget.tag_configure("hr", font=("Consolas", 8), foreground="#334155", spacing1=8, spacing3=8)

        # Table formatting tags
        text_widget.tag_configure("table_border", font=("Consolas", 9), foreground="#334155")
        text_widget.tag_configure("table_head", font=("Consolas", 9, "bold"), foreground=ACCENT_CYAN, background="#1e293b")
        text_widget.tag_configure("table_cell", font=("Consolas", 9), foreground="#cbd5e1", background="#0a101f")
        text_widget.tag_configure("table_cell_alt", font=("Consolas", 9), foreground="#f1f5f9", background="#0f172a")

        # Metadata card tags
        text_widget.tag_configure("meta_label", font=("Consolas", 8), foreground="#64748b", background="#090e1a", lmargin1=16, lmargin2=16)
        text_widget.tag_configure("meta_value", font=("Consolas", 9, "bold"), foreground=ACCENT_CYAN, background="#090e1a", lmargin1=16, lmargin2=16)

        # Chat-specific tags
        text_widget.tag_configure("user_hdr", font=("Segoe UI", 9, "bold"), foreground=ACCENT_CYAN, spacing1=14, spacing3=4)
        text_widget.tag_configure("user_body", font=("Segoe UI", 10), foreground="#f8fafc", lmargin1=16, lmargin2=16, spacing3=10)
        text_widget.tag_configure("ai_hdr", font=("Segoe UI", 9, "bold"), foreground=ACCENT_EMERALD, spacing1=14, spacing3=4)
        text_widget.tag_configure("ai_body", font=("Segoe UI", 10), foreground="#cbd5e1", lmargin1=16, lmargin2=16, spacing3=8)
        text_widget.tag_configure("sys_card", font=("Segoe UI", 9, "italic"), foreground=TEXT_MUTED, background="#090e1a", lmargin1=16, lmargin2=16, spacing1=8, spacing3=8)
        text_widget.tag_configure("error_card", font=("Segoe UI", 9, "bold"), foreground="#f87171", background="#450a0a", lmargin1=16, lmargin2=16, spacing1=6, spacing3=6)

        # Priority elevation
        text_widget.tag_raise("bold")
        text_widget.tag_raise("italic")
        text_widget.tag_raise("bold_italic")
        text_widget.tag_raise("code")
        text_widget.tag_raise("math")

    def _get_rendered_math_formula(self, latex_str: str, fontsize: int = 11, color: str = None, is_display: bool = False):
        """
        Renders a LaTeX math expression into a high-DPI Tkinter PhotoImage using Matplotlib's mathtext engine.
        Results are cached in memory for zero-latency re-renders across views.
        Falls back gracefully to None if matplotlib is unavailable or TeX syntax is invalid.
        """
        if not HAS_MATHTEXT:
            return None

        clean_tex = latex_str.strip()
        if not clean_tex:
            return None

        # Strip outer delimiters if present
        if clean_tex.startswith("$$") and clean_tex.endswith("$$") and len(clean_tex) > 3:
            clean_tex = clean_tex[2:-2].strip()
        elif clean_tex.startswith("$") and clean_tex.endswith("$") and len(clean_tex) > 1:
            clean_tex = clean_tex[1:-1].strip()

        # LaTeX preprocessing for matplotlib mathtext compatibility
        clean_tex = re.sub(r'\\text\{([^}]+)\}', r'\\mathrm{\1}', clean_tex)
        clean_tex = re.sub(r'\\operatorname\{([^}]+)\}', r'\\mathrm{\1}', clean_tex)
        clean_tex = re.sub(r'\\mathbb\{([A-Za-z])\}', r'\\mathbf{\1}', clean_tex)
        clean_tex = re.sub(r'\\bm\{([^}]+)\}', r'\\mathbf{\1}', clean_tex)

        use_color = color or (ACCENT_CYAN if is_display else TEXT_ACCENT)
        dpi = 135 if is_display else 115

        cache_key = (clean_tex, fontsize, use_color, is_display)
        if cache_key in self._math_image_cache:
            return self._math_image_cache[cache_key]

        try:
            tex_expr = f"${clean_tex}$"
            buf = io.BytesIO()
            mathtext.math_to_image(tex_expr, buf, dpi=dpi, format="png", color=use_color)
            buf.seek(0)
            img = Image.open(buf)
            photo = ImageTk.PhotoImage(img)
            self._math_image_cache[cache_key] = photo
            return photo
        except Exception:
            return None

    def _insert_inline_text(self, text: str, base_tags: tuple = ("normal",), target_widget=None):
        """Parses inline tokens (bold, italic, code, math, links, checkboxes) and inserts tagged text / formula images."""
        widget = target_widget or self.txt_doc
        pos = 0
        for m in INLINE_PATTERN.finditer(text):
            if m.start() > pos:
                chunk = text[pos:m.start()]
                widget.insert("end", chunk, base_tags)

            if m.group('code_span'):
                code_str = m.group('c_text')
                widget.insert("end", f" {code_str} ", ("code",))
            elif m.group('bold_italic'):
                bi_str = m.group('bi_text')
                widget.insert("end", bi_str, base_tags + ("bold_italic",))
            elif m.group('bold'):
                b_str = m.group('b_text')
                widget.insert("end", b_str, base_tags + ("bold",))
            elif m.group('bold_u'):
                b_str = m.group('b_text_u')
                widget.insert("end", b_str, base_tags + ("bold",))
            elif m.group('italic'):
                i_str = m.group('i_text')
                widget.insert("end", i_str, base_tags + ("italic",))
            elif m.group('italic_u'):
                i_str = m.group('i_text_u')
                widget.insert("end", i_str, base_tags + ("italic",))
            elif m.group('math'):
                m_str = m.group('m_text')
                photo = self._get_rendered_math_formula(m_str, fontsize=10, color=TEXT_ACCENT, is_display=False)
                if photo:
                    widget.image_create("end", image=photo)
                    if not hasattr(widget, "_embedded_images"):
                        widget._embedded_images = []
                    widget._embedded_images.append(photo)
                else:
                    widget.insert("end", f" {m_str} ", ("math",))
            elif m.group('checkbox'):
                chk = m.group('chk_val').strip().lower()
                widget.insert("end", "☑ " if chk == 'x' else "☐ ", ("check_done" if chk == 'x' else "check_todo",))
            elif m.group('link'):
                l_text = m.group('l_text')
                l_url = m.group('l_url')
                self._link_counter += 1
                link_tag = f"link_{self._link_counter}"
                widget.tag_configure(
                    link_tag,
                    foreground="#38bdf8",
                    underline=True,
                    font=("Segoe UI", 10, "underline")
                )
                widget.tag_bind(link_tag, "<Enter>", lambda e, w=widget: w.config(cursor="hand2"))
                widget.tag_bind(link_tag, "<Leave>", lambda e, w=widget: w.config(cursor=""))
                widget.tag_bind(link_tag, "<Button-1>", lambda e, url=l_url: self._on_link_click(url))
                widget.insert("end", f"{l_text} ↗", (link_tag,))

            pos = m.end()

        if pos < len(text):
            widget.insert("end", text[pos:], base_tags)

    def _render_markdown_in_text(self, markdown_text: str, target_widget=None, clear: bool = True):
        """Custom rich markdown parser and tag applicator for Tkinter Text widget."""
        widget = target_widget or self.txt_doc
        if clear:
            widget.delete("1.0", "end")
            widget._embedded_images = []
        elif not hasattr(widget, "_embedded_images"):
            widget._embedded_images = []

        lines = markdown_text.splitlines()
        total_lines = len(lines)
        idx = 0

        # 1. Frontmatter check (YAML header)
        if lines and lines[0].strip() == "---":
            closing_idx = -1
            for j in range(1, min(25, total_lines)):
                if lines[j].strip() == "---":
                    closing_idx = j
                    break
            if closing_idx != -1:
                meta = {}
                for k in range(1, closing_idx):
                    if ":" in lines[k]:
                        key, val = lines[k].split(":", 1)
                        meta[key.strip()] = val.strip().strip('"').strip("'")

                day_val = meta.get("day", "0")
                try:
                    day_num = int(day_val)
                    day_badge = f" DAY {day_num:03d} "
                except ValueError:
                    day_badge = f" DAY {day_val} "

                week_val = meta.get("week", "01")
                level_val = meta.get("level", "01")
                weekday = meta.get("weekday", "")
                theme = meta.get("theme", "")
                est_time = meta.get("estimated_time", "20-30 min")
                project = meta.get("monthly_project", "")
                level_title = meta.get("level_title", "")

                widget.insert("end", f"┌─{day_badge}───────────────────────────────────────────────────────┐\n", ("table_border",))
                card_line1 = f"│  Week {week_val} · Level {level_val}  │  {weekday} — {theme}  │  ⏱ {est_time}\n"
                widget.insert("end", card_line1, ("meta_value",))
                if level_title or project:
                    card_line2 = f"│  🎯 Focus: {level_title}\n"
                    widget.insert("end", card_line2, ("meta_label",))
                    if project:
                        card_line3 = f"│  🛠 Project: {project}\n"
                        widget.insert("end", card_line3, ("meta_label",))
                widget.insert("end", "└──────────────────────────────────────────────────────────────────┘\n\n", ("table_border",))
                idx = closing_idx + 1

        while idx < total_lines:
            line = lines[idx]
            stripped = line.strip()

            # Fenced code block
            if stripped.startswith("```"):
                lang = stripped.lstrip("`").strip().upper() or "CODE"
                idx += 1
                code_lines = []
                while idx < total_lines and not lines[idx].strip().startswith("```"):
                    code_lines.append(lines[idx])
                    idx += 1
                idx += 1  # skip closing ```

                bar_len = max(10, 54 - len(lang))
                widget.insert("end", f"┌─ [ {lang} ] " + "─" * bar_len + "┐\n", ("table_border",))
                for cl in code_lines:
                    widget.insert("end", f"  {cl}\n", ("codeblock",))
                widget.insert("end", "└" + "─" * (bar_len + len(lang) + 11) + "┘\n\n", ("table_border",))
                continue

            # Display Math block ($$ ... $$)
            if stripped == "$$" or (stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 2):
                if stripped == "$$":
                    idx += 1
                    math_lines = []
                    while idx < total_lines and lines[idx].strip() != "$$":
                        math_lines.append(lines[idx].strip())
                        idx += 1
                    idx += 1
                    math_content = " ".join(math_lines)
                else:
                    math_content = stripped[2:-2].strip()
                    idx += 1

                photo = self._get_rendered_math_formula(math_content, fontsize=12, color=ACCENT_CYAN, is_display=True)
                if photo:
                    widget.insert("end", "   ")
                    widget.image_create("end", image=photo)
                    widget._embedded_images.append(photo)
                    widget.insert("end", "\n\n")
                else:
                    widget.insert("end", f"   📐  {math_content}\n\n", ("math_block",))
                continue

            # Table detection
            if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
                table_lines = []
                while idx < total_lines and lines[idx].strip().startswith("|") and lines[idx].strip().endswith("|"):
                    table_lines.append(lines[idx])
                    idx += 1
                chunks = self._format_markdown_table(table_lines, max_col_width=22)
                for chunk_text, tags in chunks:
                    widget.insert("end", chunk_text, tags)
                continue

            # Headings
            if line.startswith("# "):
                self._insert_inline_text(line[2:], ("h1",), target_widget=widget)
                widget.insert("end", "\n\n")
                idx += 1
                continue
            elif line.startswith("## "):
                self._insert_inline_text(line[3:], ("h2",), target_widget=widget)
                widget.insert("end", "\n\n")
                idx += 1
                continue
            elif line.startswith("### "):
                self._insert_inline_text(line[4:], ("h3",), target_widget=widget)
                widget.insert("end", "\n\n")
                idx += 1
                continue
            elif line.startswith("#### "):
                self._insert_inline_text(line[5:], ("h4",), target_widget=widget)
                widget.insert("end", "\n\n")
                idx += 1
                continue

            # Horizontal rules
            if stripped in ("---", "***", "___", "- - -", "* * *"):
                widget.insert("end", "―" * 64 + "\n\n", ("hr",))
                idx += 1
                continue

            # Blockquote
            if line.startswith("> ") or line == ">":
                q_text = line[2:] if line.startswith("> ") else ""
                widget.insert("end", "  ▎ ", ("quote_bar",))
                self._insert_inline_text(q_text, ("quote",), target_widget=widget)
                widget.insert("end", "\n")
                idx += 1
                continue

            # Checkbox list items: - [ ] or - [x]
            chk_match = re.match(r'^(\s*)[-*+]\s+\[([ xX])\]\s+(.*)$', line)
            if chk_match:
                indent = len(chk_match.group(1))
                is_done = (chk_match.group(2).lower() == 'x')
                widget.insert("end", " " * indent + ("  ☑  " if is_done else "  ☐  "), ("check_done" if is_done else "check_todo",))
                self._insert_inline_text(chk_match.group(3), ("normal",), target_widget=widget)
                widget.insert("end", "\n")
                idx += 1
                continue

            # Bullet list items
            bullet_match = re.match(r'^(\s*)[-*+]\s+(.*)$', line)
            if bullet_match:
                indent = len(bullet_match.group(1))
                widget.insert("end", " " * indent + "  • ", ("bullet_sym",))
                self._insert_inline_text(bullet_match.group(2), ("bullet",), target_widget=widget)
                widget.insert("end", "\n")
                idx += 1
                continue

            # Numbered list items
            num_match = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
            if num_match:
                indent = len(num_match.group(1))
                num = num_match.group(2)
                widget.insert("end", " " * indent + f"  {num}. ", ("num_sym",))
                self._insert_inline_text(num_match.group(3), ("bullet",), target_widget=widget)
                widget.insert("end", "\n")
                idx += 1
                continue

            # Empty line
            if not stripped:
                widget.insert("end", "\n")
                idx += 1
                continue

            # Normal paragraph line
            self._insert_inline_text(line, ("normal",), target_widget=widget)
            widget.insert("end", "\n")
            idx += 1

    def _draw_architecture_canvas(self):
        """Draws visual architecture and topology dynamically for the active day."""
        c = self.canvas
        c.delete("all")
        self.update_idletasks()
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 100 or h < 100:
            w = max(950, self.winfo_width() - 360)
            h = max(650, self.winfo_height() - 150)

        # Background Grid pattern
        for x in range(0, w, 40):
            c.create_line(x, 0, x, h, fill="#0d1527", width=1)
        for y in range(0, h, 40):
            c.create_line(0, y, w, y, fill="#0d1527", width=1)

        # Header Title
        c.create_text(30, 25, anchor="w", text=f"Day {self.current_day:03d} System Architecture & Topology Map",
                      fill="#ffffff", font=("Segoe UI", 12, "bold"))
        c.create_text(w - 30, 25, anchor="e", text="Aviation 365 Ecosystem Canvas",
                      fill=TEXT_MUTED, font=("Segoe UI", 8))

        # Check for day-specific mermaid file in current files or learned directory
        mermaid_fname = next((f for f in self.current_files if f.endswith(".mermaid")), None)
        mermaid_text = ""
        if mermaid_fname and mermaid_fname in self.current_files:
            mermaid_text = self.current_files[mermaid_fname]
        else:
            target_name = f"day-{self.current_day:03d}"
            for p in LEARNED_DIR.glob(f"**/{target_name}/*.mermaid"):
                if p.is_file():
                    mermaid_text = p.read_text(encoding="utf-8", errors="replace")
                    mermaid_fname = p.name
                    break

        if self.current_day == 1 and (mermaid_fname and "taxonomy" in mermaid_fname or not mermaid_text):
            self._draw_day1_taxonomy_canvas(w, h)
        elif mermaid_text:
            self._draw_dynamic_mermaid_canvas(mermaid_text, w, h)
        else:
            self._draw_fallback_canvas(w, h)

    def _draw_dynamic_mermaid_canvas(self, mermaid_text, w, h):
        """Dynamically parses and renders Mermaid flowchart subgraphs, node cards, and arrows."""
        c = self.canvas
        subgraph_pattern = re.compile(r'subgraph\s+([A-Za-z0-9_]+)\s*(?:\["([^"]+)"\])?(.*?)(?=\bend\b)', re.DOTALL)
        node_pattern = re.compile(r'([A-Za-z0-9_]+)\["([^"]+)"\]')

        subgraphs = []
        for sg_id, sg_label, sg_body in subgraph_pattern.findall(mermaid_text):
            label = sg_label if sg_label else sg_id
            nodes = []
            for n_id, n_text in node_pattern.findall(sg_body):
                clean_text = n_text.replace('\\n', '\n').strip()
                nodes.append({"id": n_id, "text": clean_text})
            subgraphs.append({"id": sg_id, "label": label, "nodes": nodes})

        if not subgraphs:
            self._draw_fallback_canvas(w, h)
            return

        palette = [ACCENT_CYAN, ACCENT_EMERALD, ACCENT_PURPLE, ACCENT_AMBER, ACCENT_PINK]
        top_y = 55
        margin_x = 35
        avail_w = w - (margin_x * 2)

        # Special 3-column layout if 5 subgraphs (e.g. Day 2: Inputs | 3 Paradigms | Decision)
        if len(subgraphs) == 5:
            col_w = max(220, (avail_w - 60) // 3)
            # Column 1: Inputs
            self._draw_subgraph_box(subgraphs[0], margin_x, top_y, col_w, h - top_y - 45, palette[0])
            # Column 2: 3 Middle Paradigms stacked vertically
            mid_x = margin_x + col_w + 30
            mid_avail_h = h - top_y - 45
            mid_h = (mid_avail_h - 24) // 3
            for idx, sg in enumerate(subgraphs[1:4]):
                self._draw_subgraph_box(sg, mid_x, top_y + idx * (mid_h + 12), col_w, mid_h, palette[(idx + 1) % len(palette)])
            # Column 3: Decision / Output
            right_x = mid_x + col_w + 30
            self._draw_subgraph_box(subgraphs[4], right_x, top_y, col_w, h - top_y - 45, palette[4])

            # Draw cross-stage connecting arrows
            c.create_line(margin_x + col_w, top_y + (h - top_y - 45) // 2, mid_x, top_y + (h - top_y - 45) // 2,
                          fill="#38bdf8", arrow="last", width=2)
            c.create_line(mid_x + col_w, top_y + (h - top_y - 45) // 2, right_x, top_y + (h - top_y - 45) // 2,
                          fill="#38bdf8", arrow="last", width=2)
            return

        # Standard N-column horizontal distribution (1 to 4 subgraphs)
        N = len(subgraphs)
        gap_x = 24
        col_w = max(200, (avail_w - (gap_x * (N - 1))) // N)
        col_h = max(420, h - top_y - 45)

        for i, sg in enumerate(subgraphs):
            col_x = margin_x + i * (col_w + gap_x)
            color = palette[i % len(palette)]
            self._draw_subgraph_box(sg, col_x, top_y, col_w, col_h, color)

            # Draw connecting arrow to next column
            if i < N - 1:
                next_x = col_x + col_w + gap_x
                mid_y = top_y + 160
                c.create_line(col_x + col_w, mid_y, next_x, mid_y, fill="#38bdf8", arrow="last", width=2)

    def _draw_subgraph_box(self, sg, x, y, box_w, box_h, accent_color):
        """Draws an individual subgraph container box and its internal node cards."""
        c = self.canvas
        # Container background
        c.create_rectangle(x, y, x + box_w, y + box_h, fill="#0b1329", outline=accent_color, width=2)

        # Header Pill
        header_h = 32
        c.create_rectangle(x, y, x + box_w, y + header_h, fill="#0f1e3d", outline=accent_color, width=1)
        c.create_text(x + 12, y + header_h // 2, anchor="w", text=sg["label"][:36],
                      fill=accent_color, font=("Segoe UI", 9, "bold"))

        # Node cards
        nodes = sg["nodes"]
        if not nodes:
            return

        node_margin_x = 12
        card_w = box_w - (node_margin_x * 2)
        avail_card_h = box_h - header_h - 24
        node_h = max(46, min(76, (avail_card_h - (len(nodes) - 1) * 12) // len(nodes)))
        node_gap = 12

        for j, node in enumerate(nodes):
            ny = y + header_h + 14 + j * (node_h + node_gap)
            nx = x + node_margin_x
            if ny + node_h > y + box_h - 4:
                break

            # Node card
            c.create_rectangle(nx, ny, nx + card_w, ny + node_h, fill="#030816", outline="#1e293b", width=1)
            # Accent left border indicator
            c.create_line(nx, ny, nx, ny + node_h, fill=accent_color, width=3)

            # Node text (wrapped)
            lines = node["text"].split("\n")
            if len(lines) == 1 and len(lines[0]) > 32:
                lines = textwrap.wrap(lines[0], width=max(20, int(card_w / 7.5)))

            text_str = "\n".join(lines[:3])
            c.create_text(nx + 10, ny + node_h // 2, anchor="w", text=text_str,
                          fill="#f1f5f9", font=("Segoe UI", 8))

            # Internal connecting downward arrow
            if j < len(nodes) - 1 and (ny + node_h + node_gap <= y + box_h):
                arr_x = nx + card_w // 2
                c.create_line(arr_x, ny + node_h, arr_x, ny + node_h + node_gap,
                              fill=accent_color, arrow="last", width=1)

    def _draw_day1_taxonomy_canvas(self, w, h):
        """Specialized signature diagram for Day 001 Taxonomy & Systems."""
        c = self.canvas
        left_x = 40
        top_y = 60
        box_w = 460
        box_h = 360

        # Outer Box: Artificial Intelligence
        c.create_rectangle(left_x, top_y, left_x + box_w, top_y + box_h, fill="#0c192e", outline=ACCENT_CYAN, width=2)
        c.create_text(left_x + 16, top_y + 18, anchor="w", text="ARTIFICIAL INTELLIGENCE (Broad Computational Rationality)",
                      fill=ACCENT_CYAN, font=("Segoe UI", 9, "bold"))

        # Symbolic AI
        sym_x = left_x + 20
        sym_y = top_y + 40
        c.create_rectangle(sym_x, sym_y, sym_x + 420, sym_y + 55, fill="#1e1b18", outline=ACCENT_AMBER, width=1)
        c.create_text(sym_x + 12, sym_y + 16, anchor="w", text="Symbolic / Deterministic AI", fill=ACCENT_AMBER, font=("Segoe UI", 9, "bold"))
        c.create_text(sym_x + 12, sym_y + 36, anchor="w", text="• A* Search • Minimax • Expert Rule Engines • SMT Solvers", fill=TEXT_MUTED, font=("Segoe UI", 8))

        # Machine Learning Box
        ml_x = left_x + 20
        ml_y = sym_y + 70
        ml_w = 420
        ml_h = 230
        c.create_rectangle(ml_x, ml_y, ml_x + ml_w, ml_y + ml_h, fill="#0d2137", outline="#3b82f6", width=2)
        c.create_text(ml_x + 12, ml_y + 16, anchor="w", text="MACHINE LEARNING (Statistical Optimization over Features)",
                      fill="#60a5fa", font=("Segoe UI", 8, "bold"))

        # Deep Learning Box
        dl_x = ml_x + 16
        dl_y = ml_y + 35
        dl_w = 388
        dl_h = 165
        c.create_rectangle(dl_x, dl_y, dl_x + dl_w, dl_y + dl_h, fill="#1c1335", outline=ACCENT_PURPLE, width=2)
        c.create_text(dl_x + 12, dl_y + 14, anchor="w", text="DEEP LEARNING (Hierarchical Representation Learning)",
                      fill=ACCENT_PURPLE, font=("Segoe UI", 8, "bold"))

        # Generative AI Box
        gen_x = dl_x + 16
        gen_y = dl_y + 35
        gen_w = 356
        gen_h = 110
        c.create_rectangle(gen_x, gen_y, gen_x + gen_w, gen_y + gen_h, fill="#2a1226", outline=ACCENT_PINK, width=2)
        c.create_text(gen_x + 12, gen_y + 14, anchor="w", text="GENERATIVE AI (Density Estimation & Sampling)",
                      fill=ACCENT_PINK, font=("Segoe UI", 8, "bold"))
        c.create_text(gen_x + 12, gen_y + 38, anchor="w", text="• Autoregressive Sequence Transformers (LLMs)", fill=TEXT_MAIN, font=("Segoe UI", 8))
        c.create_text(gen_x + 12, gen_y + 58, anchor="w", text="• Latent Diffusion Models (Image / Video)", fill=TEXT_MAIN, font=("Segoe UI", 8))
        c.create_text(gen_x + 12, gen_y + 78, anchor="w", text="• GANs & Variational Autoencoders", fill=TEXT_MUTED, font=("Segoe UI", 8))

        # Right Side: Agentic Closed Loop
        right_x = left_x + box_w + 50
        right_w = max(380, w - right_x - 40)
        right_h = box_h

        c.create_rectangle(right_x, top_y, right_x + right_w, top_y + right_h, fill="#091b1f", outline=ACCENT_EMERALD, width=2)
        c.create_text(right_x + 16, top_y + 18, anchor="w", text="AGENTIC SYSTEMS (Closed-Loop Stateful Control Topology)",
                      fill=ACCENT_EMERALD, font=("Segoe UI", 9, "bold"))

        nodes = [
            ("1. Perception", "Sensory inputs & environment observations", right_x + 30, top_y + 60),
            ("2. Working Memory", "Persistent state, scratchpad, context history", right_x + 30, top_y + 125),
            ("3. Deliberative Planner", "Reasoning engine (can invoke LLMs / Solvers)", right_x + 30, top_y + 190),
            ("4. Tool Actuation", "Safe API calls, code execution, sandboxes", right_x + 30, top_y + 255),
            ("5. Environmental Feedback", "Self-correction, validation, rollback", right_x + 30, top_y + 315)
        ]

        for idx, (title, desc, nx, ny) in enumerate(nodes):
            c.create_rectangle(nx, ny, nx + right_w - 60, ny + 45, fill="#112d2f", outline="#2dd4bf", width=1)
            c.create_text(nx + 12, ny + 14, anchor="w", text=title, fill="#ffffff", font=("Segoe UI", 9, "bold"))
            c.create_text(nx + 12, ny + 32, anchor="w", text=desc, fill="#99f6e4", font=("Segoe UI", 7))
            if idx < len(nodes) - 1:
                mid_x = nx + (right_w - 60) // 2
                c.create_line(mid_x, ny + 45, mid_x, ny + 65, arrow="last", fill=ACCENT_EMERALD, width=2)

        loop_x = right_x + right_w - 20
        c.create_line(right_x + right_w - 60, top_y + 337, loop_x, top_y + 337, fill=ACCENT_EMERALD, width=2)
        c.create_line(loop_x, top_y + 337, loop_x, top_y + 82, fill=ACCENT_EMERALD, width=2)
        c.create_line(loop_x, top_y + 82, right_x + right_w - 60, top_y + 82, arrow="last", fill=ACCENT_EMERALD, width=2)

        c.create_line(gen_x + gen_w, gen_y + 40, right_x + 30, top_y + 212, dash=(4, 4), arrow="last", fill=ACCENT_PINK, width=2)
        c.create_text((gen_x + gen_w + right_x) // 2, gen_y + 15, text="LLM invokes & powers", fill=ACCENT_PINK, font=("Segoe UI", 7, "bold"))

    def _draw_fallback_canvas(self, w, h):
        """Draws a generic high-contrast pipeline topology card when no Mermaid diagram is present."""
        c = self.canvas
        top_y = 70
        box_w = min(700, w - 80)
        box_x = (w - box_w) // 2
        box_h = 360

        c.create_rectangle(box_x, top_y, box_x + box_w, top_y + box_h, fill="#0b1329", outline=ACCENT_CYAN, width=2)
        c.create_text(box_x + 20, top_y + 25, anchor="w", text=f"Day {self.current_day:03d} Aviation System Lifecycle & Interfaces",
                      fill="#ffffff", font=("Segoe UI", 11, "bold"))

        stages = [
            ("Phase 1: Operational Planning & Regulatory Baseline", "Flight planning, fuel policy, crew FTL compliance, NOTAM/weather minima & continuing airworthiness."),
            ("Phase 2: Ground Turnaround & Collaborative Departure", "A-CDM coordination, loadsheet/CG calculations, passenger & cargo handling, ATC pushback & taxi."),
            ("Phase 3: Trajectory Execution, Separation & Turnaround", "En-route ATM separation, descent profiles, landing rollout, stand arrival & post-flight defect logging.")
        ]

        for i, (st_name, st_desc) in enumerate(stages):
            sy = top_y + 65 + i * 90
            sx = box_x + 30
            sw = box_w - 60
            c.create_rectangle(sx, sy, sx + sw, sy + 65, fill="#030816", outline="#1e293b", width=1)
            c.create_line(sx, sy, sx, sy + 65, fill=ACCENT_CYAN, width=3)
            c.create_text(sx + 16, sy + 20, anchor="w", text=st_name, fill=ACCENT_CYAN, font=("Segoe UI", 9, "bold"))
            c.create_text(sx + 16, sy + 44, anchor="w", text=st_desc, fill=TEXT_MAIN, font=("Segoe UI", 8))

            if i < len(stages) - 1:
                mid_x = sx + sw // 2
                c.create_line(mid_x, sy + 65, mid_x, sy + 90, fill=ACCENT_EMERALD, arrow="last", width=2)

    def run_active_experiment(self):
        """Runs the active day's experiment with real-time streaming output and interactive stdin."""
        target_name = f"day-{self.current_day:03d}"
        learned_dir = None
        for p in LEARNED_DIR.glob(f"**/{target_name}"):
            if p.is_dir():
                learned_dir = p
                break

        if not learned_dir:
            messagebox.showinfo("No Code", f"No completed experiment code found in learned/ for Day {self.current_day:03d}.")
            return

        py_files = list(learned_dir.glob("*.py"))
        if not py_files:
            messagebox.showinfo("No Script", f"No Python script found in {learned_dir.name}.")
            return

        target_py = py_files[0]
        for p in py_files:
            if "experiment" in p.name.lower():
                target_py = p
                break

        # Terminate any previous running process
        if self.active_process and self.active_process.poll() is None:
            try:
                self.active_process.terminate()
            except Exception:
                pass

        self.notebook.select(self.tab_console)
        self.txt_console.delete("1.0", "end")
        self.lbl_console_title.config(text=f"Running {target_py.name}...")
        self.lbl_input_prompt.config(fg=TEXT_ACCENT, text="Interactive Input ↵:")
        self.txt_console.insert("end", f"▶ Running {target_py.name} (Day {self.current_day:03d})...\n")
        self.txt_console.insert("end", "  [Interactive Mode: Type your choices in the console or input bar and press Enter]\n\n")
        self.entry_console_in.focus_set()

        try:
            self.active_process = subprocess.Popen(
                [sys.executable, "-u", str(target_py)],
                cwd=str(learned_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
        except Exception as e:
            self._append_console_output(f"Failed to launch process: {e}\n")
            return

        def _stream_reader(proc, name):
            t0 = time.perf_counter()
            try:
                buffer = []
                while True:
                    ch = proc.stdout.read(1)
                    if not ch:
                        break
                    buffer.append(ch)
                    # Flush immediately on newline or prompt punctuation so user sees prompt without waiting for \n
                    if ch == "\n" or ch in (":", ">", "?") or len(buffer) >= 64:
                        chunk = "".join(buffer)
                        buffer.clear()
                        self.console_queue.put(("output", chunk))
                        if ch in (":", ">", "?"):
                            self.console_queue.put(("prompt", None))

                if buffer:
                    chunk = "".join(buffer)
                    self.console_queue.put(("output", chunk))
            except Exception:
                pass

            proc.wait()
            elapsed = time.perf_counter() - t0
            code = proc.returncode
            self.console_queue.put(("complete", (code, elapsed, name)))

        threading.Thread(target=_stream_reader, args=(self.active_process, target_py.name), daemon=True).start()

    def _check_console_queue(self):
        """Periodically polls console messages from worker threads on the main Tk thread."""
        try:
            while True:
                msg_type, payload = self.console_queue.get_nowait()
                if msg_type == "output":
                    self._append_console_output(payload)
                elif msg_type == "prompt":
                    self.entry_console_in.focus_set()
                    self.lbl_input_prompt.config(fg="#34d399", text="Your Input ↵:")
                elif msg_type == "complete":
                    code, elapsed, name = payload
                    self._on_experiment_complete(code, elapsed, name)
                    self.lbl_input_prompt.config(fg=TEXT_MUTED, text="Console Input:")
        except queue.Empty:
            pass
        finally:
            self.after(20, self._check_console_queue)

    def _on_console_text_key(self, event):
        """Routes key events pressed inside the console output text box directly into the input entry."""
        if event.keysym in ("Return", "KP_Enter"):
            self._send_console_input()
            return "break"
        elif event.keysym == "BackSpace":
            current = self.entry_console_in.get()
            if current:
                self.entry_console_in.delete(len(current) - 1, "end")
            self.entry_console_in.focus_set()
            return "break"
        elif event.char and event.char.isprintable():
            self.entry_console_in.insert("end", event.char)
            self.entry_console_in.focus_set()
            return "break"
        return None

    def _stop_active_process(self):
        """Terminates any active running experiment process."""
        if self.active_process and self.active_process.poll() is None:
            try:
                self.active_process.terminate()
                self._append_console_output("\n\n[⏹ Process terminated by user]\n")
                self.lbl_console_title.config(text="Process Stopped")
                self.lbl_input_prompt.config(fg=TEXT_MUTED, text="Console Input:")
            except Exception as e:
                self._append_console_output(f"\n[Error stopping process]: {e}\n")

    def _send_console_input(self):
        """Sends user typed input from the entry bar to the active running subprocess."""
        text = self.entry_console_in.get()
        self.entry_console_in.delete(0, "end")
        if self.active_process and self.active_process.poll() is None:
            try:
                self.active_process.stdin.write(text + "\n")
                self.active_process.stdin.flush()
                self._append_console_output(f"{text}\n")
                self.lbl_input_prompt.config(fg=TEXT_ACCENT, text="Interactive Input ↵:")
            except Exception as e:
                self._append_console_output(f"\n[Stdin Error]: {e}\n")
        else:
            self._append_console_output(f"[Notice: No active running process to receive input]\n")

    def _append_console_output(self, text):
        """Appends output text and scrolls to the latest position."""
        self.txt_console.insert("end", text)
        self.txt_console.see("end")

    def _on_experiment_complete(self, code, elapsed, script_name):
        status = "PASSED" if code == 0 else f"EXIT {code}"
        self.lbl_console_title.config(text=f"{script_name}: {status} ({elapsed:.3f}s)")
        self.txt_console.insert("end", f"\n[Process completed in {elapsed:.3f}s with exit code {code}]\n")
        self.txt_console.see("end")

    # =========================================================================
    # STUDENT PROFILE, LEARNING STYLE & TUTOR INSIGHTS
    # =========================================================================

    def _get_default_profile(self) -> dict:
        return {
            "student_name": "Aviation 365 Student",
            "archetype": "🛠️ Hands-On Systems Builder",
            "archetype_desc": "Prefers concrete code examples, running experiments immediately, and inspecting intermediate state over abstract mathematical proofs.",
            "scores": {
                "code_vs_theory": 80,
                "systems_vs_primitives": 75,
                "visual_vs_verbal": 70,
                "pace_and_density": 85
            },
            "preferences": {
                "explanation_depth": "Balanced Intuition + Mechanics",
                "math_rigor": "Plain-English Intuitive Translation",
                "code_style": "Production-grade, annotated with intermediate printouts",
                "custom_directives": ""
            },
            "tutor_insights": {
                "summary": "Learner tends to ask for hands-on code examples, edge-case behavior, and how abstractions translate into runtime execution.",
                "frequent_topics": ["Runtime Mechanics", "Edge Cases", "Code Implementation"],
                "inquiries": []
            }
        }

    def _load_student_profile(self):
        """Loads persistent student profile, learning style scores, and inquiry insights."""
        self.student_profile = self._get_default_profile()
        if PROFILE_FILE.exists():
            try:
                data = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, dict) and isinstance(self.student_profile.get(k), dict):
                            self.student_profile[k].update(v)
                        else:
                            self.student_profile[k] = v
            except Exception as e:
                print(f"Error reading profile file: {e}")
        else:
            self._save_student_profile()

    def _save_student_profile(self):
        """Persists student profile, learning style archetype, and insights to .aviation_profile.json."""
        try:
            PROFILE_FILE.write_text(json.dumps(self.student_profile, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"Error saving profile: {e}")

    def _record_student_inquiry(self, query: str, day_num: int):
        """Records custom (non-quick-prompt) student queries and updates tutor insights."""
        if not query or len(query.strip()) < 3:
            return

        q_lower = query.lower()

        # Classify inquiry domain
        if any(k in q_lower for k in ["error", "fail", "break", "edge", "bug", "crash", "exception", "why does it fail"]):
            cat = "Edge Cases & Failure Modes"
        elif any(k in q_lower for k in ["math", "derive", "formula", "proof", "loss", "gradient", "calculus", "equation", "matrix"]):
            cat = "Mathematical Derivations"
        elif any(k in q_lower for k in ["pipeline", "architecture", "system", "topology", "scale", "state", "diagram", "interface"]):
            cat = "Architecture & Systems"
        elif any(k in q_lower for k in ["code", "function", "implement", "syntax", "python", "script", "run", "class", "def "]):
            cat = "Implementation & Code"
        elif any(k in q_lower for k in ["latency", "benchmark", "speed", "complexity", "memory", "profile", "fast", "cache", "throughput"]):
            cat = "Performance & Optimization"
        else:
            cat = "Conceptual Intuition & Mechanics"

        entry = {
            "day": day_num,
            "timestamp": time.strftime("%Y-%m-%d %H:%M"),
            "category": cat,
            "query": query[:240]
        }

        t_insights = self.student_profile.setdefault("tutor_insights", {})
        inquiries = t_insights.setdefault("inquiries", [])
        inquiries.append(entry)
        if len(inquiries) > 60:
            inquiries.pop(0)

        # Re-synthesize frequent topics and observation summary
        cat_counts = {}
        for item in inquiries:
            c = item.get("category", "General")
            cat_counts[c] = cat_counts.get(c, 0) + 1

        sorted_cats = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)
        top_topics = [c for c, _ in sorted_cats[:3]]
        t_insights["frequent_topics"] = top_topics

        # Synthesize observation summary
        if len(inquiries) == 1:
            summary = f"Student initiated custom enquiry focusing on {top_topics[0]}."
        elif len(top_topics) >= 2:
            summary = (
                f"Student primarily explores {top_topics[0]} ({cat_counts[top_topics[0]]}x) and {top_topics[1]} ({cat_counts[top_topics[1]]}x). "
                f"Tends to ask detailed questions on concrete mechanics, system invariants, and runtime behavior."
            )
        else:
            summary = f"Student questions consistently focus on {top_topics[0]}."

        t_insights["summary"] = summary
        self._save_student_profile()

    def _get_learned_day_dir(self, day_num: int) -> Path:
        """Returns the path to the learned directory for day_num."""
        target_name = f"day-{day_num:03d}"
        for p in LEARNED_DIR.glob(f"**/{target_name}"):
            if p.is_dir():
                return p
        w = ((day_num - 1) // 7) + 1
        if w > 52: w = 52
        return LEARNED_DIR / f"week-{w:02d}" / target_name

    def _load_day_chat_history(self, day_num: int):
        """Loads persisted chat history for day_num from learned/week-XX/day-YYY/chat_history.json."""
        day_dir = self._get_learned_day_dir(day_num)
        chat_f = day_dir / "chat_history.json"
        if chat_f.exists():
            try:
                data = json.loads(chat_f.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.gemini_histories[day_num] = data
                    return
            except Exception:
                pass
        if day_num not in self.gemini_histories:
            self.gemini_histories[day_num] = []

    def _save_day_chat_history(self, day_num: int):
        """Persists the chat history for day_num into learned/week-XX/day-YYY/chat_history.json."""
        day_dir = self._get_learned_day_dir(day_num)
        try:
            day_dir.mkdir(parents=True, exist_ok=True)
            chat_f = day_dir / "chat_history.json"
            history = self.gemini_histories.get(day_num, [])
            chat_f.write_text(json.dumps(history, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"Error saving chat history for Day {day_num:03d}: {e}")

    # =========================================================================
    # GEMINI AI TUTOR & CODE GENERATION INTEGRATION
    # =========================================================================

    def _load_gemini_config(self):
        """Loads Gemini API key and model preference from config file or environment variable."""
        self.gemini_key = ""
        self.gemini_model = DEFAULT_GEMINI_MODEL
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                self.gemini_key = data.get("gemini_api_key", "").strip()
                self.gemini_model = data.get("gemini_model", DEFAULT_GEMINI_MODEL).strip()
            except Exception:
                pass
        if not self.gemini_key:
            self.gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
        self._init_gemini_client()

    def _save_gemini_config(self, key: str, model: str):
        """Persists Gemini configuration to local config file and updates active client."""
        self.gemini_key = key.strip()
        self.gemini_model = model.strip() if model.strip() else DEFAULT_GEMINI_MODEL
        try:
            payload = {
                "gemini_api_key": self.gemini_key,
                "gemini_model": self.gemini_model
            }
            CONFIG_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            os.environ["GEMINI_API_KEY"] = self.gemini_key
        except Exception as e:
            print(f"Error persisting Gemini config: {e}")
        self._init_gemini_client()
        self._update_gemini_ui_status()
        self.gemini_chats.clear() # Reset chat sessions with updated client / key

    def _init_gemini_client(self):
        """Initializes or resets google.genai Client."""
        self.gemini_client = None
        if self.gemini_key and GENAI_AVAILABLE:
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_key)
            except Exception as e:
                print(f"Gemini client initialization error: {e}")

    def _update_gemini_ui_status(self):
        """Updates toolbar button, statusbar, and tutor tab badges according to key status."""
        has_key = bool(self.gemini_key)
        if hasattr(self, "btn_gemini_key"):
            if has_key:
                self.btn_gemini_key.config(text="🔑 Gemini: Ready", fg="#34d399", bg="#064e3b")
            else:
                self.btn_gemini_key.config(text="🔑 Set Gemini Key", fg=ACCENT_AMBER, bg="#1e293b")
        if hasattr(self, "lbl_gemini_status"):
            if has_key:
                self.lbl_gemini_status.config(text=f"⚡ Gemini: Ready ({self.gemini_model})", fg=ACCENT_EMERALD)
            else:
                self.lbl_gemini_status.config(text="⚡ Gemini: Key Not Configured", fg=ACCENT_AMBER)
        if hasattr(self, "lbl_tutor_model_badge"):
            if has_key:
                self.lbl_tutor_model_badge.config(text=f"⚡ {self.gemini_model}", fg=ACCENT_EMERALD)
            else:
                self.lbl_tutor_model_badge.config(text="⚠️ Key Required", fg=ACCENT_AMBER)

    def _open_gemini_key_dialog(self):
        """Displays a clean modal dialog to enter/verify/save the user's Gemini API key."""
        dialog = tk.Toplevel(self)
        dialog.title("🔑 Gemini API Configuration")
        dialog.geometry("560x440")
        dialog.configure(bg=BG_PANEL)
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog over main window
        try:
            self.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() - 560) // 2
            y = self.winfo_y() + (self.winfo_height() - 440) // 2
            dialog.geometry(f"+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

        # Title
        tk.Label(dialog, text="Gemini API Configuration", font=("Segoe UI", 13, "bold"), fg="#ffffff", bg=BG_PANEL).pack(padx=24, pady=(18, 4), anchor="w")
        tk.Label(dialog, text="Configure your Google Gemini API key to enable intelligent AI mentoring, technical walkthrough generation, and custom operational experiment code creation at the level of each day.",
                 font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL, wraplength=510, justify="left").pack(padx=24, pady=(0, 10), anchor="w")

        # Google AI Studio link
        link_frame = tk.Frame(dialog, bg=BG_PANEL)
        link_frame.pack(fill="x", padx=24, pady=(0, 14))
        lbl_link = tk.Label(link_frame, text="👉 Get a free Gemini API key at Google AI Studio (aistudio.google.com) ↗",
                            font=("Segoe UI", 9, "underline"), fg=TEXT_ACCENT, bg=BG_PANEL, cursor="hand2")
        lbl_link.pack(side="left")
        lbl_link.bind("<Button-1>", lambda e: webbrowser.open("https://aistudio.google.com/app/apikey"))

        # API Key input
        tk.Label(dialog, text="Google Gemini API Key:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_PANEL).pack(padx=24, anchor="w")
        entry_key = tk.Entry(dialog, font=("Consolas", 10), bg=BG_CODE, fg="#ffffff", insertbackground=TEXT_ACCENT, bd=1, relief="solid", show="•")
        entry_key.pack(fill="x", padx=24, pady=(4, 6))
        if self.gemini_key:
            entry_key.insert(0, self.gemini_key)

        var_show = tk.BooleanVar(value=False)
        def _toggle_key_vis():
            entry_key.config(show="" if var_show.get() else "•")
        chk_show = tk.Checkbutton(dialog, text="Show key characters", variable=var_show, command=_toggle_key_vis,
                                  font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL, selectcolor=BG_CODE, activebackground=BG_PANEL)
        chk_show.pack(padx=24, anchor="w", pady=(0, 12))

        # Model Combobox
        tk.Label(dialog, text="Gemini Model:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_PANEL).pack(padx=24, anchor="w")
        combo_model = ttk.Combobox(dialog, values=AVAILABLE_GEMINI_MODELS, state="readonly", font=("Segoe UI", 9))
        combo_model.set(self.gemini_model if self.gemini_model in AVAILABLE_GEMINI_MODELS else DEFAULT_GEMINI_MODEL)
        combo_model.pack(fill="x", padx=24, pady=(4, 14))

        # Status Label
        lbl_test_status = tk.Label(dialog, text="Status: Ready", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL)
        lbl_test_status.pack(padx=24, anchor="w", pady=(0, 16))

        # Connection test worker
        def _test_connection():
            key_val = entry_key.get().strip()
            model_val = combo_model.get().strip()
            if not key_val:
                lbl_test_status.config(text="❌ Please enter an API key first.", fg="#f87171")
                return
            lbl_test_status.config(text="⏳ Testing connection with Google Gemini API...", fg=ACCENT_AMBER)
            btn_test.config(state="disabled")

            def _worker():
                try:
                    from google import genai
                    c = genai.Client(api_key=key_val)
                    resp = c.models.generate_content(model=model_val, contents="Hi, reply with one word: Connected")
                    txt = resp.text.strip() if hasattr(resp, "text") and resp.text else "OK"
                    dialog.after(0, lambda: lbl_test_status.config(text=f"✓ Success! Connected to {model_val} ({txt[:30]})", fg=ACCENT_EMERALD))
                except Exception as ex:
                    dialog.after(0, lambda: lbl_test_status.config(text=f"❌ Connection failed: {str(ex)[:70]}", fg="#f87171"))
                finally:
                    dialog.after(0, lambda: btn_test.config(state="normal"))

            threading.Thread(target=_worker, daemon=True).start()

        # Save and close
        def _save_and_close():
            key_val = entry_key.get().strip()
            model_val = combo_model.get().strip()
            self._save_gemini_config(key_val, model_val)
            dialog.destroy()
            self.lbl_status.config(text=f"Gemini configuration updated: {model_val}")

        # Buttons
        btn_frame = tk.Frame(dialog, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=24, pady=(0, 16))

        btn_test = tk.Button(btn_frame, text="⚡ Test Connection", font=("Segoe UI", 9, "bold"),
                             fg="#ffffff", bg=ACCENT_CYAN, activebackground="#0891b2", bd=0, padx=12, pady=5,
                             cursor="hand2", command=_test_connection)
        btn_test.pack(side="left")

        btn_cancel = tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 9), fg=TEXT_MUTED, bg="#1e293b",
                               activebackground="#334155", bd=0, padx=12, pady=5, cursor="hand2", command=dialog.destroy)
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(btn_frame, text="Save Configuration", font=("Segoe UI", 9, "bold"),
                             fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", bd=0, padx=14, pady=5,
                             cursor="hand2", command=_save_and_close)
        btn_save.pack(side="right")

    def _open_about_dialog(self):
        """Displays a comprehensive About modal explaining PracticAI 365, philosophy, workspaces, rules, and navigation."""
        dialog = tk.Toplevel(self)
        dialog.title("ℹ️ About Aviation 365 Studio")
        dialog.geometry("780x640")
        dialog.minsize(680, 500)
        dialog.configure(bg=BG_PANEL)
        dialog.transient(self)
        dialog.grab_set()

        # Center on parent
        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 390
            y = self.winfo_y() + (self.winfo_height() // 2) - 320
            dialog.geometry(f"780x640+{max(40, x)}+{max(40, y)}")
        except Exception:
            pass

        # 1. Header Frame
        header = tk.Frame(dialog, bg=BG_PANEL, height=75)
        header.pack(fill="x")

        title_row = tk.Frame(header, bg=BG_PANEL)
        title_row.pack(fill="x", padx=20, pady=(12, 4))

        tk.Label(title_row, text="✈️ Aviation 365 Studio · The Complete Aviation Ecosystem", font=("Segoe UI", 13, "bold"),
                 fg="#ffffff", bg=BG_PANEL).pack(side="left")
        badge_ver = tk.Label(title_row, text="v1.0 RELEASE", font=("Segoe UI", 7, "bold"),
                             fg="#090d16", bg=ACCENT_CYAN, padx=6, pady=1)
        badge_ver.pack(side="left", padx=10)

        tk.Label(header, text="The Complete Civil Aviation Ecosystem: Operational, Technical, Regulatory & Human Systems",
                 font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", padx=20, pady=(0, 10))

        # 2. Badges Bar
        badges_bar = tk.Frame(dialog, bg="#090e1a", height=32, highlightthickness=1, highlightbackground=BORDER)
        badges_bar.pack(fill="x")
        badges = [
            ("365 Days", "#38bdf8", "#0b2038"),
            ("52 Weeks", "#a855f7", "#28123d"),
            ("7 Workspaces", "#10b981", "#092e21"),
            ("ICAO & EASA Aligned", "#f59e0b", "#362106"),
            ("100% Local & Private", "#ec4899", "#3b1126")
        ]
        for text, fg, bg in badges:
            b = tk.Label(badges_bar, text=f"• {text}", font=("Segoe UI", 8, "bold"),
                         fg=fg, bg=bg, padx=8, pady=2, bd=1, relief="solid")
            b.pack(side="left", padx=6, pady=5)

        # 3. Scrollable Content Container
        container = tk.Frame(dialog, bg=BG_PANEL)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=BG_PANEL)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=max(600, e.width - 20)))

        # Mouse wheel support
        def _on_mousewheel(event):
            delta = int(-1 * (event.delta / 120)) if event.delta else 0
            canvas.yview_scroll(delta, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        dialog.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Card builder helper
        def add_card(title, title_color, content_items):
            card = tk.Frame(scrollable, bg=BG_PANEL, bd=1, relief="solid", highlightthickness=1, highlightbackground="#334155")
            card.pack(fill="x", pady=6, padx=4)

            hdr = tk.Frame(card, bg=BG_PANEL)
            hdr.pack(fill="x", padx=16, pady=(10, 4))
            tk.Label(hdr, text=title, font=("Segoe UI", 10, "bold"), fg=title_color, bg=BG_PANEL).pack(side="left")

            for item in content_items:
                if isinstance(item, tuple):
                    prefix, body = item
                    row = tk.Frame(card, bg=BG_PANEL)
                    row.pack(fill="x", padx=16, pady=2)
                    tk.Label(row, text=prefix, font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=BG_PANEL).pack(side="left", anchor="n")
                    tk.Label(row, text=body, font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_PANEL, wraplength=640, justify="left").pack(side="left", fill="x", expand=True, padx=(4, 0))
                else:
                    tk.Label(card, text=item, font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_PANEL, wraplength=700, justify="left").pack(anchor="w", padx=16, pady=2)
            tk.Frame(card, height=8, bg=BG_PANEL).pack()

        # Section 1: Philosophy
        add_card("✈️ 1. The Core Philosophy: Aviation as a System of Systems", ACCENT_CYAN, [
            "Aviation 365 is a year-long, self-contained desktop learning environment designed to master aviation as a connected operational, technical, regulatory and human system — from international rules and aircraft physics to flight dispatch, airport turnarounds, air traffic management, and safety governance.",
            "A flight can be technically airworthy yet unable to depart because of weather minima, crew duty limits, an unavailable stand, a baggage problem, a failed communication link or an airspace restriction. Aviation 365 makes those systemic connections visible.",
            "Evidence Over Assertion: We distinguish what a statutory regulation requires (ICAO SARPs, EASA IRs, FARs), what an airline chooses in its Operations Manual (Part-A/B/C/D), what industry commonly practices, and what is merely proposed."
        ])

        # Section 2: Workspaces
        add_card("🛠️ 2. The 7 Aviation Workspaces Explained", ACCENT_EMERALD, [
            ("📖 Lesson Document: ", "Operational lesson guide establishing the concept, weekly rhythm, regulatory foundations, operational workflows, and real-world system interfaces."),
            ("📊 Operational & Technical Analysis: ", "Analytical deep-dive rendering authentic flight physics, aerodynamics, navigation geometry, payload-range trade-offs, fuel reserves, CASK/RASK economics, or regulatory decision matrices with worked numerical traces."),
            ("🐍 Operational Python Tool: ", "Interactive, self-contained Python tools and simulations that directly support the day's subject (dispatch viability, turnaround critical paths, fuel burn, wind triangles, or connectivity metrics)."),
            ("🗺️ System Topology Canvas: ", "Interactive visual architecture diagrams showing organisations, services, information flows (AFTN, A-CDM, NMOC), and multi-stakeholder dependencies."),
            ("💻 Execution Console: ", "Real-time streaming subprocess runner featuring bidirectional interactive input, parameter tuning, and operational failure stress-testing."),
            ("🤖 Aviation AI Specialist: ", "Pedagogically bounded mentor steeped in ICAO Annexes, EASA Easy Access Rules, airline dispatch, ATM, and safety engineering."),
            ("🎯 Scenario Assessment: ", "High-signal operational scenario assessments testing practical decision-making with a 0–3 Stars rating system (⭐⭐⭐ Mastered, ⭐⭐ Proficient, ⭐ Developing, ⚪ Unfinished).")
        ])

        # Section 3: Experiment Rules
        add_card("📐 3. The Aviation Operational Experiment Principles", ACCENT_PURPLE, [
            ("Principle 1 · Direct Domain Support: ", "Every Python experiment must directly model the day's aviation subject — never math for the sake of math."),
            ("Principle 2 · Interactive Parameter Exploration: ", "Prompt for operational variables (payload, winds, fuel, runway condition, duty hours) with sensible defaults."),
            ("Principle 3 · Transparent Operational Working: ", "'Show the Working' — display intermediate flight dispatch, performance, aerodynamic, or economic calculations."),
            ("Principle 4 · SMS Adversarial Stress Testing: ", "Simulate degrading weather, equipment deferrals (MEL), slot revisions, or crew timeouts to test operational margins."),
            ("Principle 5 · Clean Exit & Zero External Dependencies: ", "Completely self-contained standard library Python running reliably on any workstation.")
        ])

        # Section 4: Shortcuts
        add_card("⌨️ 4. Navigation & Shortcuts", ACCENT_AMBER, [
            ("◀ / ▶ or Spinbox: ", "Navigate freely across all 365 days of the curriculum."),
            ("Ctrl + 1 to 7: ", "Switch directly between the 7 workspace tabs (Document, Math, Code, Canvas, Console, Tutor, Test)."),
            ("Ctrl + G / Ctrl + K: ", "Configure or test your Google Gemini API key."),
            ("F1 / Ctrl + H: ", "Open this About PracticAI Studio modal at any time."),
            ("Interactive Links: ", "Click any day-XXX, math.md, script.py, or syllabus link in the document viewer to navigate immediately."),
            ("Learned vs Syllabus: ", "Toggle between your implemented code in learned/ and the master syllabus plan in lessons/.")
        ])

        # Section 5: Privacy
        add_card("🔒 5. Privacy & Local Storage", "#ec4899", [
            ("100% Local: ", "Your API key is stored locally in .aviation_config.json. Stars and completions are saved in .aviation_progress.json. Zero telemetry.")
        ])

        # 4. Bottom Action Bar
        bottom = tk.Frame(dialog, bg=BG_PANEL, height=45)
        bottom.pack(fill="x", side="bottom")

        btn_close = tk.Button(bottom, text="Close", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=ACCENT_CYAN,
                              activebackground="#0891b2", bd=0, padx=16, pady=5, cursor="hand2", command=dialog.destroy)
        btn_close.pack(side="right", padx=16, pady=8)

    # =========================================================================
    # PERSONALISATION MODAL & LEARNING STYLE DIAGNOSTIC TEST
    # =========================================================================

    def _open_personalisation_dialog(self):
        """Displays the Personalisation Modal featuring Learning Style, AI Tutor Insights, and Directives."""
        dialog = tk.Toplevel(self)
        dialog.title("🎓 Student Personalisation & AI Profile")
        dialog.geometry("820x680")
        dialog.minsize(740, 560)
        dialog.configure(bg=BG_PANEL)
        dialog.transient(self)
        dialog.grab_set()

        # Center on parent
        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 410
            y = self.winfo_y() + (self.winfo_height() // 2) - 340
            dialog.geometry(f"820x680+{max(30, x)}+{max(30, y)}")
        except Exception:
            pass

        # 1. Header Banner
        header = tk.Frame(dialog, bg="#1e293b", height=60, bd=0, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        header.pack(fill="x")

        hdr_left = tk.Frame(header, bg="#1e293b")
        hdr_left.pack(side="left", padx=20, pady=10)

        tk.Label(hdr_left, text="🎓 Student Personalisation & AI Profile", font=("Segoe UI", 12, "bold"),
                 fg="#ffffff", bg="#1e293b").pack(anchor="w")
        tk.Label(hdr_left, text="Diagnose your learning archetype, review accumulated AI Tutor enquiry insights, and tune your pedagogy.",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w")

        prof = self.student_profile
        cur_archetype = prof.get("archetype", "🛠️ Hands-On Systems Builder")
        lbl_top_badge = tk.Label(header, text=cur_archetype, font=("Segoe UI", 9, "bold"),
                                 fg="#ffffff", bg="#4f46e5", padx=10, pady=4, bd=0)
        lbl_top_badge.pack(side="right", padx=20, pady=12)

        # 2. Main Notebook Tabs
        p_notebook = ttk.Notebook(dialog)
        p_notebook.pack(fill="both", expand=True, padx=16, pady=12)

        tab_style = tk.Frame(p_notebook, bg=BG_PANEL)
        p_notebook.add(tab_style, text="  🧠 Learning Style & Test  ")

        tab_insights = tk.Frame(p_notebook, bg=BG_PANEL)
        p_notebook.add(tab_insights, text="  🤖 AI Tutor Insights  ")

        tab_prefs = tk.Frame(p_notebook, bg=BG_PANEL)
        p_notebook.add(tab_prefs, text="  ⚙️ Tutor Preferences  ")

        # ---------------------------------------------------------------------
        # TAB 1: LEARNING STYLE & DIAGNOSTIC TEST
        # ---------------------------------------------------------------------
        def _render_tab_style():
            for child in tab_style.winfo_children():
                child.destroy()

            cur_p = self.student_profile
            arch_title = cur_p.get("archetype", "🛠️ Hands-On Systems Builder")
            arch_desc = cur_p.get("archetype_desc", "")
            scores = cur_p.get("scores", {
                "code_vs_theory": 80,
                "systems_vs_primitives": 75,
                "visual_vs_verbal": 70,
                "pace_and_density": 85
            })

            # Top Archetype Card
            arch_card = tk.Frame(tab_style, bg="#1e293b", bd=1, relief="solid", highlightthickness=1, highlightbackground="#4f46e5")
            arch_card.pack(fill="x", padx=12, pady=(12, 10))

            card_hdr = tk.Frame(arch_card, bg="#1e293b")
            card_hdr.pack(fill="x", padx=16, pady=(12, 4))

            tk.Label(card_hdr, text=arch_title, font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg="#1e293b").pack(side="left")
            tk.Label(card_hdr, text="ACTIVE LEARNING ARCHETYPE", font=("Segoe UI", 7, "bold"),
                     fg="#ffffff", bg="#4f46e5", padx=8, pady=2).pack(side="right")

            tk.Label(arch_card, text=arch_desc, font=("Segoe UI", 9), fg=TEXT_MAIN, bg="#1e293b",
                     wraplength=720, justify="left").pack(anchor="w", padx=16, pady=(2, 14))

            # Dimension Meters Section
            meters_frame = tk.Frame(tab_style, bg=BG_PANEL)
            meters_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

            tk.Label(meters_frame, text="Cognitive Preference Dimensions", font=("Segoe UI", 10, "bold"),
                     fg="#ffffff", bg=BG_PANEL).pack(anchor="w", pady=(0, 8))

            dimensions = [
                ("Code vs Theory", scores.get("code_vs_theory", 80), "Pure Theory & Proofs", "Hands-On Working Code", ACCENT_CYAN),
                ("Systems vs Primitives", scores.get("systems_vs_primitives", 75), "Mathematical Primitives", "End-to-End System Pipelines", ACCENT_EMERALD),
                ("Visual vs Verbal", scores.get("visual_vs_verbal", 70), "Verbal & Structured Text", "Visual Topologies & Diagrams", ACCENT_PURPLE),
                ("Pacing & Density", scores.get("pace_and_density", 85), "Gradual & Introductory", "High-Density & Rigorous", ACCENT_AMBER)
            ]

            for dim_name, val, left_lbl, right_lbl, bar_color in dimensions:
                row = tk.Frame(meters_frame, bg="#1e293b", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER_BRIGHT)
                row.pack(fill="x", pady=4)

                top_r = tk.Frame(row, bg="#1e293b")
                top_r.pack(fill="x", padx=14, pady=(8, 2))
                tk.Label(top_r, text=dim_name, font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#1e293b").pack(side="left")
                tk.Label(top_r, text=f"{val}%", font=("Segoe UI", 9, "bold"), fg=bar_color, bg="#1e293b").pack(side="right")

                # Visual meter bar
                c_meter = tk.Canvas(row, height=12, bg=BG_CODE, highlightthickness=0)
                c_meter.pack(fill="x", padx=14, pady=4)

                def _draw_bar(canvas=c_meter, score=val, color=bar_color):
                    canvas.update_idletasks()
                    w = canvas.winfo_width()
                    if w <= 1: w = 700
                    fill_w = max(4, int(w * (score / 100.0)))
                    canvas.create_rectangle(0, 0, fill_w, 12, fill=color, outline="")

                c_meter.bind("<Configure>", lambda e, c=c_meter, s=val, col=bar_color: _draw_bar(c, s, col))
                row.after(20, lambda c=c_meter, s=val, col=bar_color: _draw_bar(c, s, col))

                bot_r = tk.Frame(row, bg="#1e293b")
                bot_r.pack(fill="x", padx=14, pady=(2, 8))
                tk.Label(bot_r, text=f"◀ {left_lbl}", font=("Segoe UI", 7), fg=TEXT_MUTED, bg="#1e293b").pack(side="left")
                tk.Label(bot_r, text=f"{right_lbl} ▶", font=("Segoe UI", 7), fg=TEXT_MUTED, bg="#1e293b").pack(side="right")

            # Diagnostic Action Bar
            action_row = tk.Frame(tab_style, bg=BG_PANEL)
            action_row.pack(fill="x", padx=12, pady=10)

            btn_test = tk.Button(action_row, text="🎯 Take / Retake Learning Style Test", font=("Segoe UI", 10, "bold"),
                                 fg="#ffffff", bg=ACCENT_CYAN, activebackground="#0891b2", bd=0, padx=16, pady=8,
                                 cursor="hand2", command=lambda: self._open_learning_style_test(dialog))
            btn_test.pack(side="left")

            tk.Label(action_row, text="Takes 2 minutes · 6 targeted cognitive diagnostic questions",
                     font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=14)

        _render_tab_style()

        # ---------------------------------------------------------------------
        # TAB 2: AI TUTOR INSIGHTS & INQUIRIES
        # ---------------------------------------------------------------------
        def _render_tab_insights():
            for child in tab_insights.winfo_children():
                child.destroy()

            t_insights = self.student_profile.get("tutor_insights", {})
            summary = t_insights.get("summary", "No custom inquiries logged yet. Ask questions in the AI Tutor to build live insights.")
            frequent_topics = t_insights.get("frequent_topics", ["First Principles", "Architecture", "Runtime Invariants"])
            inquiries = t_insights.get("inquiries", [])

            # Synthesis Observation Card
            synth_card = tk.Frame(tab_insights, bg="#1e293b", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER_BRIGHT)
            synth_card.pack(fill="x", padx=12, pady=(12, 10))

            tk.Label(synth_card, text="🧠 AI Tutor Observation Summary", font=("Segoe UI", 10, "bold"),
                     fg=ACCENT_EMERALD, bg="#1e293b").pack(anchor="w", padx=16, pady=(10, 4))
            tk.Label(synth_card, text=summary, font=("Segoe UI", 9), fg=TEXT_MAIN, bg="#1e293b",
                     wraplength=730, justify="left").pack(anchor="w", padx=16, pady=(0, 8))

            # Frequent Question Themes
            tk.Label(synth_card, text="Observed Question Themes:", font=("Segoe UI", 8, "bold"),
                     fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w", padx=16, pady=(0, 4))

            badges_row = tk.Frame(synth_card, bg="#1e293b")
            badges_row.pack(fill="x", padx=16, pady=(0, 12))

            for topic in frequent_topics:
                tk.Label(badges_row, text=f"• {topic}", font=("Segoe UI", 8, "bold"),
                         fg="#38bdf8", bg=BG_CODE, padx=8, pady=3, bd=1, relief="solid").pack(side="left", padx=(0, 6))

            # Inquiries Log Section
            inq_header = tk.Frame(tab_insights, bg=BG_PANEL)
            inq_header.pack(fill="x", padx=12, pady=(6, 4))
            tk.Label(inq_header, text=f"Recorded Custom Inquiries ({len(inquiries)})", font=("Segoe UI", 10, "bold"),
                     fg="#ffffff", bg=BG_PANEL).pack(side="left")
            tk.Label(inq_header, text="Collected automatically from non-quick-prompt questions typed in chat",
                     font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=12)

            # Inquiries Treeview
            tree_container = tk.Frame(tab_insights, bg=BG_PANEL)
            tree_container.pack(fill="both", expand=True, padx=12, pady=(0, 10))

            tree_scroll = ttk.Scrollbar(tree_container)
            tree_scroll.pack(side="right", fill="y")

            inq_tree = ttk.Treeview(tree_container, columns=("day", "time", "cat", "query"),
                                    show="headings", selectmode="browse", yscrollcommand=tree_scroll.set)
            inq_tree.pack(side="left", fill="both", expand=True)
            tree_scroll.config(command=inq_tree.yview)

            inq_tree.heading("day", text="Day")
            inq_tree.heading("time", text="Time")
            inq_tree.heading("cat", text="Domain / Topic")
            inq_tree.heading("query", text="Student Inquiry Snippet")

            inq_tree.column("day", width=60, anchor="center")
            inq_tree.column("time", width=120, anchor="center")
            inq_tree.column("cat", width=180, anchor="w")
            inq_tree.column("query", width=360, anchor="w")

            if inquiries:
                for item in reversed(inquiries):
                    inq_tree.insert("", "end", values=(
                        f"Day {item.get('day', 1):03d}",
                        item.get("timestamp", ""),
                        item.get("category", "General"),
                        item.get("query", "")
                    ))
            else:
                inq_tree.insert("", "end", values=("-", "-", "No custom inquiries", "Type questions in the AI Tutor chat to see your enquiry patterns appear here!"))

            # Bottom Actions
            btn_row = tk.Frame(tab_insights, bg=BG_PANEL)
            btn_row.pack(fill="x", padx=12, pady=(0, 10))

            def _clear_history():
                if messagebox.askyesno("Clear Inquiries", "Reset inquiry logs and start fresh?"):
                    self.student_profile["tutor_insights"]["inquiries"] = []
                    self.student_profile["tutor_insights"]["summary"] = "Inquiry logs reset. Tutor will recalibrate from future questions."
                    self.student_profile["tutor_insights"]["frequent_topics"] = ["First Principles", "Architecture", "Runtime Invariants"]
                    self._save_student_profile()
                    _render_tab_insights()

            btn_clear = tk.Button(btn_row, text="🧹 Clear Inquiry History", font=("Segoe UI", 9),
                                  fg=TEXT_MUTED, bg="#1e293b", activebackground="#334155", bd=0, padx=12, pady=5,
                                  cursor="hand2", command=_clear_history)
            btn_clear.pack(side="left")

        _render_tab_insights()

        # ---------------------------------------------------------------------
        # TAB 3: TUTOR DIRECTIVES & PREFERENCES
        # ---------------------------------------------------------------------
        def _render_tab_prefs():
            for child in tab_prefs.winfo_children():
                child.destroy()

            cur_p = self.student_profile
            prefs = cur_p.get("preferences", {})

            card = tk.Frame(tab_prefs, bg="#1e293b", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER_BRIGHT)
            card.pack(fill="both", expand=True, padx=12, pady=12)

            tk.Label(card, text="Pedagogical Directives & Instruction Tuning", font=("Segoe UI", 10, "bold"),
                     fg="#ffffff", bg="#1e293b").pack(anchor="w", padx=18, pady=(14, 2))
            tk.Label(card, text="Customize how the AI Tutor formats explanations, approaches math, and delivers code.",
                     font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w", padx=18, pady=(0, 14))

            # Student Name
            tk.Label(card, text="Learner Display Name:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b").pack(anchor="w", padx=18)
            entry_name = tk.Entry(card, font=("Segoe UI", 9), bg=BG_CODE, fg="#ffffff", insertbackground=ACCENT_CYAN, bd=1, relief="solid")
            entry_name.pack(fill="x", padx=18, pady=(4, 12))
            entry_name.insert(0, cur_p.get("student_name", "Aviation 365 Student"))

            # Explanation Depth
            tk.Label(card, text="Explanation Depth & Pacing:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b").pack(anchor="w", padx=18)
            combo_depth = ttk.Combobox(card, values=[
                "Balanced Intuition + Mechanics",
                "Concise & Fast (Direct answers, high density)",
                "Deep First-Principles (Comprehensive walkthroughs with analogies)"
            ], state="readonly", font=("Segoe UI", 9))
            cur_depth = prefs.get("explanation_depth", "Balanced Intuition + Mechanics")
            combo_depth.set(cur_depth if cur_depth in combo_depth["values"] else combo_depth["values"][0])
            combo_depth.pack(fill="x", padx=18, pady=(4, 12))

            # Math Rigor
            tk.Label(card, text="Mathematical Walkthrough Style:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b").pack(anchor="w", padx=18)
            combo_math = ttk.Combobox(card, values=[
                "Plain-English Intuitive Translation (Explain ideas in plain words, trace numbers)",
                "Code-First Numeric (Translate math directly into Python arrays and tensor shapes)",
                "Rigorous Formalism (Show calculus derivations and LaTeX equations)"
            ], state="readonly", font=("Segoe UI", 9))
            cur_math = prefs.get("math_rigor", "Plain-English Intuitive Translation")
            match_math = next((v for v in combo_math["values"] if cur_math in v), combo_math["values"][0])
            combo_math.set(match_math)
            combo_math.pack(fill="x", padx=18, pady=(4, 12))

            # Code Style
            tk.Label(card, text="Code Generation Preference:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#1e293b").pack(anchor="w", padx=18)
            combo_code = ttk.Combobox(card, values=[
                "Production-grade, annotated with intermediate printouts",
                "Minimal standard library first (zero external dependencies)",
                "Educational with step-by-step assert guards and trace mechanics"
            ], state="readonly", font=("Segoe UI", 9))
            cur_code = prefs.get("code_style", "Production-grade, annotated with intermediate printouts")
            combo_code.set(cur_code if cur_code in combo_code["values"] else combo_code["values"][0])
            combo_code.pack(fill="x", padx=18, pady=(4, 12))

            # Custom Directives
            tk.Label(card, text="Custom Directives to AI Tutor (Injected into every lesson prompt):", font=("Segoe UI", 9, "bold"),
                     fg=ACCENT_CYAN, bg="#1e293b").pack(anchor="w", padx=18)
            txt_custom = tk.Text(card, height=4, font=("Segoe UI", 9), bg=BG_CODE, fg="#ffffff",
                                 insertbackground=ACCENT_CYAN, padx=10, pady=6, wrap="word", bd=1, relief="solid")
            txt_custom.pack(fill="x", padx=18, pady=(4, 14))
            txt_custom.insert("1.0", prefs.get("custom_directives", ""))

            # Save Button
            def _save_prefs():
                cur_p["student_name"] = entry_name.get().strip() or "Aviation 365 Student"
                cur_p["preferences"]["explanation_depth"] = combo_depth.get().split("(")[0].strip()
                cur_p["preferences"]["math_rigor"] = combo_math.get().split("(")[0].strip()
                cur_p["preferences"]["code_style"] = combo_code.get().strip()
                cur_p["preferences"]["custom_directives"] = txt_custom.get("1.0", "end").strip()
                self._save_student_profile()
                # Clear active chat instances so next prompt picks up updated master instruction
                self.gemini_chats.clear()
                messagebox.showinfo("Profile Updated", "Your personalisation preferences and directives have been saved!")

            btn_save = tk.Button(card, text="💾 Save & Apply Profile", font=("Segoe UI", 9, "bold"),
                                 fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", bd=0, padx=16, pady=6,
                                 cursor="hand2", command=_save_prefs)
            btn_save.pack(anchor="w", padx=18, pady=(0, 14))

        _render_tab_prefs()

        # 3. Bottom Close Button
        bottom_bar = tk.Frame(dialog, bg=BG_PANEL, height=45)
        bottom_bar.pack(fill="x", side="bottom")

        btn_close = tk.Button(bottom_bar, text="Close", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=ACCENT_CYAN,
                              activebackground="#0891b2", bd=0, padx=16, pady=5, cursor="hand2", command=dialog.destroy)
        btn_close.pack(side="right", padx=16, pady=8)

        # Allow tab refresh from sub-dialogs
        dialog.refresh_style_tab = _render_tab_style
        dialog.refresh_insights_tab = _render_tab_insights

    def _open_learning_style_test(self, parent_dialog=None):
        """Displays the interactive 6-question Learning Style Diagnostic Assessment."""
        test_win = tk.Toplevel(self)
        test_win.title("🎯 PracticAI Learning Style Assessment")
        test_win.geometry("840x720")
        test_win.minsize(760, 580)
        test_win.configure(bg=BG_PANEL)
        test_win.transient(self)
        test_win.grab_set()

        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 420
            y = self.winfo_y() + (self.winfo_height() // 2) - 360
            test_win.geometry(f"840x720+{max(20, x)}+{max(20, y)}")
        except Exception:
            pass

        # Header
        top_bar = tk.Frame(test_win, bg="#1e293b", height=60, bd=0, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        top_bar.pack(fill="x")

        hdr_f = tk.Frame(top_bar, bg="#1e293b")
        hdr_f.pack(side="left", padx=20, pady=10)

        tk.Label(hdr_f, text="🎯 Learning Style Diagnostic Assessment", font=("Segoe UI", 12, "bold"),
                 fg="#ffffff", bg="#1e293b").pack(anchor="w")
        tk.Label(hdr_f, text="Answer these 6 cognitive questions to discover your AI engineering archetype and tune the AI Tutor.",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w")

        # Scrollable questions container
        container = tk.Frame(test_win, bg=BG_PANEL)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        q_canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        q_scroll = ttk.Scrollbar(container, orient="vertical", command=q_canvas.yview)
        scrollable_q_frame = tk.Frame(q_canvas, bg=BG_PANEL)

        scrollable_q_frame.bind(
            "<Configure>",
            lambda e: q_canvas.configure(scrollregion=q_canvas.bbox("all"))
        )
        canvas_win = q_canvas.create_window((0, 0), window=scrollable_q_frame, anchor="nw")
        q_canvas.configure(yscrollcommand=q_scroll.set)

        q_canvas.bind(
            "<Configure>",
            lambda e: q_canvas.itemconfig(canvas_win, width=max(600, e.width - 24))
        )

        q_canvas.pack(side="left", fill="both", expand=True)
        q_scroll.pack(side="right", fill="y")

        # Questions Definition
        questions = [
            {
                "id": "q1",
                "title": "Question 1 · Initial Approach to New Aviation Concepts",
                "q": "When encountering a brand-new aviation concept (e.g. A-CDM turnaround milestones or EASA Part-CAT fuel schemes), what is your instinctive first step?",
                "options": {
                    "A": "Trace a concrete operational flight scenario from gate to gate with realistic inputs and milestones.",
                    "B": "Study the regulatory baseline (ICAO Annexes, EASA AMC/GM, or FAA FARs) from first principles.",
                    "C": "Sketch the ecosystem interaction diagram showing stakeholder dependencies and information flows.",
                    "D": "Examine a real accident, incident report, or operational failure where this mechanism broke down."
                }
            },
            {
                "id": "q2",
                "title": "Question 2 · Internalizing Multi-Step Aviation Workflows",
                "q": "How do you best internalize multi-step processes (e.g. pre-flight weight & balance, slot allocation, or wake turbulence separation)?",
                "options": {
                    "A": "Trace a concrete worked calculation step-by-step with real aircraft weights, speeds, or fuel numbers.",
                    "B": "Inspect a high-level system topology diagram tracking sequence milestones and interfaces.",
                    "C": "Review the statutory rulebook, certification specifications, and operator SOP checklists.",
                    "D": "Follow a cockpit or flight dispatch operational decision tree in a simulated scenario."
                }
            },
            {
                "id": "q3",
                "title": "Question 3 · Overcoming Conceptual Confusion",
                "q": "When a complex aviation topic leaves you stuck, what helps you break through the bottleneck fastest?",
                "options": {
                    "A": "An interactive Python simulation allowing you to test variables and observe the outcome.",
                    "B": "A plain-English breakdown explaining the operational trade-offs and physical rationale.",
                    "C": "A clear visual flow diagram isolating the exact entity or threshold that restricts the operation.",
                    "D": "An adversarial 'Break-It' scenario showing where the naive assumption causes an incident or grounding."
                }
            },
            {
                "id": "q4",
                "title": "Question 4 · Quantitative Analysis & Flight Physics Relationship",
                "q": "What is your preferred relationship with mathematical formulas and quantitative metrics in aviation?",
                "options": {
                    "A": "Plain-English operational intuition first: explain what the numbers physically mean, then trace real data.",
                    "B": "Operational dispatch bounds: show me limits, tables, density altitude effects, and safety buffers.",
                    "C": "Rigorous flight physics: full aerodynamic lift/drag, thermodynamics, and navigational geometry equations.",
                    "D": "Practical flight rules of thumb and operational heuristics (e.g. 3:1 descent rule, 1-in-60 rule)."
                }
            },
            {
                "id": "q5",
                "title": "Question 5 · Professional Background & Primary Perspective",
                "q": "Which best describes your background, primary lens, or area of greatest interest in aviation?",
                "options": {
                    "A": "Flight Operations & Dispatch: focused on airline OCC, flight planning, crew FTL, and operational control.",
                    "B": "Aerospace Engineering & Maintenance: focused on aircraft systems, aerodynamics, engines, and Part-M/145 airworthiness.",
                    "C": "Air Traffic Management & Aerodromes: focused on airspace design, ATC separation, runway capacity, and A-CDM.",
                    "D": "Aviation Economics, Law & Strategy: focused on airline commercial models, bilateral treaties, and ICAO/EASA regulation."
                }
            },
            {
                "id": "q6",
                "title": "Question 6 · Daily Experiment Workflow Preference",
                "q": "When running an interactive daily Python experiment, what is your natural priority?",
                "options": {
                    "A": "Simulate the flight or turnaround scenario immediately, tweaking inputs to see operational results.",
                    "B": "Study the underlying decision logic, regulatory constraints, and algorithmic validation rules.",
                    "C": "Formulate stress-test edge cases (convective weather, slot delays, MEL items) to push the system to failure.",
                    "D": "Analyze operational margins, cost trade-offs, and fleet efficiency metrics."
                }
            }
        ]

        answers = {}
        for q in questions:
            var = tk.StringVar(value="")
            answers[q["id"]] = var

            card = tk.Frame(scrollable_q_frame, bg="#1e293b", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER_BRIGHT)
            card.pack(fill="x", pady=6, padx=6)

            tk.Label(card, text=q["title"], font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg="#1e293b").pack(anchor="w", padx=16, pady=(10, 4))
            tk.Label(card, text=q["q"], font=("Segoe UI", 9), fg="#ffffff", bg="#1e293b", wraplength=760, justify="left").pack(anchor="w", padx=16, pady=(0, 8))

            for opt_key, opt_text in q["options"].items():
                rb = tk.Radiobutton(card, text=f"{opt_key}. {opt_text}", variable=var, value=opt_key,
                                    font=("Segoe UI", 9), fg="#cbd5e1", bg="#1e293b", selectcolor=BG_CODE,
                                    activebackground="#1e293b", activeforeground="#ffffff", wraplength=740, justify="left")
                rb.pack(anchor="w", padx=22, pady=3)

            tk.Frame(card, bg="#1e293b", height=8).pack()

        # Submit Action Bar
        action_bar = tk.Frame(test_win, bg=BG_PANEL, height=55)
        action_bar.pack(fill="x", side="bottom", padx=16, pady=10)

        def _calculate_and_submit():
            unanswered = [q["id"] for q in questions if not answers[q["id"]].get()]
            if unanswered:
                messagebox.showwarning("Incomplete", f"Please answer all 6 questions before submitting ({len(unanswered)} remaining).")
                return

            ans_map = {q_id: v.get() for q_id, v in answers.items()}

            # Scoring algorithm
            # Dimensions: code_score, systems_score, visual_score, density_score
            c_score = 0
            s_score = 0
            v_score = 0
            d_score = 0

            # Q1
            if ans_map["q1"] == "A": c_score += 25; s_score += 15
            elif ans_map["q1"] == "B": c_score += 5; s_score += 5; d_score += 15
            elif ans_map["q1"] == "C": v_score += 25; s_score += 15
            elif ans_map["q1"] == "D": s_score += 20; c_score += 10

            # Q2
            if ans_map["q2"] == "A": c_score += 25; d_score += 10
            elif ans_map["q2"] == "B": v_score += 25; s_score += 15
            elif ans_map["q2"] == "C": c_score += 5; d_score += 20
            elif ans_map["q2"] == "D": s_score += 15; v_score += 10

            # Q3
            if ans_map["q3"] == "A": c_score += 25; d_score += 10
            elif ans_map["q3"] == "B": s_score += 15; c_score += 10
            elif ans_map["q3"] == "C": v_score += 25; s_score += 15
            elif ans_map["q3"] == "D": s_score += 20; c_score += 20

            # Q4
            if ans_map["q4"] == "A": c_score += 15; s_score += 15
            elif ans_map["q4"] == "B": s_score += 25; c_score += 15; d_score += 15
            elif ans_map["q4"] == "C": c_score += 5; d_score += 25
            elif ans_map["q4"] == "D": c_score += 25; s_score += 10

            # Q5
            if ans_map["q5"] == "A": s_score += 25; d_score += 15; c_score += 15
            elif ans_map["q5"] == "B": s_score += 15; c_score += 15
            elif ans_map["q5"] == "C": d_score += 15; c_score += 10
            elif ans_map["q5"] == "D": c_score += 25; d_score += 25; s_score += 15

            # Q6
            if ans_map["q6"] == "A": c_score += 20; d_score += 10
            elif ans_map["q6"] == "B": s_score += 25; v_score += 10
            elif ans_map["q6"] == "C": s_score += 20; c_score += 15
            elif ans_map["q6"] == "D": d_score += 25; c_score += 15

            # Normalize to 0-100 scales
            code_vs_theory = min(100, max(20, int((c_score / 125.0) * 100)))
            systems_vs_primitives = min(100, max(20, int((s_score / 120.0) * 100)))
            visual_vs_verbal = min(100, max(20, int((v_score / 75.0) * 100)))
            pace_and_density = min(100, max(20, int((d_score / 100.0) * 100)))

                        # Archetype mapping tailored for Aviation 365
            if code_vs_theory >= 65 and systems_vs_primitives >= 60:
                archetype = "✈️ Airline Operations & Dispatch Specialist"
                desc = "Prefers operational flight planning, fuel policy calculations, payload-range trade-offs, and resolving schedule disruptions over abstract theoretical models."
            elif code_vs_theory <= 45:
                archetype = "📐 Aeronautical Engineer & Flight Physicist"
                desc = "Internalizes concepts through aerodynamic equations, flight mechanics, propulsion thermodynamics, and structural certification criteria."
            elif visual_vs_verbal >= 65 and systems_vs_primitives >= 55:
                archetype = "🌐 ATM & Airspace Systems Architect"
                desc = "Thinks in 4D trajectory negotiations, radar separation standards, airspace capacity modeling, and collaborative network management (A-CDM)."
            elif pace_and_density >= 70:
                archetype = "🛡️ Safety, SMS & Regulatory Investigator"
                desc = "Thrives on ICAO Annexes, EASA rule traceability, accident case studies, Bow-Tie barrier analysis, and human factors error management."
            else:
                archetype = "🛫 Airport & Ground Handling Manager"
                desc = "Focuses on airside movement dynamics, turnaround critical paths, slot allocation, terminal passenger flow, and airport infrastructure design."

            # Update profile
            self.student_profile["archetype"] = archetype
            self.student_profile["archetype_desc"] = desc
            self.student_profile["scores"] = {
                "code_vs_theory": code_vs_theory,
                "systems_vs_primitives": systems_vs_primitives,
                "visual_vs_verbal": visual_vs_verbal,
                "pace_and_density": pace_and_density
            }
            self._save_student_profile()
            self.gemini_chats.clear() # Reset chat instances to inject updated style

            test_win.destroy()

            # Refresh parent dialog tabs if open
            if parent_dialog and hasattr(parent_dialog, "refresh_style_tab"):
                try:
                    parent_dialog.refresh_style_tab()
                except Exception:
                    pass

            messagebox.showinfo("Archetype Diagnosed!",
                                f"Congratulations! Your diagnosed learning archetype is:\n\n"
                                f"{archetype}\n\n"
                                f"{desc}\n\n"
                                f"Scores:\n"
                                f"• Code vs Theory: {code_vs_theory}%\n"
                                f"• Systems vs Primitives: {systems_vs_primitives}%\n"
                                f"• Visual vs Verbal: {visual_vs_verbal}%\n"
                                f"• Pacing & Density: {pace_and_density}%\n\n"
                                f"The AI Tutor has been automatically updated to calibrate all future lesson answers to this profile!")

        btn_submit = tk.Button(action_bar, text="✨ Submit & Calculate My Learning Style", font=("Segoe UI", 10, "bold"),
                               fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", bd=0, padx=20, pady=8,
                               cursor="hand2", command=_calculate_and_submit)
        btn_submit.pack(side="left")

        btn_cancel = tk.Button(action_bar, text="Cancel", font=("Segoe UI", 9),
                               fg=TEXT_MUTED, bg="#1e293b", activebackground="#334155", bd=0, padx=14, pady=8,
                               cursor="hand2", command=test_win.destroy)
        btn_cancel.pack(side="right")

    def _build_curriculum_catalog(self):
        """Indexes all 365 daily lessons for fast pedagogical context construction."""
        self.curriculum_catalog.clear()
        if not LESSONS_DIR.exists():
            return
        for f in LESSONS_DIR.glob("week-*/day-*.md"):
            try:
                d_num = int(f.stem.split("-")[1])
                txt = f.read_text(encoding="utf-8", errors="ignore")
                tm = re.search(r'title:\s*"([^"]+)"', txt)
                thm = re.search(r'theme:\s*"?([^\n\r"]+)"?', txt)
                lm = re.search(r'level_title:\s*"([^"]+)"', txt)
                w_num = ((d_num - 1) // 7) + 1
                if w_num > 52: w_num = 52
                self.curriculum_catalog[d_num] = {
                    "title": tm.group(1) if tm else f.stem,
                    "theme": thm.group(1) if thm else "",
                    "level": lm.group(1) if lm else "",
                    "week": w_num
                }
            except Exception:
                pass

    def _build_gemini_pedagogical_context(self, target_day: int) -> str:
        """
        Constructs a strict pedagogical system prompt for Day target_day:
        1. Summarizes all curriculum concepts mastered from Day 1 to target_day - 1.
        2. Injects current Day target_day topic, mental model, math derivation, and architecture diagram.
        3. Enforces the strict pedagogical boundary that Days target_day + 1 to 365 are locked and unknown.
        4. Mandates adherence to the 6 PracticAI Experiment Rules for generated code.
        """
        w_num = ((target_day - 1) // 7) + 1
        if w_num > 52: w_num = 52

        # Current Day Artifacts
        readme_text = ""
        math_text = ""
        mermaid_text = ""
        py_text = ""
        target_name = f"day-{target_day:03d}"

        learned_day_dir = None
        for p in LEARNED_DIR.glob(f"**/{target_name}"):
            if p.is_dir():
                learned_day_dir = p
                break

        if learned_day_dir:
            rf = learned_day_dir / "README.md"
            if rf.exists():
                readme_text = rf.read_text(encoding="utf-8", errors="replace")
            mf_math = learned_day_dir / "math.md"
            if mf_math.exists():
                math_text = mf_math.read_text(encoding="utf-8", errors="replace")
            mf = learned_day_dir / "architecture.mermaid"
            if mf.exists():
                mermaid_text = mf.read_text(encoding="utf-8", errors="replace")
            pf = learned_day_dir / "experiment.py"
            if pf.exists():
                py_text = pf.read_text(encoding="utf-8", errors="replace")
        else:
            lf = LESSONS_DIR / f"week-{w_num:02d}" / f"day-{target_day:03d}.md"
            if lf.exists():
                readme_text = lf.read_text(encoding="utf-8", errors="replace")

        # Mastered curriculum progression up to target_day - 1
        mastered_list = []
        if target_day > 1:
            start_recent = max(1, target_day - 7)
            if start_recent > 1:
                mastered_list.append(f"• Days 001 to {start_recent - 1:03d}: Foundational concepts, baseline architectures, and mathematical paradigms mastered.")
            for d in range(start_recent, target_day):
                info = self.curriculum_catalog.get(d)
                if info:
                    mastered_list.append(f"• Day {d:03d} [{info['theme']}]: {info['title']} (Domain: {info['level']})")
                else:
                    mastered_list.append(f"• Day {d:03d}: Mastered prior lesson.")

        current_info = self.curriculum_catalog.get(target_day, {})
        day_title = current_info.get("title", f"Day {target_day:03d}")
        day_theme = current_info.get("theme", "Build")
        day_level = current_info.get("level", "Foundations")

        # Personalised Student Profile & Insights
        prof = self.student_profile
        student_name = prof.get("student_name", "Student")
        style = prof.get("archetype", "🛠️ Hands-On Systems Builder")
        style_desc = prof.get("archetype_desc", "")
        scores = prof.get("scores", {})
        prefs = prof.get("preferences", {})
        insights = prof.get("tutor_insights", {})
        summary = insights.get("summary", "Student engages actively with hands-on examples.")
        frequent_topics = ", ".join(insights.get("frequent_topics", []))
        custom_directives = prefs.get("custom_directives", "")

        system_instruction = f"""You are the Aviation 365 Pedagogical Mentor and Senior Aviation Systems Expert for Day {target_day:03d} of the 365 Days of Aviation curriculum. You specialize in the complete civil aviation ecosystem: airlines (AOC/OCC), aerodromes (ADR), air navigation service providers (ANSPs/ATM), safety regulators (ICAO Annexes, Regulation (EU) 2018/1139, EASA Easy Access Rules, NAAs), aircraft airworthiness (Part-M/Part-145/Part-21), and Safety Management Systems (SMS).

=== STRICT PEDAGOGICAL BOUNDARY (CRITICAL) ===
- Current Student Level: Day {target_day:03d} (Week {w_num:02d})
- Mastered Knowledge: Concepts and techniques from Day 001 up to Day {target_day - 1:03d}.
- LOCKED FUTURE ZONE: Days {target_day + 1:03d} through 365 are strictly FORBIDDEN from being spoiled, assumed, or required!
  Anchor all explanations, operational procedures, and implementations strictly in what has been developed up to Day {target_day:03d}.

=== CURRICULUM LEARNED SO FAR (DAYS 001 TO {max(0, target_day - 1):03d}) ===
{chr(10).join(mastered_list) if mastered_list else "This is Day 001. The student is starting from first principles with zero assumed aviation system knowledge."}

=== TODAY'S FOCUS: DAY {target_day:03d} ===
Title: {day_title}
Theme: {day_theme}
Domain Level: {day_level}
Week: {w_num:02d}

--- DAY {target_day:03d} CURRICULUM ARTIFACT (Lesson Guide) ---
{readme_text[:2500] if readme_text else "Day topic in syllabus."}

{f"--- OPERATIONAL & TECHNICAL ANALYSIS ---{chr(10)}{math_text[:2500]}" if math_text else ""}
{f"--- ARCHITECTURE & TOPOLOGY (Mermaid) ---{chr(10)}{mermaid_text}" if mermaid_text else ""}
{f"--- CURRENT DAY EXPERIMENT CODE ---{chr(10)}{py_text[:3000]}" if py_text else "Note: experiment.py has not yet been authored for today."}

=== STUDENT PROFILE & TAILORED LEARNING STYLE ===
• Student Name: {student_name}
• Learning Style Archetype: {style}
  Archetype Focus: {style_desc}
• Cognitive Dimensions:
  - Code vs Theory: {scores.get('code_vs_theory', 80)}/100 ({'Prefers working code & operational simulations' if scores.get('code_vs_theory', 80) >= 50 else 'Prefers regulatory and operational theory first'})
  - Systems vs Primitives: {scores.get('systems_vs_primitives', 75)}/100 ({'Focuses on end-to-end ecosystem architecture & flight operations' if scores.get('systems_vs_primitives', 75) >= 50 else 'Focuses on isolated component mechanics'})
  - Visual vs Verbal: {scores.get('visual_vs_verbal', 70)}/100 ({'Prefers diagrams, A-CDM flow layouts, and visual system maps' if scores.get('visual_vs_verbal', 70) >= 50 else 'Prefers written walkthroughs and structured narratives'})
  - Pacing & Density: {scores.get('pace_and_density', 80)}/100
• Pedagogical Preferences:
  - Explanation Depth: {prefs.get('explanation_depth', 'Balanced Intuition + Mechanics')}
  - Analytical Rigor Level: {prefs.get('math_rigor', 'Operational Context + Worked Numerical Examples')}
  - Code Formatting: {prefs.get('code_style', 'Production-grade, annotated with intermediate printouts')}
{f"• Learner Custom Directives: {custom_directives}" if custom_directives else ""}

=== ACCUMULATED TUTOR INSIGHTS ON THIS LEARNER ===
• Inquiry Style Summary: {summary}
• Observed Question Themes: {frequent_topics if frequent_topics else "Aviation system interfaces, flight operations, regulatory compliance"}
• Personalisation Mandate: Actively adapt your explanation pacing, analogies, code depth, and conceptual metaphors to match this student's learning style and historical inquiry tendencies.

=== YOUR ROLES ===
1. Aviation System Explainer: Clarify operational mechanisms, mental models, and real-world implications in plain English at exactly the student's level and tailored to their learning archetype.
2. Operational & Technical Analyst: Explain the quantitative analysis, flight physics, aerodynamics, navigation geometry, or operational metrics in plain language without abstract math for math's sake. Describe what the metrics physically represent in airline, airport, ATM, or regulatory operations, and trace real numbers through worked examples.
3. Aviation Tool Generator: When asked to write or generate Python experiment code for Day {target_day:03d}, produce a complete, runnable, self-contained Python script that directly models and supports today's aviation topic (e.g. flight planning, payload-range, turnaround critical path, slot allocation, economic impact, or regulatory compliance) — never abstract math. Follow the Aviation Experiment Principles:
   Principle 1: Direct Domain Support — model the real-world operational decision or system interface.
   Principle 2: Interactive exploration prompts using prompt_float/prompt_param with realistic operational defaults.
   Principle 3: Transparent intermediate mechanics: print step-by-step intermediate calculations and operational gates ("Show the Working").
   Principle 4: Safety & Adversarial stress test mode: provide an interactive menu option to simulate degrading weather, MEL deferrals, slot delays, or crew timeouts.
   Principle 5: Clean exit & self-contained standard library Python.

=== PLAIN-ENGLISH FIRST DIRECTIVE (CRITICAL) ===
- All explanations MUST be delivered in accessible, intuitive PLAIN ENGLISH.
- When explaining quantitative concepts or calculations:
  • Do NOT invent or dump abstract math for the sake of math.
  • Explain the core operational idea in plain language: what the quantities represent (e.g. payload trade-offs, reserve fuel margins, slot delay costs, braking action friction), why the rules exist, and how the actors coordinate.
  • Format any operational or physical equations using clean LaTeX notation ($inline$ and $$display$$) so the visual studio renders them into graphic formula typography.
"""
        return system_instruction

    def _build_gemini_tab(self, parent):
        """Constructs Tab 5: Interactive Gemini AI Tutor & Pair Programmer."""
        # Top Information Banner
        top_banner = tk.Frame(parent, bg="#1e293b", height=42, highlightthickness=1, highlightbackground=BORDER)
        top_banner.pack(fill="x")

        self.lbl_tutor_day_title = tk.Label(
            top_banner, text="Day 001 · Topic", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1e293b"
        )
        self.lbl_tutor_day_title.pack(side="left", padx=12, pady=8)

        self.lbl_tutor_scope_badge = tk.Label(
            top_banner, text="🔒 Horizon: Days 1–001 (Days 002–365 locked)", font=("Segoe UI", 8, "bold"),
            fg=ACCENT_CYAN, bg="#0f172a", padx=8, pady=3, bd=1, relief="solid"
        )
        self.lbl_tutor_scope_badge.pack(side="left", padx=8, pady=8)

        btn_cfg_key = tk.Button(
            top_banner, text="🔑 Settings", font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg="#0f172a",
            bd=1, relief="solid", cursor="hand2", command=self._open_gemini_key_dialog
        )
        btn_cfg_key.pack(side="right", padx=12, pady=8)

        self.lbl_tutor_model_badge = tk.Label(
            top_banner, text=f"⚡ {self.gemini_model}", font=("Segoe UI", 8, "bold"), fg=ACCENT_EMERALD, bg="#1e293b"
        )
        self.lbl_tutor_model_badge.pack(side="right", padx=6, pady=8)

        # Quick Action Prompt Chips Bar
        chips_bar = tk.Frame(parent, bg="#0f172a", height=38, highlightthickness=1, highlightbackground=BORDER)
        chips_bar.pack(fill="x")

        tk.Label(chips_bar, text="Quick Prompts:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg="#0f172a").pack(side="left", padx=(12, 6), pady=6)

        btn_chip_concept = tk.Button(chips_bar, text="✈️ Explain Concept", font=("Segoe UI", 8), fg=TEXT_MAIN, bg="#1e293b",
                                     bd=1, relief="solid", cursor="hand2", command=self._prompt_explain_concept)
        btn_chip_concept.pack(side="left", padx=3, pady=6)

        btn_chip_math = tk.Button(chips_bar, text="📐 Flight Physics & Math", font=("Segoe UI", 8), fg=TEXT_MAIN, bg="#1e293b",
                                  bd=1, relief="solid", cursor="hand2", command=self._prompt_math_walkthrough)
        btn_chip_math.pack(side="left", padx=3, pady=6)

        btn_chip_code = tk.Button(chips_bar, text="⚡ Generate Aviation Tool", font=("Segoe UI", 8, "bold"), fg="#ffffff", bg=ACCENT_CYAN,
                                  activebackground="#0891b2", bd=0, padx=8, cursor="hand2", command=self._prompt_generate_code)
        btn_chip_code.pack(side="left", padx=5, pady=6)

        self.btn_chip_explain_code = tk.Button(
            chips_bar, text="📖 Explain Aviation Logic in Plain English", font=("Segoe UI", 8, "bold"),
            fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", bd=0, padx=8, pady=2,
            cursor="hand2", command=self._prompt_explain_code
        )
        self.btn_chip_explain_code.pack(side="left", padx=5, pady=6)

        btn_chip_stress = tk.Button(chips_bar, text="🛡️ SMS Hazard & Edge Cases", font=("Segoe UI", 8), fg=TEXT_MAIN, bg="#1e293b",
                                    bd=1, relief="solid", cursor="hand2", command=self._prompt_stress_test)
        btn_chip_stress.pack(side="left", padx=3, pady=6)

        btn_chip_clear = tk.Button(chips_bar, text="🧹 Clear Chat", font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#0f172a",
                                   bd=0, cursor="hand2", command=self._clear_day_chat)
        btn_chip_clear.pack(side="right", padx=12, pady=6)

        # Generated Code Action Bar (hidden by default)
        self.code_action_bar = tk.Frame(parent, bg="#0b1329", height=38, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        self.code_action_bar.pack(fill="x")

        self.lbl_code_action_status = tk.Label(
            self.code_action_bar, text="✨ Python Experiment Code Detected in Gemini Response:",
            font=("Segoe UI", 8, "bold"), fg=ACCENT_EMERALD, bg="#0b1329"
        )
        self.lbl_code_action_status.pack(side="left", padx=12, pady=6)

        self.btn_code_run = tk.Button(
            self.code_action_bar, text="▶ Run in Console", font=("Segoe UI", 8, "bold"), fg="#ffffff", bg=ACCENT_EMERALD,
            activebackground="#059669", bd=0, padx=10, pady=2, cursor="hand2", command=self._on_run_generated_code
        )
        self.btn_code_run.pack(side="right", padx=(4, 12), pady=6)

        self.btn_code_save = tk.Button(
            self.code_action_bar, text="💾 Save to experiment.py", font=("Segoe UI", 8, "bold"), fg="#ffffff", bg="#2563eb",
            activebackground="#1d4ed8", bd=0, padx=10, pady=2, cursor="hand2", command=self._on_save_code_to_experiment
        )
        self.btn_code_save.pack(side="right", padx=4, pady=6)

        self.btn_code_load = tk.Button(
            self.code_action_bar, text="📥 Load into Code Tab", font=("Segoe UI", 8), fg=TEXT_MAIN, bg="#1e293b",
            bd=1, relief="solid", padx=8, pady=2, cursor="hand2", command=self._on_load_code_to_editor
        )
        self.btn_code_load.pack(side="right", padx=4, pady=6)

        self.btn_code_explain = tk.Button(
            self.code_action_bar, text="📖 Explain in Plain English", font=("Segoe UI", 8, "bold"),
            fg="#ffffff", bg="#0891b2", activebackground="#0e7490", bd=0, padx=8, pady=2,
            cursor="hand2", command=self._prompt_explain_code
        )
        self.btn_code_explain.pack(side="right", padx=4, pady=6)

        # Hide initially
        self.code_action_bar.pack_forget()

        # Bottom Input Frame
        input_frame = tk.Frame(parent, bg="#1e293b", height=70, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        input_frame.pack(side="bottom", fill="x")

        self.txt_gemini_input = tk.Text(
            input_frame, height=3, font=("Segoe UI", 9), bg=BG_CODE, fg="#ffffff",
            insertbackground=ACCENT_CYAN, padx=8, pady=6, wrap="word", bd=1, relief="solid"
        )
        self.txt_gemini_input.pack(side="left", fill="both", expand=True, padx=(12, 8), pady=8)
        self.txt_gemini_input.bind("<Return>", self._on_gemini_input_return)

        btn_col = tk.Frame(input_frame, bg="#1e293b")
        btn_col.pack(side="right", padx=(0, 12), pady=8)

        self.btn_gemini_send = tk.Button(
            btn_col, text="Ask Gemini ↵", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=ACCENT_CYAN,
            activebackground="#0891b2", activeforeground="#ffffff", bd=0, padx=14, pady=6,
            cursor="hand2", command=self._send_gemini_prompt
        )
        self.btn_gemini_send.pack(fill="x", pady=(0, 4))

        self.btn_gemini_stop = tk.Button(
            btn_col, text="⏹ Stop", font=("Segoe UI", 8), fg="#ef4444", bg="#0f172a",
            bd=1, relief="solid", state="disabled", command=self._stop_gemini_generation
        )
        self.btn_gemini_stop.pack(fill="x")

        # Scrollable Chat Log
        chat_container = tk.Frame(parent, bg=BG_PANEL)
        chat_container.pack(fill="both", expand=True)

        chat_scroll = ttk.Scrollbar(chat_container)
        chat_scroll.pack(side="right", fill="y")

        self.txt_gemini_chat = tk.Text(
            chat_container, bg=BG_PANEL, fg=TEXT_MAIN, insertbackground=ACCENT_CYAN,
            font=("Segoe UI", 10), padx=24, pady=16, wrap="word", bd=0,
            highlightthickness=0, yscrollcommand=chat_scroll.set
        )
        self.txt_gemini_chat.pack(fill="both", expand=True)
        chat_scroll.config(command=self.txt_gemini_chat.yview)

        # Configure chat formatting tags
        self._configure_markdown_tags(self.txt_gemini_chat)

    def _update_gemini_tab_header(self):
        """Updates the top banner of the AI Tutor tab reflecting the current active day and script status."""
        if not hasattr(self, "lbl_tutor_day_title"):
            return
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")
        self.lbl_tutor_day_title.config(text=f"Day {d:03d} · {title[:48]}")
        self.lbl_tutor_scope_badge.config(text=f"🔒 Horizon: Days 1–{d:03d} (Days {d+1:03d}–365 locked)")
        self._update_gemini_ui_status()

        # Update Explain Code button availability based on whether experiment code is in place
        py_name, py_code = self._get_active_experiment_code()
        if hasattr(self, "btn_chip_explain_code"):
            if py_code:
                short_name = py_name if len(py_name) <= 15 else "Code"
                self.btn_chip_explain_code.config(
                    state="normal",
                    bg=ACCENT_EMERALD,
                    fg="#ffffff",
                    text=f"📖 Explain {short_name} in Plain English"
                )
            else:
                self.btn_chip_explain_code.config(
                    state="disabled",
                    bg="#1e293b",
                    fg=TEXT_MUTED,
                    text="📖 Explain Code (No script yet)"
                )

    def _render_day_chat(self, day_num: int):
        """Renders the chat history for day_num or presents the welcome prompt card."""
        if not hasattr(self, "txt_gemini_chat"):
            return
        self.txt_gemini_chat.delete("1.0", "end")
        history = self.gemini_histories.get(day_num, [])

        if not history:
            info = self.curriculum_catalog.get(day_num, {})
            title = info.get("title", f"Day {day_num:03d}")
            level = info.get("level", "Core Foundations")
            welcome = (
                f"👋 Welcome to Day {day_num:03d} Pedagogical Co-Pilot!\n"
                f"Domain: {level}\n"
                f"Topic: {title}\n\n"
                f"• Mastered Horizon: You have completed all foundational concepts from Days 1 to {max(0, day_num - 1)}.\n"
                f"• Spoiler-Locked Future: Days {day_num + 1} to 365 are locked and will not be spoiled.\n"
                f"• Mission: Explore today's mental model, mathematical derivation, and build the interactive experiment.\n\n"
                f"Click any Quick Prompt above to begin, or ask a question below!\n"
            )
            self.txt_gemini_chat.insert("end", welcome, "sys_card")
            if hasattr(self, "code_action_bar"):
                self.code_action_bar.pack_forget()
            return

        # Render stored history
        has_code = False
        for msg in history:
            role = msg.get("role")
            text = msg.get("text", "")
            if role == "user":
                self.txt_gemini_chat.insert("end", f"👤 You (Day {day_num:03d})\n", "user_hdr")
                self.txt_gemini_chat.insert("end", f"{text}\n\n", "user_body")
            elif role == "ai":
                self.txt_gemini_chat.insert("end", f"🤖 Gemini Tutor (Day {day_num:03d})\n", "ai_hdr")
                self._render_markdown_in_text(text, target_widget=self.txt_gemini_chat, clear=False)
                self.txt_gemini_chat.insert("end", "\n")
                code = self._extract_python_code(text)
                if code:
                    has_code = True
                    self.last_generated_code = code

        if has_code and hasattr(self, "code_action_bar"):
            self.code_action_bar.pack(fill="x", before=self.txt_gemini_chat.master)
            self.lbl_code_action_status.config(text=f"✨ Generated Python Code ({len(self.last_generated_code.splitlines())} lines) - Ready to run!")
        elif hasattr(self, "code_action_bar"):
            self.code_action_bar.pack_forget()

        self.txt_gemini_chat.see("end")

    def _prompt_explain_concept(self):
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")
        prompt = (
            f"Explain the core concept, intuition, and mechanism of Day {d:03d} ({title}) in clear, intuitive plain English, "
            f"using mental models, practical analogies, and step-by-step logic, building strictly upon what we learned in Days 1 to {max(1, d - 1)} "
            f"without assuming later locked days."
        )
        self._send_gemini_prompt(prompt)

    def _prompt_math_walkthrough(self):
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")
        prompt = (
            f"Explain the mathematical idea behind Day {d:03d} ({title}) in plain English. "
            f"Do NOT simply restate or dump the formulas. Instead, explain the core intuition in plain language: "
            f"what the mathematical idea is doing, what the terms physically represent, why the equations work, "
            f"and walk through a concrete numerical example with real numbers. "
            f"Format any math formulas in clean LaTeX ($...$ and $$...$$)."
        )
        self._send_gemini_prompt(prompt)

    def _prompt_generate_code(self):
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")
        prompt = (
            f"Generate a complete, interactive, self-contained Python script for Day {d:03d} ({title}) "
            f"implementing the lesson's experiment. Strictly adhere to the 6 PracticAI Experiment Rules: "
            f"1. Interactive parameter prompts (prompt_param helper with defaults, bounds, casting). "
            f"2. Unbuffered UTF-8 output (sys.stdout.reconfigure(encoding='utf-8', errors='replace')). "
            f"3. Transparent intermediate mechanics ('Show the working' with clear numerical outputs). "
            f"4. Adversarial stress test option in the interactive menu. "
            f"5. Real-time microbenchmark using time.perf_counter(). "
            f"6. Self-contained: standard library first, using only tools mastered up to Day {d:03d}. "
            f"Make it complete, runnable, and output the code in a python code block."
        )
        self._send_gemini_prompt(prompt)

    def _get_active_experiment_code(self) -> tuple[str, str]:
        """Returns (filename, code_text) for the active day's experiment script, or ("", "")."""
        # 1. Check current_files
        for fname, content in self.current_files.items():
            if fname.endswith(".py") and content.strip():
                return fname, content

        # 2. Check learned directory
        target_name = f"day-{self.current_day:03d}"
        for p in LEARNED_DIR.glob(f"**/{target_name}/*.py"):
            if p.is_file():
                try:
                    txt = p.read_text(encoding="utf-8", errors="replace")
                    if txt.strip():
                        return p.name, txt
                except Exception:
                    pass

        # 3. Check last generated code in memory
        if self.last_generated_code and self.last_generated_code.strip():
            return "generated_experiment.py", self.last_generated_code

        return "", ""

    def _prompt_explain_code(self):
        """Requests Gemini to explain the experiment script in plain English with function-level references."""
        py_name, py_code = self._get_active_experiment_code()
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")

        if not py_code:
            messagebox.showinfo(
                "No Experiment Script",
                f"No Python experiment script found for Day {d:03d} yet.\n\n"
                "Click '⚡ Generate Experiment Code' first or create an experiment.py script in the learned directory."
            )
            return

        prompt = (
            f"Please explain the Python experiment script ({py_name}) for Day {d:03d} ({title}) in plain English, "
            f"avoiding jargon and providing clear intuition with function-level references:\n\n"
            f"1. Plain-English Intuition: What does this script do in plain language, and what practical idea does it demonstrate?\n"
            f"2. Function-by-Function Breakdown: Walk through each function in the code step-by-step (referencing `def function_name`). "
            f"Explain in simple plain English: what it does, what inputs it takes, what calculations happen inside, and what it returns.\n"
            f"3. Explaining Any Math/Calculations: For any math or transformations inside the functions, do NOT just restate the equations—explain the mathematical idea in plain words.\n"
            f"4. Interactive Controls & Stress Testing: How do the interactive parameters and Break-It mode test the system?\n"
            f"5. Real-World Connection: How this reinforces today's lesson from first principles.\n\n"
            f"Here is the experiment script to explain:\n```python\n{py_code}\n```"
        )
        self._send_gemini_prompt(prompt)

    def _prompt_stress_test(self):
        d = self.current_day
        info = self.curriculum_catalog.get(d, {})
        title = info.get("title", f"Day {d:03d}")
        prompt = (
            f"In clear plain English, explain the key edge cases, failure modes, and adversarial stress tests for Day {d:03d} ({title}): "
            f"why they break the system, what assumptions fail, and how to stress-test them in code."
        )
        self._send_gemini_prompt(prompt)

    def _clear_day_chat(self):
        """Clears chat conversation for the active day and removes persisted log."""
        d = self.current_day
        self.gemini_chats[d] = None
        self.gemini_histories[d] = []
        self._save_day_chat_history(d)
        self._render_day_chat(d)

    def _on_gemini_input_return(self, event):
        """Handles Return key in chat input (Shift+Return for newline)."""
        if event.state & 0x1: # Shift key held
            return None
        self._send_gemini_prompt()
        return "break"

    def _send_gemini_prompt(self, prompt_text: str = None):
        """Dispatches a user prompt to the streaming Gemini background worker."""
        if not self.gemini_key:
            self.txt_gemini_chat.insert("end", "\n🔑 Gemini API Key Not Set\nPlease click 'Settings' or the API Key button to configure your Google Gemini API key.\n\n", "error_card")
            self.txt_gemini_chat.see("end")
            self._open_gemini_key_dialog()
            return

        if not self.gemini_client:
            self._init_gemini_client()
            if not self.gemini_client:
                self.txt_gemini_chat.insert("end", "\n❌ Gemini client could not be initialized. Please check your API key in Settings.\n\n", "error_card")
                self.txt_gemini_chat.see("end")
                return

        is_custom_inquiry = False
        if prompt_text is None:
            is_custom_inquiry = True
            prompt_text = self.txt_gemini_input.get("1.0", "end").strip()
            self.txt_gemini_input.delete("1.0", "end")

        if not prompt_text:
            return

        d = self.current_day

        # Record non-quick-prompt inquiries to build tutor insights over time
        if is_custom_inquiry:
            self._record_student_inquiry(prompt_text, d)

        # Append to UI and history
        self.txt_gemini_chat.insert("end", f"👤 You (Day {d:03d})\n", "user_hdr")
        self.txt_gemini_chat.insert("end", f"{prompt_text}\n\n", "user_body")
        self.txt_gemini_chat.see("end")

        self.gemini_histories.setdefault(d, []).append({"role": "user", "text": prompt_text})
        self._save_day_chat_history(d)

        # Set UI state to active generation
        self.btn_gemini_send.config(state="disabled")
        self.btn_gemini_stop.config(state="normal")
        self.gemini_stop_requested = False

        # Launch background stream worker
        self.gemini_worker_thread = threading.Thread(
            target=self._run_gemini_stream_worker, args=(prompt_text, d), daemon=True
        )
        self.gemini_worker_thread.start()

    def _run_gemini_stream_worker(self, prompt_text: str, day_num: int):
        """Background thread worker that streams Gemini responses via google.genai."""
        try:
            # Ensure multi-turn chat instance exists for this day
            if day_num not in self.gemini_chats or self.gemini_chats[day_num] is None:
                system_instruction = self._build_gemini_pedagogical_context(day_num)
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
                self.gemini_chats[day_num] = self.gemini_client.chats.create(
                    model=self.gemini_model,
                    config=config
                )

            chat = self.gemini_chats[day_num]
            stream = chat.send_message_stream(prompt_text)

            self.gemini_queue.put(("start_response", (day_num,)))
            full_text = []

            for chunk in stream:
                if self.gemini_stop_requested:
                    break
                if chunk.text:
                    full_text.append(chunk.text)
                    self.gemini_queue.put(("chunk", chunk.text))

            combined = "".join(full_text)
            self.gemini_queue.put(("done", (combined, day_num)))

        except Exception as e:
            self.gemini_queue.put(("error", (str(e), day_num)))

    def _check_gemini_queue(self):
        """Polls streaming chunks and completion events on the main Tk thread."""
        try:
            while True:
                msg_type, payload = self.gemini_queue.get_nowait()
                if msg_type == "start_response":
                    day_num, = payload
                    self.txt_gemini_chat.insert("end", f"🤖 Gemini Tutor (Day {day_num:03d})\n", "ai_hdr")
                elif msg_type == "chunk":
                    self.txt_gemini_chat.insert("end", payload, "ai_body")
                    self.txt_gemini_chat.see("end")
                elif msg_type == "done":
                    full_text, day_num = payload
                    self.gemini_histories.setdefault(day_num, []).append({"role": "ai", "text": full_text})
                    self._save_day_chat_history(day_num)
                    self.btn_gemini_send.config(state="normal")
                    self.btn_gemini_stop.config(state="disabled")

                    # Re-render chat so completed markdown (including math formulas and code blocks) is rendered with rich typography
                    self._render_day_chat(day_num)

                    # Check for generated code
                    code = self._extract_python_code(full_text)
                    if code:
                        self.last_generated_code = code
                        self.code_action_bar.pack(fill="x", before=self.txt_gemini_chat.master)
                        lines_cnt = len(code.splitlines())
                        self.lbl_code_action_status.config(text=f"✨ Generated Python Code ({lines_cnt} lines) - Ready to run!")

                elif msg_type == "error":
                    err_msg, day_num = payload
                    self.txt_gemini_chat.insert("end", f"\n❌ Gemini API Error: {err_msg}\n\n", "error_card")
                    self.txt_gemini_chat.see("end")
                    self.btn_gemini_send.config(state="normal")
                    self.btn_gemini_stop.config(state="disabled")
        except queue.Empty:
            pass
        finally:
            self.after(30, self._check_gemini_queue)

    def _stop_gemini_generation(self):
        """Signals the background worker to halt streaming."""
        self.gemini_stop_requested = True
        self.btn_gemini_stop.config(state="disabled")
        self.btn_gemini_send.config(state="normal")

    def _extract_python_code(self, text: str) -> str:
        """Extracts python script blocks from a markdown formatted response."""
        matches = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
        if matches:
            return matches[-1].strip()
        generic_matches = re.findall(r"```\s*(.*?)\s*```", text, re.DOTALL)
        if generic_matches:
            for m in reversed(generic_matches):
                if "import " in m or "def " in m or "print(" in m:
                    return m.strip()
        return ""

    def _on_load_code_to_editor(self):
        """Loads generated code into Tab 2 (Code Editor)."""
        if not self.last_generated_code:
            return
        self.txt_code.delete("1.0", "end")
        self.txt_code.insert("1.0", self.last_generated_code)
        self.lbl_code_filename.config(text="generated_experiment.py")
        self.notebook.select(self.tab_code)
        self.lbl_status.config(text="Loaded Gemini generated code into Code Editor")

    def _on_save_code_to_experiment(self):
        """Saves generated code as learned/week-WW/day-DDD/experiment.py."""
        if not self.last_generated_code:
            return
        d = self.current_day
        target_name = f"day-{d:03d}"
        w_num = ((d - 1) // 7) + 1
        if w_num > 52: w_num = 52

        target_dir = LEARNED_DIR / f"week-{w_num:02d}" / target_name
        target_dir.mkdir(parents=True, exist_ok=True)
        py_path = target_dir / "experiment.py"
        py_path.write_text(self.last_generated_code, encoding="utf-8")

        self.current_files["experiment.py"] = self.last_generated_code
        self.load_day(d)
        self.btn_run.config(state="normal")
        self.lbl_status.config(text=f"Saved experiment code to {py_path.name}")
        messagebox.showinfo("Code Saved", f"Successfully saved experiment code to:\n{py_path}")

    def _on_run_generated_code(self):
        """Saves generated code to experiment.py and immediately executes it in the Console."""
        if not self.last_generated_code:
            return
        self._on_save_code_to_experiment()
        self.notebook.select(self.tab_console)
        self.run_active_experiment()

    # =========================================================================
    # RECREATE & EXPAND LESSON SUITE WITH GEMINI (PERSONALIZED)
    # =========================================================================

    def recreate_day_with_gemini(self):
        """
        Interactive action from Tab 1 (Lesson Document) allowing the user to call Gemini
        to generate or recreate the complete 4-part learning suite from the syllabus plan.
        """
        self._open_lesson_generator_dialog(initial_day=self.current_day)

    def _run_recreate_day_worker(self, target_day: int):
        """
        Background worker that calls Gemini to generate:
        - Lesson Guide (README.md)
        - Technical Walkthrough (analysis.md & math.md)
        - Operational Python Tool (experiment.py)
        tailored to the student profile.
        """
        try:
            client = genai.Client(api_key=self.gemini_key)
            w_num = ((target_day - 1) // 7) + 1
            if w_num > 52: w_num = 52

            day_info = self.curriculum_catalog.get(target_day, {})
            day_title = day_info.get("title", f"Day {target_day:03d}")
            day_theme = day_info.get("theme", "Understand")
            day_level = day_info.get("level", "Aviation as a system")

            # Extract student profile
            prof = self.student_profile
            student_name = prof.get("student_name", "Student")
            arch = prof.get("archetype", "🛠️ Hands-On Systems Builder")
            arch_desc = prof.get("archetype_desc", "")
            scores = prof.get("scores", {})
            prefs = prof.get("preferences", {})
            custom_directives = prefs.get("custom_directives", "")

            system_instruction = f"""You are the Chief Aviation Architect and Senior Flight Operations Pedagogical Lead for the 365 Days of Aviation curriculum.
Your mission is to expand and recreate Day {target_day:03d} into a coherent, robust, and deep exploration of civil aviation.

=== LEARNER CUSTOMISATION CONTEXT ===
• Student Name: {student_name}
• Learning Archetype: {arch} ({arch_desc})
• Cognitive Profile:
  - Code vs Theory: {scores.get('code_vs_theory', 80)}/100 ({'Prefers working code & operational simulations' if scores.get('code_vs_theory', 80) >= 50 else 'Prefers regulatory and operational theory first'})
  - Systems vs Primitives: {scores.get('systems_vs_primitives', 75)}/100 ({'Focuses on end-to-end ecosystem architecture & flight operations' if scores.get('systems_vs_primitives', 75) >= 50 else 'Focuses on isolated component mechanics'})
  - Visual vs Verbal: {scores.get('visual_vs_verbal', 70)}/100
• Preferences:
  - Explanation Depth: {prefs.get('explanation_depth', 'Deep Mechanical + Operational Realism')}
  - Technical Rigor: {prefs.get('math_rigor', 'Operational Context + Worked Numerical Examples')}
  - Code Style: {prefs.get('code_style', 'Production-grade, annotated with intermediate printouts')}
{f"• Student Directives: {custom_directives}" if custom_directives else ""}

=== PEDAGOGICAL BOUNDARY & SCOPE ===
• Topic: {day_title} (Day {target_day:03d}, Week {w_num:02d}, Theme: {day_theme})
• Domain Level: {day_level}
• Do NOT invent abstract machine learning math or graph theory for the sake of math!
• All content MUST be genuine civil aviation: ICAO SARPs, EASA Easy Access Rules/CAT/Part-M/Part-ORO, flight operations, dispatch, A-CDM turnarounds, structural envelopes (MZFM/MTOM/MLM), trajectory vertical profiles (Top of Descent 3:1 rule), statutory fuel reserves, and SMS safety barriers.

=== REQUIRED OUTPUT STRUCTURE (CRITICAL) ===
You MUST return your output strictly segmented into three tagged blocks with no introductory text before the first tag:

<<<LESSON_DOCUMENT>>>
# Day {target_day:03d} — Operational Guide: {day_title}

[← Return to Master Syllabus](../../lessons/README.md) | [Technical Walkthrough](analysis.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Executive Summary & Operational Context
(Comprehensive, engaging, plain-English exploration tailored to the student's learning style, detailing why this topic exists, who regulates it, and how it impacts safety and commerce.)

## 2. Institutional Architecture & Stakeholder Handshakes
(Breakdown of airlines, airports, ANSPs, ground handlers, and civil aviation authorities involved.)

## 3. Real-World Flight Operations Scenario & Failure Modes
(Realistic flight example, edge cases, disruption cascades, and SMS barriers.)

## 4. Practical Implementation Reference
(Explanation of the interactive Python tool and how to interpret its findings.)
<<<END_LESSON_DOCUMENT>>>

<<<TECHNICAL_WALKTHROUGH>>>
# Day {target_day:03d} — Technical Walkthrough: {day_title}

[← Return to Lesson Guide](README.md) | [System Topology Canvas](architecture.mermaid) | [Run Python Simulator](experiment.py)

---

## 1. Quantitative Modeling & Physical/Operational Principles
(Real-world formulas in LaTeX $inline$ and $$display$$, explaining the physical or legal meaning of every variable without math for math's sake.)

## 2. Step-by-Step Worked Numerical Trace
(A concrete, realistic numerical example, e.g. A320 or B737 flight, step-by-step numbers, inputs, and final outputs.)

## 3. Regulatory Boundaries & Critical Thresholds
(Statutory certification limits, MEL relief categories, fuel reserve limits, or curfew cutoffs.)
<<<END_TECHNICAL_WALKTHROUGH>>>

<<<OPERATIONAL_EXPERIMENT>>>
\"\"\"
Day {target_day:03d} Operational Experiment: {day_title}
Self-contained standard library Python tool directly modeling today's aviation topic.
\"\"\"
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Interactive prompts with sensible defaults on Enter
# Step-by-step intermediate calculation printouts
# Adversarial stress test / failure injection
# Clean exit code 0
<<<END_OPERATIONAL_EXPERIMENT>>>
"""

            user_prompt = f"Recreate and expand Day {target_day:03d}: '{day_title}' into a comprehensive aviation learning suite tailored to my learning profile."

            self.after(0, lambda: self.lbl_doc_recreate_status.config(text="Generating with Gemini..."))

            response = client.models.generate_content(
                model=self.gemini_model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                    max_output_tokens=8192
                )
            )

            raw_text = response.text or ""

            # Parse the three sections
            doc_match = re.search(r"<<<LESSON_DOCUMENT>>>(.*?)<<<END_LESSON_DOCUMENT>>>", raw_text, re.DOTALL)
            tech_match = re.search(r"<<<TECHNICAL_WALKTHROUGH>>>(.*?)<<<END_TECHNICAL_WALKTHROUGH>>>", raw_text, re.DOTALL)
            code_match = re.search(r"<<<OPERATIONAL_EXPERIMENT>>>(.*?)<<<END_OPERATIONAL_EXPERIMENT>>>", raw_text, re.DOTALL)

            lesson_doc = doc_match.group(1).strip() if doc_match else ""
            tech_walkthrough = tech_match.group(1).strip() if tech_match else ""
            py_code = code_match.group(1).strip() if code_match else ""

            # If python code contains backtick fences, strip them
            if py_code.startswith("```python"):
                py_code = re.sub(r"^```python\s*", "", py_code)
                py_code = re.sub(r"\s*```$", "", py_code)
            elif py_code.startswith("```"):
                py_code = re.sub(r"^```\s*", "", py_code)
                py_code = re.sub(r"\s*```$", "", py_code)

            if not lesson_doc and not tech_walkthrough and not py_code:
                raise ValueError("Gemini response did not contain the expected delimited lesson blocks.")

            # Target directory
            target_dir = LEARNED_DIR / f"week-{w_num:02d}" / f"day-{target_day:03d}"
            target_dir.mkdir(parents=True, exist_ok=True)

            if lesson_doc:
                (target_dir / "README.md").write_text(lesson_doc, encoding="utf-8")
            if tech_walkthrough:
                (target_dir / "analysis.md").write_text(tech_walkthrough, encoding="utf-8")
                (target_dir / "math.md").write_text(tech_walkthrough, encoding="utf-8")
            if py_code:
                (target_dir / "experiment.py").write_text(py_code, encoding="utf-8")

            # Post success to UI thread
            self.after(0, lambda: self._on_recreate_success(target_day))

        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self._on_recreate_error(err_msg))

    def _on_recreate_success(self, day_num: int):
        self.btn_recreate_lesson.config(state="normal", text="✨ Recreate with Gemini (Personalized)")
        self.lbl_doc_recreate_status.config(text="✨ Suite Recreated!")
        self.lbl_status.config(text=f"✨ Successfully regenerated Day {day_num:03d} with Gemini.")
        self.load_day(day_num)
        messagebox.showinfo(
            "Lesson Suite Recreated",
            f"Day {day_num:03d} has been successfully expanded and recreated by Gemini!\n\n"
            f"Updated files:\n"
            f"• 📖 README.md (Lesson Document)\n"
            f"• 📊 analysis.md / math.md (Technical Walkthrough)\n"
            f"• 🐍 experiment.py (Operational Python Tool)\n\n"
            f"All tabs have been refreshed."
        )

    def _on_recreate_error(self, err_msg: str):
        self.btn_recreate_lesson.config(state="normal", text="✨ Recreate with Gemini (Personalized)")
        self.lbl_doc_recreate_status.config(text="❌ Error")
        self.lbl_status.config(text=f"❌ Error recreating lesson: {err_msg[:60]}")
        messagebox.showerror(
            "Recreation Failed",
            f"Failed to recreate the lesson with Gemini:\n\n{err_msg}"
        )

    # =========================================================================
    # GAMIFIED KNOWLEDGE TEST & PROGRESS MANAGEMENT (0-3 STARS)
    # =========================================================================

    def _load_progress(self):
        """Loads completed days and star ratings from .aviation_progress.json."""
        self.completed_days = {}
        if PROGRESS_FILE.exists():
            try:
                data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
                for k, v in data.get("completed_days", {}).items():
                    self.completed_days[int(k)] = v
                self.total_stars = data.get("total_stars", sum(v.get("stars", 0) for v in self.completed_days.values()))
            except Exception:
                pass

        # If new or empty, initialize Day 1 as completed with 3 stars so user has active baseline
        if not self.completed_days:
            self.completed_days[1] = {
                "stars": 3,
                "score": 100,
                "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "feedback": "Mastered civil aviation ecosystem fundamentals, regulatory governance, and systemic flight operations."
            }
            self.total_stars = 3
            self._save_progress()

        self._scan_learned_days()

    def _save_progress(self):
        """Saves current completion status and stars to .aviation_progress.json."""
        self.total_stars = sum(v.get("stars", 0) for v in self.completed_days.values())
        payload = {
            "completed_days": {str(k): v for k, v in self.completed_days.items()},
            "total_stars": self.total_stars,
            "total_completed": len([d for d, v in self.completed_days.items() if v.get("stars", 0) >= 1])
        }
        try:
            PROGRESS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _on_notebook_tab_changed(self, event):
        """Called when user switches tabs in the workspace notebook."""
        try:
            sel = self.notebook.select()
            if hasattr(self, "tab_video") and sel != str(self.tab_video) and getattr(self, "video_is_playing", False):
                self._pause_video_playback()

            if sel == str(self.tab_canvas):
                self._draw_architecture_canvas()
            elif sel == str(self.tab_test):
                self._render_test_view()
            elif sel == str(self.tab_gemini):
                self._update_gemini_tab_header()
            elif hasattr(self, "tab_slides") and sel == str(self.tab_slides):
                self._on_slides_tab_selected()
            elif hasattr(self, "tab_infographic") and sel == str(self.tab_infographic):
                self._on_infographic_tab_selected()
            elif hasattr(self, "tab_video") and sel == str(self.tab_video):
                self._on_video_tab_selected()
        except Exception:
            pass

    def _build_test_tab(self, parent):
        """Builds Tab 6: Gemini-Led Knowledge Assessment & Gamified Rating."""
        top_bar = tk.Frame(parent, bg="#1e293b", height=50)
        top_bar.pack(fill="x")

        self.lbl_test_title = tk.Label(top_bar, text="Day 001 Knowledge Assessment", font=("Segoe UI", 11, "bold"),
                                       fg="#ffffff", bg="#1e293b")
        self.lbl_test_title.pack(side="left", padx=16, pady=10)

        self.lbl_test_badge = tk.Label(top_bar, text="Status: ⚪ Unfinished", font=("Segoe UI", 9, "bold"),
                                       fg=TEXT_MUTED, bg=BG_CODE, padx=10, pady=3, bd=1, relief="solid")
        self.lbl_test_badge.pack(side="left", padx=10, pady=10)

        self.lbl_test_timer = tk.Label(top_bar, text="⏱️ 2–5 Min Assessment · 0–3 Stars", font=("Segoe UI", 8),
                                       fg=TEXT_MUTED, bg="#1e293b")
        self.lbl_test_timer.pack(side="right", padx=16, pady=10)

        # Scrollable questions container
        container = tk.Frame(parent, bg=BG_PANEL)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        self.test_canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        test_scroll = ttk.Scrollbar(container, orient="vertical", command=self.test_canvas.yview)
        self.test_scrollable_frame = tk.Frame(self.test_canvas, bg=BG_PANEL)

        self.test_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.test_canvas.configure(scrollregion=self.test_canvas.bbox("all"))
        )
        self.test_canvas_window = self.test_canvas.create_window((0, 0), window=self.test_scrollable_frame, anchor="nw")
        self.test_canvas.configure(yscrollcommand=test_scroll.set)

        self.test_canvas.bind(
            "<Configure>",
            lambda e: self.test_canvas.itemconfig(self.test_canvas_window, width=max(600, e.width - 24))
        )

        self.test_canvas.pack(side="left", fill="both", expand=True)
        test_scroll.pack(side="right", fill="y")

    def _update_test_tab_header(self):
        """Updates the Test Tab header title, stars badge, and timer indicator."""
        d = self.current_day
        info = self.completed_days.get(d)
        stars = info.get("stars", 0) if info else 0
        score = info.get("score", 0) if info else 0

        title = f"Day {d:03d} Knowledge Mastery Assessment"
        catalog_entry = self.curriculum_catalog.get(d, {})
        if catalog_entry.get("title"):
            title = f"Day {d:03d}: {catalog_entry['title']}"

        self.lbl_test_title.config(text=title[:52] + ("..." if len(title) > 52 else ""))

        if stars == 3:
            self.lbl_test_badge.config(text=f"⭐⭐⭐ Mastered ({score}%)", fg=ACCENT_EMERALD, bg="#062e24")
        elif stars == 2:
            self.lbl_test_badge.config(text=f"⭐⭐ Proficient ({score}%)", fg=ACCENT_CYAN, bg="#082f49")
        elif stars == 1:
            self.lbl_test_badge.config(text=f"⭐ Developing ({score}%)", fg=ACCENT_AMBER, bg="#2e1a05")
        else:
            self.lbl_test_badge.config(text="Status: ⚪ Unfinished - Pass to Complete Day", fg=TEXT_MUTED, bg=BG_CODE)

    def _render_test_view(self):
        """Renders the question cards, mastery banner, and submission controls in the test tab."""
        for child in self.test_scrollable_frame.winfo_children():
            child.destroy()

        d = self.current_day
        info = self.completed_days.get(d)
        stars = info.get("stars", 0) if info else 0
        score = info.get("score", 0) if info else 0
        feedback = info.get("feedback", "") if info else ""

        # Top Mastery Result Banner if completed
        if stars >= 1:
            star_str = "⭐" * stars
            tier = "Mastered" if stars == 3 else ("Proficient" if stars == 2 else "Developing")
            color = ACCENT_EMERALD if stars == 3 else (ACCENT_CYAN if stars == 2 else ACCENT_AMBER)
            bg_color = "#022c22" if stars == 3 else ("#082f49" if stars == 2 else "#2e1a05")

            banner = tk.Frame(self.test_scrollable_frame, bg=bg_color, bd=1, relief="solid",
                              highlightthickness=1, highlightbackground=color)
            banner.pack(fill="x", pady=(0, 14), padx=6)

            top_row = tk.Frame(banner, bg=bg_color)
            top_row.pack(fill="x", padx=16, pady=(12, 4))

            tk.Label(top_row, text=f"{star_str} Day {d:03d} {tier}!", font=("Segoe UI", 13, "bold"),
                     fg=color, bg=bg_color).pack(side="left")
            tk.Label(top_row, text=f"Score: {score}%", font=("Segoe UI", 11, "bold"),
                     fg="#ffffff", bg=bg_color).pack(side="right")

            if feedback:
                tk.Label(banner, text=feedback, font=("Segoe UI", 9, "italic"), fg="#cbd5e1",
                         bg=bg_color, wraplength=760, justify="left").pack(anchor="w", padx=16, pady=(0, 10))

            btn_row = tk.Frame(banner, bg=bg_color)
            btn_row.pack(fill="x", padx=16, pady=(0, 12))

            tk.Button(btn_row, text="🔄 Retake Test (Level Up)", font=("Segoe UI", 8, "bold"),
                      fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155", bd=1, relief="solid",
                      padx=10, pady=3, cursor="hand2", command=self._retake_knowledge_test).pack(side="left")

            if d < 365:
                tk.Button(btn_row, text=f"▶ Advance to Day {d+1:03d}", font=("Segoe UI", 8, "bold"),
                          fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", bd=0,
                          padx=12, pady=3, cursor="hand2", command=self._advance_to_next_day).pack(side="left", padx=12)

        # Questions Section
        questions = self._get_day_test_questions(d)
        self.test_vars = {}
        self.test_reasoning_entries = {}

        q_labels = [
            "Question 1 · Core Conceptual Mental Model & Taxonomy",
            "Question 2 · Mathematical Formulation & Algorithmic Invariants",
            "Question 3 · Adversarial Break-It Scenario & Production Failure Modes"
        ]

        for i, q_data in enumerate(questions):
            card = tk.Frame(self.test_scrollable_frame, bg="#1e293b", bd=1, relief="solid",
                            highlightthickness=1, highlightbackground=BORDER_BRIGHT)
            card.pack(fill="x", pady=8, padx=6)

            hdr = tk.Label(card, text=q_labels[i], font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg="#1e293b")
            hdr.pack(anchor="w", padx=16, pady=(10, 4))

            q_text = tk.Label(card, text=q_data["q"], font=("Segoe UI", 10), fg="#ffffff", bg="#1e293b",
                              wraplength=780, justify="left")
            q_text.pack(anchor="w", padx=16, pady=(0, 8))

            var = tk.StringVar(value="")
            self.test_vars[i] = var

            for opt_key, opt_text in q_data["options"].items():
                rb = tk.Radiobutton(card, text=f"{opt_key}. {opt_text}", variable=var, value=opt_key,
                                    font=("Segoe UI", 9), fg="#cbd5e1", bg="#1e293b", selectcolor=BG_CODE,
                                    activebackground="#1e293b", activeforeground="#ffffff",
                                    wraplength=760, justify="left")
                rb.pack(anchor="w", padx=22, pady=3)

            # If already completed, display the correct answer and pedagogical explanation
            if stars >= 1:
                exp_frame = tk.Frame(card, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground="#334155")
                exp_frame.pack(fill="x", padx=16, pady=(8, 12))
                tk.Label(exp_frame, text=f"✓ Correct Key: {q_data['correct']}", font=("Segoe UI", 9, "bold"),
                         fg=ACCENT_EMERALD, bg="#0f172a").pack(anchor="w", padx=10, pady=(6, 2))
                tk.Label(exp_frame, text=q_data["explanation"], font=("Segoe UI", 8),
                         fg=TEXT_MUTED, bg="#0f172a", wraplength=740, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        # Technical Defense / Reasoning Box
        reasoning_card = tk.Frame(self.test_scrollable_frame, bg="#1e293b", bd=1, relief="solid",
                                  highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        reasoning_card.pack(fill="x", pady=8, padx=6)

        tk.Label(reasoning_card, text="Technical Defense & Rationale (Bonus: up to +10% score)",
                 font=("Segoe UI", 9, "bold"), fg=ACCENT_AMBER, bg="#1e293b").pack(anchor="w", padx=16, pady=(10, 2))
        tk.Label(reasoning_card, text="Briefly defend your answers in 1–2 sentences (e.g. why the invariant holds or how the adversarial edge case causes failure):",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w", padx=16, pady=(0, 6))

        r_entry = tk.Entry(reasoning_card, font=("Segoe UI", 9), bg=BG_CODE, fg="#ffffff",
                           insertbackground=ACCENT_CYAN, bd=1, relief="solid")
        r_entry.pack(fill="x", padx=16, pady=(0, 12))
        self.test_reasoning_entries[0] = r_entry

        # Submit Action Bar
        action_bar = tk.Frame(self.test_scrollable_frame, bg=BG_PANEL)
        action_bar.pack(fill="x", pady=14, padx=6)

        btn_submit = tk.Button(action_bar, text="✨ Submit Assessment & Grade with Gemini", font=("Segoe UI", 10, "bold"),
                               fg="#ffffff", bg=ACCENT_CYAN, activebackground="#0891b2", activeforeground="#ffffff",
                               bd=0, padx=18, pady=8, cursor="hand2", command=self._submit_knowledge_test)
        btn_submit.pack(side="left")

        self.lbl_test_action_status = tk.Label(action_bar, text="Ready · Select answers for all 3 questions",
                                               font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL)
        self.lbl_test_action_status.pack(side="left", padx=16)

    def _get_day_test_questions(self, day_num: int):
        """Generates 3 targeted, high-signal scenario questions tailored to the day's curriculum."""
        target_name = f"day-{day_num:03d}"
        w_num = ((day_num - 1) // 7) + 1
        if w_num > 52: w_num = 52

                # Bespoke high-precision bank for Day 1 and Day 2 (Aviation)
        if day_num == 1:
            return [
                {
                    "q": "What constitutes the core definition of the civil aviation system in Aviation 365?",
                    "options": {
                        "A": "A connected operational, technical, regulatory and human system of systems enabling safe air transport, commerce, and global connectivity",
                        "B": "A collection of independent disciplines with no operational dependencies between airlines, airports, and ANSPs",
                        "C": "Exclusively pilot flight-training syllabi and aircraft flying checklists",
                        "D": "A purely commercial passenger booking network with no physical ground operations"
                    },
                    "correct": "A",
                    "explanation": "Aviation is an interdependent system of systems. A flight can be mechanically airworthy yet unable to operate due to crew duty limits, unavailable stands, weather, airspace constraints, or regulatory restrictions."
                },
                {
                    "q": "Which international treaty established the legal foundation of modern international civil aviation, State sovereignty over airspace, and the creation of ICAO?",
                    "options": {
                        "A": "The Treaty of Versailles (1919)",
                        "B": "The Chicago Convention on International Civil Aviation (1944)",
                        "C": "The Warsaw Convention (1929)",
                        "D": "The Montreal Protocol (1999)"
                    },
                    "correct": "B",
                    "explanation": "Signed on December 7, 1944, the Chicago Convention (ICAO Doc 7300) established airspace sovereignty, international Standards and Recommended Practices (SARPs), and the International Civil Aviation Organization."
                },
                {
                    "q": "Why can an aircraft that has zero technical defects still be legally or physically prevented from departing?",
                    "options": {
                        "A": "It cannot; airworthy aircraft are automatically cleared to depart anytime",
                        "B": "Because departure requires an intact chain: crew FTL legality, slot/CTOT allocation, runway friction minima, dispatch fuel release, and ATC clearance",
                        "C": "Only if the aircraft manufacturer revokes the registration",
                        "D": "Because airports close whenever commercial passengers board"
                    },
                    "correct": "B",
                    "explanation": "Systemic dependencies mean that crew duty timeouts, ATFM ground delay programs, below-minima runway braking action, or security holds can ground a completely serviceable aircraft."
                }
            ]
        elif day_num == 2:
            return [
                {
                    "q": "In the aviation ecosystem stakeholder model, what is the primary operational responsibility of an Air Navigation Service Provider (ANSP)?",
                    "options": {
                        "A": "Selling airline tickets and managing passenger baggage check-in",
                        "B": "Managing air traffic services (ATS), airspace organisation, CNS infrastructure, and maintaining safe aircraft separation",
                        "C": "Certifying aircraft engines under EASA CS-E",
                        "D": "Operating duty-free shops and terminal baggage belts"
                    },
                    "correct": "B",
                    "explanation": "ANSPs provide air traffic management (ATM), air traffic control (ATC), flight information services (FIS), alerting services, and communication, navigation, and surveillance (CNS) infrastructure."
                },
                {
                    "q": "What is the key regulatory distinction between ICAO Standards and Recommended Practices (SARPs)?",
                    "options": {
                        "A": "Standards are uniform and mandatory for Contracting States unless a formal difference is notified under Article 38; Recommended Practices are desirable but non-mandatory",
                        "B": "Recommended Practices carry criminal penalties, whereas Standards are optional guidelines",
                        "C": "There is no distinction; both are identical EU regulations",
                        "D": "Standards only apply to military aircraft"
                    },
                    "correct": "A",
                    "explanation": "Under the Chicago Convention, Standards are mandatory specifications where uniform application is recognized as necessary, requiring notification of differences under Article 38 if not implemented; Recommended Practices are recognized as desirable."
                },
                {
                    "q": "How does an airline Operational Control Center (OCC) interact with an Airport Collaborative Decision Making (A-CDM) platform?",
                    "options": {
                        "A": "By completely overriding all ATC departure clearances",
                        "B": "By sharing Target Take-Off Times (TTOT) and Target Off-Block Times (TOBT) to optimize taxi sequencing and reduce runway queuing",
                        "C": "By purchasing airport runways during peak hours",
                        "D": "By bypassing customs and immigration screening"
                    },
                    "correct": "B",
                    "explanation": "A-CDM connects the airline, airport operator, ground handlers, and ATC through shared situational milestones (TOBT, TSAT, TTOT) to optimize taxi flow and pre-departure sequencing."
                }
            ]

        # Dynamic high-signal curriculum synthesis for any day from README
        readme_text = ""
        learned_matches = list(LEARNED_DIR.glob(f"**/{target_name}/README.md"))
        if learned_matches and learned_matches[0].is_file():
            readme_text = learned_matches[0].read_text(encoding="utf-8", errors="replace")
        elif (LESSONS_DIR / f"week-{w_num:02d}" / f"day-{day_num:03d}.md").exists():
            readme_text = (LESSONS_DIR / f"week-{w_num:02d}" / f"day-{day_num:03d}.md").read_text(encoding="utf-8", errors="replace")

        title_m = re.search(r'title:\s*"([^"]+)"', readme_text) or re.search(r'# Day \d+: ([^\n\r]+)', readme_text)
        day_title = title_m.group(1).strip() if title_m else f"Day {day_num:03d} Topic"

        return [
            {
                "q": f"What is the foundational operational objective of Day {day_num:03d} ({day_title})?",
                "options": {
                    "A": f"To master {day_title} through operational workflows, regulatory compliance, and cross-ecosystem interface analysis",
                    "B": "To treat aviation components as completely isolated systems with no upstream or downstream dependencies",
                    "C": "To bypass regulatory certification and rely solely on informal commercial agreements",
                    "D": "To operate commercial flights without standard operating procedures or airworthiness oversight"
                },
                "correct": "A",
                "explanation": f"Day {day_num:03d} establishes practical mastery of {day_title} grounded in operational realities, statutory regulatory standards, and systemic interdependencies."
            },
            {
                "q": f"In Day {day_num:03d}'s operational framework and system architecture, what is the critical regulatory invariant?",
                "options": {
                    "A": "Commercial punctuality takes precedence over mandatory airworthiness and safety minimums",
                    "B": "Operating procedures must comply with statutory ICAO/EASA safety baselines, operational limitations, and SMS hazard controls",
                    "C": "Safety oversight audits are purely optional recommendations that operators may ignore",
                    "D": "A flight may be dispatched regardless of crew flight duty limitations or weather minima"
                },
                "correct": "B",
                "explanation": "Aviation operates under strict legal and safety baselines: operations are permitted only within certified limitations (AFM, Part-CAT, FTL, and Aerodrome Operating Minima)."
            },
            {
                "q": f"When stress-testing Day {day_num:03d}'s operational scenario under adverse conditions, what is the primary threat mitigation?",
                "options": {
                    "A": "Ignore weather deterioration and press on to avoid airline delay compensation",
                    "B": "Evaluate cascading disruption across crew FTL, slot/CTOT windows, and diversion fuel reserves using Threat and Error Management (TEM)",
                    "C": "Disable flight data monitoring and SMS occurrence reporting during irregular operations",
                    "D": "Assume downstream destination airports will remain open indefinitely during disruptions"
                },
                "correct": "B",
                "explanation": "Safety Management Systems (SMS) and TEM require proactive identification of cascading hazards, verifying that active barriers (fuel reserves, alternate aerodromes, duty limits) remain intact."
            }
        ]

    def _submit_knowledge_test(self):
        """Evaluates test answers, awards 0-3 stars, updates completion state, and saves progress."""
        d = self.current_day
        questions = self._get_day_test_questions(d)

        # Validate answers chosen
        answers = {}
        for i in range(len(questions)):
            val = self.test_vars.get(i, tk.StringVar()).get()
            if not val:
                messagebox.showwarning("Incomplete Assessment",
                                       f"Please select an answer for Question {i+1} before submitting.")
                return
            answers[i] = val

        reasoning = self.test_reasoning_entries.get(0, tk.Entry()).get().strip()

        self.lbl_test_action_status.config(text="Grading assessment with Gemini Examiner...", fg=ACCENT_CYAN)
        self.update_idletasks()

        # Grade using Deterministic rubric + reasoning bonus (with optional Gemini enrichment)
        correct_count = sum(1 for i, q in enumerate(questions) if answers[i] == q["correct"])
        base_score = int((correct_count / len(questions)) * 90)
        reasoning_bonus = 10 if len(reasoning) >= 8 else (5 if len(reasoning) > 0 else 0)
        total_score = min(100, base_score + reasoning_bonus)

        # Star formula:
        # 3 Stars (Mastered): >= 85%
        # 2 Stars (Proficient): 70% - 84%
        # 1 Star (Developing): 50% - 69%
        # 0 Stars (Unfinished): < 50%
        if total_score >= 85:
            stars = 3
            feedback = f"Outstanding mastery ({correct_count}/{len(questions)} correct). Strong architectural reasoning and invariant understanding."
        elif total_score >= 70:
            stars = 2
            feedback = f"Solid proficiency ({correct_count}/{len(questions)} correct). Good conceptual grasp; review edge-case failure modes."
        elif total_score >= 50:
            stars = 1
            feedback = f"Developing knowledge ({correct_count}/{len(questions)} correct). Core concept understood, but requires review of mathematical invariants."
        else:
            stars = 0
            feedback = f"Needs review ({correct_count}/{len(questions)} correct). Review the lesson document and rerun the experiment before retaking."

        # If Gemini is configured, enrich the feedback with AI pedagogical insights
        if self.gemini_client:
            try:
                ai_prompt = (
                    f"You are the PracticAI Examiner. Briefly critique this student's submission for Day {d:03d} in 2 sentences:\n"
                    f"Score: {total_score}%, Answers: {answers}, Reasoning: '{reasoning}'. Correct answers: {[q['correct'] for q in questions]}."
                )
                resp = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=ai_prompt,
                    config=types.GenerateContentConfig(max_output_tokens=150, temperature=0.3)
                )
                if resp.text:
                    feedback = resp.text.strip()
            except Exception:
                pass

        # Persist progress if passed (stars >= 1) or update existing
        self.completed_days[d] = {
            "stars": stars,
            "score": total_score,
            "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "feedback": feedback
        }
        self._save_progress()
        self._scan_learned_days()

        # Update UI Badges & Status
        self.lbl_tb_stars.config(text=f"⭐ {self.total_stars} Stars")
        self.lbl_tb_progress.config(text=f"🏆 {len(self.learned_days)}/365 Done")
        self.lbl_progress.config(
            text=f"Mastery: {len(self.learned_days)}/365 Days Completed · ⭐ {self.total_stars} Stars"
        )
        self._update_test_tab_header()
        self._populate_curriculum_tree()
        self._render_test_view()

        if stars >= 1:
            messagebox.showinfo("Assessment Complete!",
                                f"Congratulations! You earned {'⭐' * stars} ({total_score}% Score) on Day {d:03d}.\n\n"
                                f"Total Stars: {self.total_stars} ⭐ · Completed: {len(self.learned_days)}/365 Days")
        else:
            messagebox.showwarning("Assessment Needs Review",
                                   f"Score: {total_score}% (0 Stars).\n\n"
                                   "A score of at least 50% (⭐) is required to mark the day as complete. "
                                   "Review the lesson document and click 'Retake Test'.")

    def _retake_knowledge_test(self):
        """Resets the day's answers to allow re-testing and leveling up stars."""
        for v in self.test_vars.values():
            v.set("")
        if 0 in self.test_reasoning_entries:
            self.test_reasoning_entries[0].delete(0, "end")
        self.lbl_test_action_status.config(text="Ready · Select your answers and submit", fg=TEXT_MUTED)
        self.test_canvas.yview_moveto(0)

    def _advance_to_next_day(self):
        """Advances to the next day in the curriculum."""
        if self.current_day < 365:
            self.load_day(self.current_day + 1)

    def _select_tab_if_enabled(self, tab):
        """Helper to switch to a notebook tab only if currently normal (enabled)."""
        try:
            if self.notebook.tab(tab, "state") == "normal":
                self.notebook.select(tab)
        except Exception:
            pass

    # =========================================================================
    # TAB 8: NOTEBOOKLM SLIDE DECK VIEWER
    # =========================================================================

    def _build_slides_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=50)
        top_bar.pack(fill="x")

        self.btn_prev_slide = tk.Button(
            top_bar, text="◀ Prev Slide", font=("Segoe UI", 9, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=10, pady=4, cursor="hand2",
            command=self._prev_slide
        )
        self.btn_prev_slide.pack(side="left", padx=(16, 6), pady=8)

        self.lbl_slide_counter = tk.Label(
            top_bar, text="Slide 0 of 0", font=("Segoe UI", 10, "bold"),
            fg=ACCENT_CYAN, bg="#1e293b", padx=6
        )
        self.lbl_slide_counter.pack(side="left", padx=4, pady=8)

        self.btn_next_slide = tk.Button(
            top_bar, text="Next Slide ▶", font=("Segoe UI", 9, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=10, pady=4, cursor="hand2",
            command=self._next_slide
        )
        self.btn_next_slide.pack(side="left", padx=6, pady=8)

        self.lbl_slide_category = tk.Label(
            top_bar, text="Executive Presentation", font=("Segoe UI", 9, "bold"),
            fg=ACCENT_EMERALD, bg="#0f172a", padx=10, pady=3, bd=1, relief="solid"
        )
        self.lbl_slide_category.pack(side="left", padx=14, pady=8)

        # Quick Slide Jump Combobox
        self.combo_slides = ttk.Combobox(top_bar, width=32, state="readonly", font=("Segoe UI", 9))
        self.combo_slides.pack(side="left", padx=10, pady=8)
        self.combo_slides.bind("<<ComboboxSelected>>", lambda e: self._show_slide(self.combo_slides.current()))

        # Copy Notes Button
        btn_copy_notes = tk.Button(
            top_bar, text="📋 Copy Notes", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=4, cursor="hand2",
            command=self._copy_slide_notes
        )
        btn_copy_notes.pack(side="right", padx=16, pady=8)

        # Main Scrollable Canvas for Slide Card
        container = tk.Frame(parent, bg=BG_PANEL)
        container.pack(fill="both", expand=True)

        self.slides_canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        slides_scroll = ttk.Scrollbar(container, orient="vertical", command=self.slides_canvas.yview)
        self.slides_inner_frame = tk.Frame(self.slides_canvas, bg=BG_PANEL)

        self.slides_inner_frame.bind(
            "<Configure>",
            lambda e: self.slides_canvas.configure(scrollregion=self.slides_canvas.bbox("all"))
        )
        self.slides_canvas_window = self.slides_canvas.create_window((0, 0), window=self.slides_inner_frame, anchor="nw")
        self.slides_canvas.configure(yscrollcommand=slides_scroll.set)

        self.slides_canvas.bind(
            "<Configure>",
            lambda e: self.slides_canvas.itemconfig(self.slides_canvas_window, width=max(600, e.width - 20))
        )

        self.slides_canvas.pack(side="left", fill="both", expand=True, padx=12, pady=10)
        slides_scroll.pack(side="right", fill="y", pady=10)

        # Collapsible Speaker Notes Drawer at Bottom
        self.notes_drawer = tk.Frame(parent, bg="#0f172a", highlightthickness=1, highlightbackground=BORDER)
        self.notes_drawer.pack(side="bottom", fill="x")

        notes_header = tk.Frame(self.notes_drawer, bg="#1e293b", height=28)
        notes_header.pack(fill="x")
        self.btn_toggle_notes = tk.Button(
            notes_header, text="🎙️ Presenter Script & Speaker Notes ▾", font=("Segoe UI", 8, "bold"),
            fg="#fde68a", bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
            bd=0, padx=10, pady=2, cursor="hand2", command=self._toggle_speaker_notes
        )
        self.btn_toggle_notes.pack(side="left", padx=8)

        self.notes_body = tk.Frame(self.notes_drawer, bg="#090d16", height=90)
        self.notes_body.pack(fill="x", padx=10, pady=(4, 8))
        self.notes_visible = True

        self.txt_speaker_notes = tk.Text(
            self.notes_body, height=4, font=("Segoe UI", 9),
            bg="#090d16", fg="#fde68a", insertbackground=TEXT_ACCENT,
            bd=0, highlightthickness=0, wrap="word"
        )
        self.txt_speaker_notes.pack(fill="both", expand=True, padx=6, pady=4)

    def _toggle_speaker_notes(self):
        if self.notes_visible:
            self.notes_body.pack_forget()
            self.btn_toggle_notes.config(text="🎙️ Presenter Script & Speaker Notes ▸")
            self.notes_visible = False
        else:
            self.notes_body.pack(fill="x", padx=10, pady=(4, 8))
            self.btn_toggle_notes.config(text="🎙️ Presenter Script & Speaker Notes ▾")
            self.notes_visible = True

    def _on_slides_tab_selected(self):
        if self.slides_data and self.slides_data.get("slides"):
            self._show_slide(self.current_slide_idx)

    def _render_slides_view(self, learned_dir):
        """Loads and prepares the slide deck from slides.json or slides.md."""
        self.slides_data = None
        self.current_slide_idx = 0

        # Try slides.json first
        json_path = learned_dir / "slides.json" if learned_dir else None
        if json_path and json_path.exists():
            try:
                self.slides_data = json.loads(json_path.read_text(encoding="utf-8", errors="replace"))
            except Exception as e:
                print(f"Error parsing slides.json: {e}")

        # Fallback to slides.md if json not parsed
        if not self.slides_data and learned_dir and (learned_dir / "slides.md").exists():
            md_text = (learned_dir / "slides.md").read_text(encoding="utf-8", errors="replace")
            self.slides_data = self._parse_slides_md(md_text)

        if self.slides_data and self.slides_data.get("slides"):
            slides = self.slides_data["slides"]
            titles = [f"Slide {s.get('slide_number', i+1)}: {s.get('title', '')[:35]}" for i, s in enumerate(slides)]
            self.combo_slides.config(values=titles)
            self._show_slide(0)
        else:
            self._reset_slides_view()

    def _parse_slides_md(self, md_text: str) -> dict:
        """Parses Markdown slides delimited by '---' into a SlideDeck dict."""
        deck = {"deck_title": f"Day {self.current_day:03d} Presentation", "slides": []}
        sections = re.split(r'\n---\n', md_text)
        s_num = 1
        for sec in sections:
            sec = sec.strip()
            if not sec: continue
            lines = sec.splitlines()
            title = ""
            subtitle = ""
            category = "Operational Overview"
            takeaway = ""
            bullets = []
            technical = ""
            notes = ""

            for line in lines:
                line_str = line.strip()
                if line_str.startswith("# "):
                    deck["deck_title"] = line_str.replace("# ", "").strip()
                elif line_str.startswith("## "):
                    title = re.sub(r'^##\s*(Slide\s*\d+:)?\s*', '', line_str).strip()
                elif line_str.startswith("*") and line_str.endswith("*") and not subtitle:
                    subtitle = line_str.strip("*").strip()
                elif "> **Key Takeaway**:" in line_str:
                    takeaway = line_str.split(":", 1)[1].strip()
                elif line_str.startswith("- ") or line_str.startswith("* "):
                    bullets.append(line_str[2:].strip())
                elif "TECHNICAL:" in line_str:
                    technical = line_str.replace("TECHNICAL:", "").strip()
                elif "*Presenter Script*:" in line_str:
                    notes = line_str.split(":", 1)[1].strip().strip("*")

            if title:
                deck["slides"].append({
                    "slide_number": s_num,
                    "category": category,
                    "title": title,
                    "subtitle": subtitle,
                    "key_takeaway": takeaway,
                    "bullets": bullets if bullets else ["Comprehensive operational analysis and regulatory alignment."],
                    "technical_callout": technical,
                    "speaker_notes": notes
                })
                s_num += 1
        return deck

    def _show_slide(self, idx: int):
        if not self.slides_data or not self.slides_data.get("slides"):
            return
        slides = self.slides_data["slides"]
        if idx < 0: idx = 0
        if idx >= len(slides): idx = len(slides) - 1
        self.current_slide_idx = idx

        s = slides[idx]
        total = len(slides)
        self.lbl_slide_counter.config(text=f"Slide {idx + 1} of {total}")

        # Determine visual theme based on slide category
        category = s.get("category", "Operational Deep Dive")
        cat_lower = category.lower()
        if any(w in cat_lower for w in ["regulat", "law", "govern", "tfeu", "statut"]):
            cat_color = ACCENT_PURPLE
            cat_icon = "⚖️"
        elif any(w in cat_lower for w in ["operat", "cat", "camo", "aoc", "flight"]):
            cat_color = ACCENT_EMERALD
            cat_icon = "✈️"
        elif any(w in cat_lower for w in ["math", "physic", "econ", "metric", "calc"]):
            cat_color = ACCENT_AMBER
            cat_icon = "📊"
        elif any(w in cat_lower for w in ["hazard", "risk", "warning", "emerg", "fail"]):
            cat_color = ACCENT_RED
            cat_icon = "⚠️"
        else:
            cat_color = ACCENT_CYAN
            cat_icon = "🌐"

        self.lbl_slide_category.config(text=f"{cat_icon} {category}", fg=cat_color)
        self.combo_slides.current(idx)
        self.btn_prev_slide.config(state="normal" if idx > 0 else "disabled")
        self.btn_next_slide.config(state="normal" if idx < total - 1 else "disabled")

        # Clear and redraw slide container
        for widget in self.slides_inner_frame.winfo_children():
            widget.destroy()

        # Slide Navigation Pill Strip (1, 2, 3, ... N)
        nav_strip = tk.Frame(self.slides_inner_frame, bg=BG_PANEL)
        nav_strip.pack(fill="x", padx=16, pady=(10, 4))
        tk.Label(nav_strip, text="SLIDE JUMP:", font=("Segoe UI", 7, "bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=(0, 6))
        for p_idx in range(total):
            is_cur = (p_idx == idx)
            btn_pill = tk.Button(
                nav_strip, text=f"{p_idx+1:02d}", font=("Segoe UI", 8, "bold" if is_cur else "normal"),
                fg="#090d16" if is_cur else TEXT_MUTED,
                bg=cat_color if is_cur else "#1e293b",
                activebackground=cat_color,
                bd=0, padx=7, pady=2, cursor="hand2",
                command=lambda p=p_idx: self._show_slide(p)
            )
            btn_pill.pack(side="left", padx=2)

        # Main Slide Presentation Card
        card = tk.Frame(self.slides_inner_frame, bg="#0f172a", bd=1, relief="solid", highlightthickness=2, highlightbackground=cat_color)
        card.pack(fill="x", padx=16, pady=8)

        # Top Category Accent Stripe
        tk.Frame(card, bg=cat_color, height=4).pack(fill="x")

        # Slide Header Bar
        hdr_bar = tk.Frame(card, bg="#0f172a")
        hdr_bar.pack(fill="x", padx=24, pady=(16, 8))

        tk.Label(
            hdr_bar, text=f"SLIDE {s.get('slide_number', idx+1):02d} / {total:02d}",
            font=("Segoe UI", 9, "bold"), fg="#090d16", bg=cat_color, padx=10, pady=2
        ).pack(side="left")

        tk.Label(
            hdr_bar, text=f"🏷️ {category.upper()}",
            font=("Segoe UI", 8, "bold"), fg=cat_color, bg="#1e293b", padx=8, pady=2
        ).pack(side="left", padx=10)

        tk.Label(
            hdr_bar, text=f"Aviation 365 · Day {self.current_day:03d}",
            font=("Segoe UI", 9), fg=TEXT_MUTED, bg="#0f172a"
        ).pack(side="right")

        # Title & Subtitle
        tk.Label(
            card, text=s.get("title", f"Slide {idx+1}"),
            font=("Segoe UI", 18, "bold"), fg=TEXT_MAIN, bg="#0f172a", wraplength=950, justify="left", anchor="w"
        ).pack(fill="x", padx=24, pady=(8, 4))

        if s.get("subtitle"):
            tk.Label(
                card, text=s.get("subtitle", ""),
                font=("Segoe UI", 11, "italic"), fg=TEXT_ACCENT, bg="#0f172a", wraplength=950, justify="left", anchor="w"
            ).pack(fill="x", padx=24, pady=(0, 14))

        # Key Takeaway Box
        if s.get("key_takeaway"):
            kt_box = tk.Frame(card, bg="#0c1f38", bd=0, highlightthickness=1, highlightbackground=cat_color)
            kt_box.pack(fill="x", padx=24, pady=(4, 16))
            tk.Label(
                kt_box, text="💡 EXECUTIVE TAKEAWAY & OPERATIONAL DIRECTIVE",
                font=("Segoe UI", 8, "bold"), fg=cat_color, bg="#0c1f38", anchor="w"
            ).pack(fill="x", padx=14, pady=(8, 2))
            tk.Label(
                kt_box, text=s.get("key_takeaway"),
                font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#0c1f38", wraplength=900, justify="left"
            ).pack(fill="x", padx=14, pady=(0, 10))

        # Operational Bullet Points
        bullets = s.get("bullets", [])
        if bullets:
            b_frame = tk.Frame(card, bg="#0f172a")
            b_frame.pack(fill="x", padx=24, pady=6)
            for b in bullets:
                b_row = tk.Frame(b_frame, bg="#0f172a")
                b_row.pack(fill="x", pady=4)
                tk.Label(b_row, text="✈️", font=("Segoe UI", 9), fg=cat_color, bg="#0f172a").pack(side="left", anchor="n", padx=(0, 8))
                tk.Label(
                    b_row, text=b, font=("Segoe UI", 11), fg=TEXT_MAIN, bg="#0f172a",
                    wraplength=900, justify="left", anchor="w"
                ).pack(side="left", fill="x", expand=True)

        # Technical Callout Box (Avionics MCDU / FMS Display Styling)
        if s.get("technical_callout"):
            tech_box = tk.Frame(card, bg="#020617", highlightthickness=1, highlightbackground=BORDER_BRIGHT)
            tech_box.pack(fill="x", padx=24, pady=(16, 20))
            tk.Label(
                tech_box, text="📟 AVIONICS & STATUTORY TECHNICAL SPECIFICATION:",
                font=("Consolas", 8, "bold"), fg=ACCENT_EMERALD, bg="#020617", anchor="w"
            ).pack(fill="x", padx=14, pady=(8, 2))
            tk.Label(
                tech_box, text=s.get("technical_callout"),
                font=("Consolas", 10), fg="#4ade80", bg="#020617",
                wraplength=900, justify="left"
            ).pack(fill="x", padx=14, pady=(0, 10))

        # Update Presenter Notes
        self.txt_speaker_notes.delete("1.0", "end")
        notes_content = s.get("speaker_notes", "No speaker notes recorded for this slide.")
        self.txt_speaker_notes.insert("1.0", notes_content)

        self.slides_canvas.yview_moveto(0)

    def _prev_slide(self):
        if self.current_slide_idx > 0:
            self._show_slide(self.current_slide_idx - 1)

    def _next_slide(self):
        if self.slides_data and self.current_slide_idx < len(self.slides_data.get("slides", [])) - 1:
            self._show_slide(self.current_slide_idx + 1)

    def _copy_slide_notes(self):
        if not self.slides_data or not self.slides_data.get("slides"):
            return
        s = self.slides_data["slides"][self.current_slide_idx]
        text_to_copy = f"Slide {self.current_slide_idx+1}: {s.get('title')}\n\nKey Takeaway: {s.get('key_takeaway')}\n\nSpeaker Notes:\n{s.get('speaker_notes')}"
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        self.lbl_status.config(text="Slide notes copied to clipboard.")

    def _reset_slides_view(self):
        self.slides_data = None
        self.current_slide_idx = 0
        self.lbl_slide_counter.config(text="Slide 0 of 0")
        self.lbl_slide_category.config(text="No Slide Deck")
        self.combo_slides.config(values=[])
        self.btn_prev_slide.config(state="disabled")
        self.btn_next_slide.config(state="disabled")
        for widget in self.slides_inner_frame.winfo_children():
            widget.destroy()
        placeholder = tk.Label(
            self.slides_inner_frame,
            text=f"No Slide Deck generated for Day {self.current_day:03d}.\nClick '⚡ NotebookLM' in the toolbar to generate slides.",
            font=("Segoe UI", 11), fg=TEXT_MUTED, bg=BG_PANEL, pady=50
        )
        placeholder.pack()
        self.txt_speaker_notes.delete("1.0", "end")
        self.txt_speaker_notes.insert("1.0", "No speaker notes available.")

    # =========================================================================
    # TAB 9: NOTEBOOKLM EXECUTIVE INFOGRAPHIC VIEWER
    # =========================================================================

    def _build_infographic_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=50)
        top_bar.pack(fill="x")

        self.lbl_info_title = tk.Label(
            top_bar, text="🖼️ Executive Infographic", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg="#1e293b"
        )
        self.lbl_info_title.pack(side="left", padx=16, pady=8)

        # Zoom Controls
        btn_zoom_in = tk.Button(
            top_bar, text="🔍 Zoom In (+)", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2",
            command=lambda: self._zoom_infographic(1.2)
        )
        btn_zoom_in.pack(side="left", padx=4, pady=8)

        btn_zoom_out = tk.Button(
            top_bar, text="🔍 Zoom Out (-)", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2",
            command=lambda: self._zoom_infographic(0.833)
        )
        btn_zoom_out.pack(side="left", padx=4, pady=8)

        btn_fit = tk.Button(
            top_bar, text="↔ Fit Window", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2",
            command=self._fit_infographic_to_window
        )
        btn_fit.pack(side="left", padx=4, pady=8)

        btn_100 = tk.Button(
            top_bar, text="1:1 (100%)", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2",
            command=lambda: self._zoom_infographic_absolute(1.0)
        )
        btn_100.pack(side="left", padx=4, pady=8)

        self.lbl_info_zoom = tk.Label(
            top_bar, text="100%", font=("Segoe UI", 8),
            fg=ACCENT_CYAN, bg="#1e293b"
        )
        self.lbl_info_zoom.pack(side="left", padx=6, pady=8)

        # Open SVG Button
        btn_open_svg = tk.Button(
            top_bar, text="🌐 Open Vector SVG (Browser)", font=("Segoe UI", 8, "bold"),
            fg="#ffffff", bg="#0891b2", activebackground="#0e7490", activeforeground="#ffffff",
            bd=0, padx=10, pady=3, cursor="hand2", command=self._open_infographic_svg
        )
        btn_open_svg.pack(side="right", padx=(4, 16), pady=8)

        # Save Button
        btn_save_info = tk.Button(
            top_bar, text="💾 Save Image As...", font=("Segoe UI", 8, "bold"),
            fg="#ffffff", bg=ACCENT_EMERALD, activebackground="#059669", activeforeground="#ffffff",
            bd=0, padx=10, pady=3, cursor="hand2", command=self._save_infographic_as
        )
        btn_save_info.pack(side="right", padx=6, pady=8)

        # Paned Window: Left Canvas + Right Blueprint Panel
        info_pane = tk.PanedWindow(parent, orient="horizontal", bg=BORDER, sashwidth=4, bd=0)
        info_pane.pack(fill="both", expand=True)

        # Left Canvas Container
        canvas_container = tk.Frame(info_pane, bg=BG_CANVAS)
        info_pane.add(canvas_container, minsize=500)

        self.info_canvas = tk.Canvas(canvas_container, bg=BG_CANVAS, highlightthickness=0)
        info_y_scroll = ttk.Scrollbar(canvas_container, orient="vertical", command=self.info_canvas.yview)
        info_x_scroll = ttk.Scrollbar(canvas_container, orient="horizontal", command=self.info_canvas.xview)

        self.info_canvas.configure(xscrollcommand=info_x_scroll.set, yscrollcommand=info_y_scroll.set)
        self.info_canvas.pack(side="left", fill="both", expand=True)
        info_y_scroll.pack(side="right", fill="y")
        info_x_scroll.pack(side="bottom", fill="x")

        # Right Blueprint Panel
        right_panel = tk.Frame(info_pane, bg=BG_PANEL, width=380)
        info_pane.add(right_panel, minsize=320)

        right_top = tk.Frame(right_panel, bg="#1e293b", height=36)
        right_top.pack(fill="x")
        tk.Label(
            right_top, text="📋 EXECUTIVE BLUEPRINT & DATA", font=("Segoe UI", 9, "bold"),
            fg=TEXT_MAIN, bg="#1e293b"
        ).pack(side="left", padx=12, pady=8)

        right_scroll_container = tk.Frame(right_panel, bg=BG_PANEL)
        right_scroll_container.pack(fill="both", expand=True)

        self.info_panel_canvas = tk.Canvas(right_scroll_container, bg=BG_PANEL, highlightthickness=0)
        panel_scroll = ttk.Scrollbar(right_scroll_container, orient="vertical", command=self.info_panel_canvas.yview)
        self.info_panel_frame = tk.Frame(self.info_panel_canvas, bg=BG_PANEL)

        self.info_panel_frame.bind(
            "<Configure>",
            lambda e: self.info_panel_canvas.configure(scrollregion=self.info_panel_canvas.bbox("all"))
        )
        self.info_panel_window = self.info_panel_canvas.create_window((0, 0), window=self.info_panel_frame, anchor="nw")
        self.info_panel_canvas.configure(yscrollcommand=panel_scroll.set)

        self.info_panel_canvas.bind(
            "<Configure>",
            lambda e: self.info_panel_canvas.itemconfig(self.info_panel_window, width=max(280, e.width - 10))
        )

        self.info_panel_canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        panel_scroll.pack(side="right", fill="y")

    def _on_infographic_tab_selected(self):
        if self.infographic_raw_pil:
            self._update_infographic_canvas()

    def _open_infographic_svg(self):
        w_num = ((self.current_day - 1) // 7) + 1
        if w_num > 52: w_num = 52
        day_dir = LEARNED_DIR / f"week-{w_num:02d}" / f"day-{self.current_day:03d}"
        svg_path = day_dir / "infographic.svg"
        if svg_path.exists():
            webbrowser.open(svg_path.resolve().as_uri())
            self.lbl_status.config(text=f"Opened {svg_path.name} in default browser.")
        else:
            messagebox.showinfo("SVG Vector File", f"No infographic.svg found for Day {self.current_day:03d}.\nGenerate it using the '⚡ NotebookLM' button.")

    def _render_infographic_view(self, learned_dir):
        """Loads infographic.png and infographic.json and updates view."""
        self.infographic_raw_pil = None
        self.infographic_photo = None
        self.infographic_data = None
        self.infographic_zoom = 0.75

        svg_path = learned_dir / "infographic.svg" if learned_dir else None
        png_path = learned_dir / "infographic.png" if learned_dir else None
        json_path = learned_dir / "infographic.json" if learned_dir else None

        if png_path and png_path.exists():
            try:
                self.infographic_raw_pil = Image.open(png_path)
            except Exception as e:
                print(f"Error opening infographic image: {e}")

        if json_path and json_path.exists():
            try:
                self.infographic_data = json.loads(json_path.read_text(encoding="utf-8", errors="replace"))
            except Exception as e:
                print(f"Error loading infographic.json: {e}")

        has_svg = svg_path and svg_path.exists()
        badge_text = " (Vector SVG & PNG)" if has_svg else ""
        self.lbl_info_title.config(text=f"🖼️ Executive Infographic{badge_text} · Day {self.current_day:03d}")

        if self.infographic_raw_pil:
            self._update_infographic_canvas()
        else:
            self._reset_infographic_view()

        self._populate_infographic_blueprint_panel()

    def _update_infographic_canvas(self):
        if not self.infographic_raw_pil:
            return
        orig_w, orig_h = self.infographic_raw_pil.size
        scaled_w = int(orig_w * self.infographic_zoom)
        scaled_h = int(orig_h * self.infographic_zoom)

        # Scale image with PIL
        resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
        resized = self.infographic_raw_pil.resize((scaled_w, scaled_h), resample_filter)
        self.infographic_photo = ImageTk.PhotoImage(resized)

        self.info_canvas.delete("all")
        self.info_canvas.create_image(10, 10, anchor="nw", image=self.infographic_photo)
        self.info_canvas.config(scrollregion=(0, 0, scaled_w + 20, scaled_h + 20))
        self.lbl_info_zoom.config(text=f"{int(self.infographic_zoom * 100)}%")

    def _zoom_infographic(self, factor: float):
        new_zoom = max(0.2, min(3.0, self.infographic_zoom * factor))
        self.infographic_zoom = new_zoom
        self._update_infographic_canvas()

    def _zoom_infographic_absolute(self, val: float):
        self.infographic_zoom = val
        self._update_infographic_canvas()

    def _fit_infographic_to_window(self):
        if not self.infographic_raw_pil:
            return
        canv_w = self.info_canvas.winfo_width() - 40
        if canv_w <= 100: canv_w = 700
        orig_w = self.infographic_raw_pil.width
        self.infographic_zoom = max(0.2, min(1.5, canv_w / orig_w))
        self._update_infographic_canvas()

    def _save_infographic_as(self):
        if not self.infographic_raw_pil:
            messagebox.showinfo("Infographic", "No infographic image available to save.")
            return
        initial_name = f"Day_{self.current_day:03d}_Aviation_Infographic.png"
        target_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Executive Infographic As",
            initialfile=initial_name,
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        if target_path:
            try:
                self.infographic_raw_pil.save(target_path, "PNG")
                messagebox.showinfo("Saved", f"Infographic exported successfully to:\n{target_path}")
            except Exception as e:
                messagebox.showerror("Error Saving", f"Failed to save image: {e}")

    def _populate_infographic_blueprint_panel(self):
        for widget in self.info_panel_frame.winfo_children():
            widget.destroy()

        if not self.infographic_data:
            tk.Label(
                self.info_panel_frame, text="No infographic data loaded.",
                font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL, pady=20
            ).pack()
            return

        data = self.infographic_data

        # Regulatory Anchor Badge
        reg_anchor = data.get("regulatory_anchor", "")
        if reg_anchor:
            reg_f = tk.Frame(self.info_panel_frame, bg="#061a1f", highlightthickness=1, highlightbackground=ACCENT_CYAN)
            reg_f.pack(fill="x", pady=(0, 10))
            tk.Label(
                reg_f, text=f"⚖️ REGULATORY ANCHOR:\n{reg_anchor}",
                font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg="#061a1f", justify="left", padx=10, pady=8
            ).pack(fill="x")

        # KPI Metrics
        kpis = data.get("kpi_metrics", [])
        if kpis:
            tk.Label(
                self.info_panel_frame, text="CORE PERFORMANCE INDICATORS",
                font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w"
            ).pack(fill="x", pady=(4, 6))

            colors = [ACCENT_CYAN, ACCENT_EMERALD, ACCENT_AMBER]
            for idx, k in enumerate(kpis):
                color = colors[idx % len(colors)]
                card = tk.Frame(self.info_panel_frame, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER)
                card.pack(fill="x", pady=4)
                tk.Label(
                    card, text=k.get("label", "Metric").upper(),
                    font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg="#0f172a", anchor="w"
                ).pack(fill="x", padx=10, pady=(6, 2))
                tk.Label(
                    card, text=str(k.get("value", "0")),
                    font=("Segoe UI", 16, "bold"), fg=color, bg="#0f172a", anchor="w"
                ).pack(fill="x", padx=10, pady=0)
                if k.get("subtext"):
                    tk.Label(
                        card, text=k.get("subtext", ""),
                        font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#0f172a", anchor="w"
                    ).pack(fill="x", padx=10, pady=(2, 6))

        # Four Pillars
        pillars = data.get("pillars", [])
        if pillars:
            tk.Label(
                self.info_panel_frame, text="OPERATIONAL & REGULATORY PILLARS",
                font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w"
            ).pack(fill="x", pady=(12, 6))

            for idx, p in enumerate(pillars):
                p_card = tk.Frame(self.info_panel_frame, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER)
                p_card.pack(fill="x", pady=4)
                hdr = tk.Frame(p_card, bg="#0f172a")
                hdr.pack(fill="x", padx=10, pady=(6, 2))
                tk.Label(
                    hdr, text=f"0{idx+1}", font=("Segoe UI", 8, "bold"),
                    fg=ACCENT_CYAN, bg="#1e293b", padx=6, pady=1
                ).pack(side="left")
                tk.Label(
                    hdr, text=p.get("title", f"Pillar {idx+1}")[:32], font=("Segoe UI", 9, "bold"),
                    fg=TEXT_MAIN, bg="#0f172a"
                ).pack(side="left", padx=6)
                tk.Label(
                    p_card, text=p.get("summary", ""), font=("Segoe UI", 8),
                    fg=TEXT_MUTED, bg="#0f172a", wraplength=320, justify="left", anchor="w"
                ).pack(fill="x", padx=10, pady=(2, 8))

        # Warning / Hazard Alert Box
        wb = data.get("warning_box", {})
        if wb:
            w_card = tk.Frame(self.info_panel_frame, bg="#271216", bd=1, relief="solid", highlightthickness=1, highlightbackground=ACCENT_RED)
            w_card.pack(fill="x", pady=(12, 6))
            tk.Label(
                w_card, text=f"⚠️ {wb.get('title', 'OPERATIONAL HAZARD')}",
                font=("Segoe UI", 9, "bold"), fg=ACCENT_RED, bg="#271216", anchor="w"
            ).pack(fill="x", padx=10, pady=(8, 4))
            tk.Label(
                w_card, text=wb.get("description", ""),
                font=("Segoe UI", 8), fg=TEXT_MAIN, bg="#271216", wraplength=320, justify="left", anchor="w"
            ).pack(fill="x", padx=10, pady=(0, 8))

        # Statutory Citations
        cits = data.get("statutory_citations", [])
        if cits:
            tk.Label(
                self.info_panel_frame, text="STATUTORY & AUDIT CITATIONS",
                font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w"
            ).pack(fill="x", pady=(12, 6))
            for cit in cits:
                tk.Label(
                    self.info_panel_frame, text=f"⚖️ {cit}", font=("Segoe UI", 8),
                    fg=TEXT_MUTED, bg=BG_PANEL, wraplength=320, justify="left", anchor="w"
                ).pack(fill="x", pady=2)

    def _reset_infographic_view(self):
        self.infographic_raw_pil = None
        self.infographic_photo = None
        self.infographic_data = None
        self.info_canvas.delete("all")
        self.info_canvas.create_text(
            300, 200,
            text=f"No Infographic generated for Day {self.current_day:03d}.\nClick '⚡ NotebookLM' in the toolbar to generate an infographic.",
            font=("Segoe UI", 11), fill=TEXT_MUTED, justify="center"
        )
        self._populate_infographic_blueprint_panel()

    # =========================================================================
    # TAB 10: NOTEBOOKLM VIDEO OVERVIEW PLAYER
    # =========================================================================

    def _build_video_tab(self, parent):
        top_bar = tk.Frame(parent, bg="#1e293b", height=50)
        top_bar.pack(fill="x")

        self.lbl_video_title = tk.Label(
            top_bar, text="🎬 Video Overview · Capt. Marcus Ross & Dr. Elena Vance",
            font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1e293b"
        )
        self.lbl_video_title.pack(side="left", padx=16, pady=8)

        self.lbl_video_host1 = tk.Label(
            top_bar, text="👨‍✈️ Capt. Marcus Ross", font=("Segoe UI", 8, "bold"),
            fg=ACCENT_CYAN, bg="#0f172a", padx=8, pady=3, bd=1, relief="solid"
        )
        self.lbl_video_host1.pack(side="left", padx=4, pady=8)

        self.lbl_video_host2 = tk.Label(
            top_bar, text="👩‍🔬 Dr. Elena Vance", font=("Segoe UI", 8, "bold"),
            fg=ACCENT_EMERALD, bg="#0f172a", padx=8, pady=3, bd=1, relief="solid"
        )
        self.lbl_video_host2.pack(side="left", padx=4, pady=8)

        # Audio Status & Mute Control
        self.lbl_video_audio_status = tk.Label(
            top_bar, text="🎙️ Dual-Voice Audio: Checking...", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED, bg="#0f172a", padx=8, pady=3, bd=1, relief="solid"
        )
        self.lbl_video_audio_status.pack(side="left", padx=8, pady=8)

        self.btn_toggle_audio = tk.Button(
            top_bar, text="🔊 Audio On", font=("Segoe UI", 8, "bold"),
            fg="#ffffff", bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2",
            command=self._toggle_audio_mute
        )
        self.btn_toggle_audio.pack(side="left", padx=4, pady=8)

        # Paned Window: Left Video Stage + Right Interactive Dialogue Transcript
        video_pane = tk.PanedWindow(parent, orient="horizontal", bg=BORDER, sashwidth=4, bd=0)
        video_pane.pack(fill="both", expand=True)

        # Left: Video Stage & Controls
        stage_frame = tk.Frame(video_pane, bg=BG_CANVAS)
        video_pane.add(stage_frame, minsize=520)

        # Video Canvas (720x500 aspect)
        canvas_box = tk.Frame(stage_frame, bg=BG_CANVAS)
        canvas_box.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        self.video_canvas = tk.Canvas(canvas_box, bg=BG_CANVAS, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        self.video_canvas.pack(fill="both", expand=True)

        # Transport Controls Bar
        transport = tk.Frame(stage_frame, bg="#0f172a", height=60, bd=1, relief="solid")
        transport.pack(fill="x", padx=16, pady=(0, 16))

        t_row1 = tk.Frame(transport, bg="#0f172a")
        t_row1.pack(fill="x", padx=16, pady=(8, 4))

        self.btn_video_play = tk.Button(
            t_row1, text="▶ Play", font=("Segoe UI", 9, "bold"),
            fg="#ffffff", bg=ACCENT_CYAN, activebackground="#0891b2", activeforeground="#ffffff",
            bd=0, padx=14, pady=3, cursor="hand2", command=self._toggle_video_playback
        )
        self.btn_video_play.pack(side="left", padx=(0, 6))

        btn_restart = tk.Button(
            t_row1, text="⏮️ Restart", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#334155", activebackground="#475569", activeforeground="#ffffff",
            bd=1, relief="solid", padx=8, pady=3, cursor="hand2", command=self._restart_video
        )
        btn_restart.pack(side="left", padx=4)

        # Scrubber Slider
        self.video_scrubber = ttk.Scale(
            t_row1, from_=0, to=10, orient="horizontal",
            command=self._on_scrubber_slide
        )
        self.video_scrubber.pack(side="left", fill="x", expand=True, padx=12)

        self.lbl_video_time = tk.Label(
            t_row1, text="00:00 / 00:00", font=("Segoe UI", 9, "bold"),
            fg=ACCENT_CYAN, bg="#0f172a"
        )
        self.lbl_video_time.pack(side="right", padx=(6, 0))

        # Speed Selector
        speed_box = tk.Frame(transport, bg="#0f172a")
        speed_box.pack(fill="x", padx=16, pady=(0, 6))
        tk.Label(speed_box, text="Speed:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#0f172a").pack(side="left", padx=4)

        for spd in [1.0, 1.25, 1.5]:
            btn_spd = tk.Button(
                speed_box, text=f"{spd}x", font=("Segoe UI", 7, "bold"),
                fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
                bd=1, relief="solid", padx=6, pady=1, cursor="hand2",
                command=lambda s=spd: self._set_video_speed(s)
            )
            btn_spd.pack(side="left", padx=2)

        self.lbl_active_speaker_bar = tk.Label(
            speed_box, text="Marcus & Elena Dual-Host Briefing · Chapter Infographics Synchronized", font=("Segoe UI", 8),
            fg=TEXT_MUTED, bg="#0f172a"
        )
        self.lbl_active_speaker_bar.pack(side="right")

        # Right: Interactive Dialogue Transcript & Segments Panel
        transcript_panel = tk.Frame(video_pane, bg=BG_PANEL, width=440)
        video_pane.add(transcript_panel, minsize=360)

        tr_top = tk.Frame(transcript_panel, bg="#1e293b", height=36)
        tr_top.pack(fill="x")
        tk.Label(
            tr_top, text="📜 INTERACTIVE DIALOGUE & CHAPTER BLUEPRINTS", font=("Segoe UI", 9, "bold"),
            fg=TEXT_MAIN, bg="#1e293b"
        ).pack(side="left", padx=12, pady=8)

        tr_container = tk.Frame(transcript_panel, bg=BG_PANEL)
        tr_container.pack(fill="both", expand=True)

        self.video_tr_canvas = tk.Canvas(tr_container, bg=BG_PANEL, highlightthickness=0)
        tr_scroll = ttk.Scrollbar(tr_container, orient="vertical", command=self.video_tr_canvas.yview)
        self.video_tr_frame = tk.Frame(self.video_tr_canvas, bg=BG_PANEL)

        self.video_tr_frame.bind(
            "<Configure>",
            lambda e: self.video_tr_canvas.configure(scrollregion=self.video_tr_canvas.bbox("all"))
        )
        self.video_tr_window = self.video_tr_canvas.create_window((0, 0), window=self.video_tr_frame, anchor="nw")
        self.video_tr_canvas.configure(yscrollcommand=tr_scroll.set)

        self.video_tr_canvas.bind(
            "<Configure>",
            lambda e: self.video_tr_canvas.itemconfig(self.video_tr_window, width=max(320, e.width - 10))
        )

        self.video_tr_canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        tr_scroll.pack(side="right", fill="y")

    def _on_video_tab_selected(self):
        if self.video_frames:
            self._display_video_frame(self.video_frame_idx)

    def _render_video_view(self, learned_dir):
        """Loads video_overview.webp, video_overview.json, and video_overview.wav."""
        self._stop_video_playback()
        self.video_data = None
        self.video_frames = []
        self.video_frame_durations = []
        self.video_frame_idx = 0
        self.video_wav_path = None
        self.video_audio_available = False
        self.video_audio_playing = False
        self.video_audio_duration_sec = 0.0

        json_path = learned_dir / "video_overview.json" if learned_dir else None
        webp_path = learned_dir / "video_overview.webp" if learned_dir else None
        wav_path = learned_dir / "video_overview.wav" if learned_dir else None

        if json_path and json_path.exists():
            try:
                self.video_data = json.loads(json_path.read_text(encoding="utf-8", errors="replace"))
            except Exception as e:
                print(f"Error loading video_overview.json: {e}")

        if webp_path and webp_path.exists():
            try:
                im = Image.open(webp_path)
                for frame in ImageSequence.Iterator(im):
                    fr_conv = frame.copy().convert("RGB")
                    self.video_frames.append(ImageTk.PhotoImage(fr_conv))
                    duration = frame.info.get("duration", 1200)
                    self.video_frame_durations.append(max(200, duration))
            except Exception as e:
                print(f"Error extracting video frames: {e}")

        # Audio Track Verification
        if wav_path and wav_path.exists():
            self.video_wav_path = wav_path
            self.video_audio_available = True
            try:
                with wave.open(str(wav_path), "rb") as wf:
                    self.video_audio_duration_sec = wf.getnframes() / float(wf.getframerate())
            except Exception:
                self.video_audio_duration_sec = self.video_data.get("estimated_duration_sec", 60) if self.video_data else 60
            self.lbl_video_audio_status.config(
                text="🎙️ Dual-Voice Audio: Active (Capt. Marcus & Dr. Elena Vance)",
                fg=ACCENT_EMERALD
            )
        else:
            self.video_wav_path = None
            self.video_audio_available = False
            self.video_audio_duration_sec = self.video_data.get("estimated_duration_sec", 60) if self.video_data else 60
            self.lbl_video_audio_status.config(
                text="Visual Only (Audio Not Generated)",
                fg=TEXT_MUTED
            )

        self._populate_video_transcript_panel()

        total_frames = len(self.video_frames)
        if total_frames > 0:
            self.video_scrubber.config(from_=0, to=total_frames - 1)
            self._display_video_frame(0)
        else:
            self._reset_video_view()

    def _display_video_frame(self, idx: int, elapsed_override: float = None):
        if not self.video_frames:
            return
        if idx < 0: idx = 0
        if idx >= len(self.video_frames): idx = len(self.video_frames) - 1
        self.video_frame_idx = idx

        # Draw frame on canvas centered
        self.video_canvas.delete("all")
        photo = self.video_frames[idx]
        cw = self.video_canvas.winfo_width()
        ch = self.video_canvas.winfo_height()
        if cw <= 10: cw = 720
        if ch <= 10: ch = 500
        x = max(0, (cw - photo.width()) // 2)
        y = max(0, (ch - photo.height()) // 2)
        self.video_canvas.create_image(x, y, anchor="nw", image=photo)

        # Update scrubber position
        self.video_scrubber.set(idx)

        # Update timecode
        tot_sec = int(self.video_audio_duration_sec) if self.video_audio_duration_sec > 0 else (len(self.video_frames) * 2)
        if elapsed_override is not None:
            cur_sec = int(elapsed_override)
        else:
            cur_sec = int((idx / max(1, len(self.video_frames) - 1)) * tot_sec)

        cur_str = f"{cur_sec // 60:02d}:{cur_sec % 60:02d}"
        tot_str = f"{tot_sec // 60:02d}:{tot_sec % 60:02d}"
        self.lbl_video_time.config(text=f"{cur_str} / {tot_str}")

        # Highlight corresponding dialogue turn
        self._highlight_dialogue_turn_for_frame(idx, cur_sec=cur_sec)

    def _toggle_video_playback(self):
        if self.video_is_playing:
            self._pause_video_playback()
        else:
            self._start_video_playback()

    def _start_video_playback(self):
        if not self.video_frames:
            return
        self.video_is_playing = True
        self.btn_video_play.config(text="⏸️ Pause", bg=ACCENT_AMBER)

        # Audio Playback with Windows SAPI
        if self.video_audio_available and not self.video_audio_muted and HAS_WINSOUND:
            try:
                winsound.PlaySound(str(self.video_wav_path), winsound.SND_ASYNC | winsound.SND_FILENAME)
                self.video_audio_playing = True
            except Exception as e:
                print(f"Audio playback error: {e}")
                self.video_audio_playing = False
        else:
            self.video_audio_playing = False

        self.video_start_time = time.time()
        self._step_video_frame()

    def _pause_video_playback(self):
        self.video_is_playing = False
        self.btn_video_play.config(text="▶ Play", bg=ACCENT_CYAN)
        if self.video_play_job:
            self.after_cancel(self.video_play_job)
            self.video_play_job = None
        if self.video_audio_playing and HAS_WINSOUND:
            try:
                winsound.PlaySound(None, 0)
            except Exception:
                pass
            self.video_audio_playing = False

    def _stop_video_playback(self):
        self._pause_video_playback()
        self.video_frame_idx = 0
        if self.video_frames:
            self._display_video_frame(0)

    def _restart_video(self):
        self._stop_video_playback()
        self._start_video_playback()

    def _step_video_frame(self):
        if not self.video_is_playing or not self.video_frames:
            return

        if self.video_audio_playing and self.video_audio_duration_sec > 0:
            elapsed = (time.time() - self.video_start_time) * self.video_playback_speed
            if elapsed >= self.video_audio_duration_sec:
                self._stop_video_playback()
                return

            dialogues = self.video_data.get("dialogue", []) if self.video_data else []
            active_turn_idx = 0
            for d_i, d in enumerate(dialogues):
                ts_str = d.get("timestamp", "00:00")
                try:
                    parts = ts_str.split(":")
                    turn_sec = int(parts[0]) * 60 + int(parts[1])
                    if turn_sec <= elapsed:
                        active_turn_idx = d_i
                    else:
                        break
                except Exception:
                    pass

            sub_f = int((elapsed * 2) % 2)
            frame_idx = min(len(self.video_frames) - 1, active_turn_idx * 2 + sub_f)
            self._display_video_frame(frame_idx, elapsed_override=elapsed)
            self.video_play_job = self.after(100, self._step_video_frame)
        else:
            self._display_video_frame(self.video_frame_idx)
            delay = 1200
            if self.video_frame_durations and self.video_frame_idx < len(self.video_frame_durations):
                delay = int(self.video_frame_durations[self.video_frame_idx] / self.video_playback_speed)
            self.video_frame_idx = (self.video_frame_idx + 1) % len(self.video_frames)
            self.video_play_job = self.after(delay, self._step_video_frame)

    def _on_scrubber_slide(self, val):
        idx = int(float(val))
        if idx != self.video_frame_idx:
            self._display_video_frame(idx)

    def _set_video_speed(self, spd: float):
        self.video_playback_speed = spd
        self.lbl_status.config(text=f"Video playback speed set to {spd}x")

    def _toggle_audio_mute(self):
        self.video_audio_muted = not self.video_audio_muted
        if self.video_audio_muted:
            self.btn_toggle_audio.config(text="🔇 Muted", bg="#475569")
            if self.video_audio_playing and HAS_WINSOUND:
                try:
                    winsound.PlaySound(None, 0)
                except Exception:
                    pass
        else:
            self.btn_toggle_audio.config(text="🔊 Audio On", bg="#334155")
            if self.video_is_playing and self.video_audio_available and HAS_WINSOUND:
                try:
                    winsound.PlaySound(str(self.video_wav_path), winsound.SND_ASYNC | winsound.SND_FILENAME)
                    self.video_audio_playing = True
                    self.video_start_time = time.time() - (self.video_frame_idx / max(1, len(self.video_frames) - 1)) * self.video_audio_duration_sec
                except Exception:
                    pass

    def _seek_video_to_timestamp(self, ts_str: str):
        """Seeks video frame closest to timestamp like '01:30'."""
        try:
            parts = ts_str.split(":")
            sec = int(parts[0]) * 60 + int(parts[1])
            dialogues = self.video_data.get("dialogue", []) if self.video_data else []
            target_turn = 0
            for d_i, d in enumerate(dialogues):
                d_ts = d.get("timestamp", "00:00")
                p = d_ts.split(":")
                d_sec = int(p[0]) * 60 + int(p[1])
                if d_sec <= sec:
                    target_turn = d_i
                else:
                    break
            target_idx = min(len(self.video_frames) - 1, target_turn * 2)
            self._display_video_frame(target_idx, elapsed_override=sec)
            if self.video_is_playing and self.video_audio_available and HAS_WINSOUND:
                self.video_start_time = time.time() - sec
                try:
                    winsound.PlaySound(str(self.video_wav_path), winsound.SND_ASYNC | winsound.SND_FILENAME)
                except Exception:
                    pass
        except Exception as e:
            print(f"Seek error: {e}")
            pass

    def _populate_video_transcript_panel(self):
        for widget in self.video_tr_frame.winfo_children():
            widget.destroy()

        if not self.video_data:
            tk.Label(
                self.video_tr_frame, text="No video transcript available.",
                font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL, pady=20
            ).pack()
            return

        # Chapter Segments Accordion
        segments = self.video_data.get("segments", [])
        if segments:
            tk.Label(
                self.video_tr_frame, text="VIDEO CHAPTERS & TOPICS",
                font=("Segoe UI", 8, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL, anchor="w"
            ).pack(fill="x", pady=(4, 6))

            seg_box = tk.Frame(self.video_tr_frame, bg="#0f172a", bd=1, relief="solid")
            seg_box.pack(fill="x", pady=(0, 10))

            for s in segments:
                row = tk.Frame(seg_box, bg="#0f172a")
                row.pack(fill="x", padx=8, pady=3)
                ts = s.get("timestamp_start", "00:00")
                btn_ts = tk.Button(
                    row, text=f"⏱️ {ts}", font=("Segoe UI", 8, "bold"),
                    fg=ACCENT_CYAN, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
                    bd=0, padx=6, pady=1, cursor="hand2",
                    command=lambda t=ts: self._seek_video_to_timestamp(t)
                )
                btn_ts.pack(side="left", padx=(0, 6))
                tk.Label(
                    row, text=s.get("segment_title", ""), font=("Segoe UI", 9),
                    fg=TEXT_MAIN, bg="#0f172a", anchor="w"
                ).pack(side="left", fill="x", expand=True)

        # Full Dialogue Script
        dialogues = self.video_data.get("dialogue", [])
        if dialogues:
            tk.Label(
                self.video_tr_frame, text="VERBATIM TECHNICAL DIALOGUE",
                font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w"
            ).pack(fill="x", pady=(8, 6))

            self.dialogue_turn_widgets = []
            for d_idx, d in enumerate(dialogues):
                spk = d.get("speaker", "Marcus")
                is_marcus = "marcus" in spk.lower()
                border_col = ACCENT_CYAN if is_marcus else ACCENT_EMERALD
                spk_color = ACCENT_CYAN if is_marcus else ACCENT_EMERALD
                spk_label = "👨‍✈️ Capt. Marcus Ross" if is_marcus else "👩‍🔬 Dr. Elena Vance"

                card = tk.Frame(self.video_tr_frame, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER)
                card.pack(fill="x", pady=4)
                self.dialogue_turn_widgets.append((d.get("timestamp", "00:00"), card))

                c_top = tk.Frame(card, bg="#0f172a")
                c_top.pack(fill="x", padx=10, pady=(6, 2))

                ts = d.get("timestamp", "00:00")
                btn_d_ts = tk.Button(
                    c_top, text=f"[{ts}]", font=("Segoe UI", 8, "bold"),
                    fg=TEXT_MUTED, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
                    bd=0, padx=5, pady=1, cursor="hand2",
                    command=lambda t=ts: self._seek_video_to_timestamp(t)
                )
                btn_d_ts.pack(side="left", padx=(0, 6))

                tk.Label(
                    c_top, text=spk_label, font=("Segoe UI", 9, "bold"),
                    fg=spk_color, bg="#0f172a"
                ).pack(side="left")

                tk.Label(
                    card, text=d.get("text", ""), font=("Segoe UI", 9),
                    fg=TEXT_MAIN, bg="#0f172a", wraplength=360, justify="left", anchor="w"
                ).pack(fill="x", padx=10, pady=(2, 6))

    def _highlight_dialogue_turn_for_frame(self, frame_idx: int, cur_sec: int = None):
        if not hasattr(self, "dialogue_turn_widgets") or not self.dialogue_turn_widgets:
            return
        if cur_sec is None:
            tot_sec = int(self.video_audio_duration_sec) if getattr(self, "video_audio_duration_sec", 0) > 0 else (len(self.video_frames) * 2)
            cur_sec = int((frame_idx / max(1, len(self.video_frames) - 1)) * tot_sec)

        active_w = None
        for ts, widget in self.dialogue_turn_widgets:
            try:
                if not widget.winfo_exists():
                    continue
                parts = ts.split(":")
                sec = int(parts[0]) * 60 + int(parts[1])
                if sec <= cur_sec:
                    active_w = widget
                else:
                    break
            except Exception:
                continue

        for ts, widget in self.dialogue_turn_widgets:
            try:
                if not widget.winfo_exists():
                    continue
                if widget == active_w:
                    widget.config(highlightbackground=ACCENT_CYAN, highlightthickness=2)
                else:
                    widget.config(highlightbackground=BORDER, highlightthickness=1)
            except Exception:
                pass

    def _reset_video_view(self):
        self._stop_video_playback()
        self.video_data = None
        self.video_frames = []
        self.video_frame_durations = []
        self.video_frame_idx = 0
        self.video_canvas.delete("all")
        self.video_canvas.create_text(
            360, 220,
            text=f"No Video Overview generated for Day {self.current_day:03d}.\nClick '⚡ NotebookLM' in the toolbar to generate a video overview.",
            font=("Segoe UI", 11), fill=TEXT_MUTED, justify="center"
        )
        self.video_scrubber.config(from_=0, to=0)
        self.lbl_video_time.config(text="00:00 / 00:00")
        self._populate_video_transcript_panel()

    # =========================================================================
    # NOTEBOOKLM GENERATION MODAL DIALOG
    # =========================================================================

    def _open_notebooklm_dialog(self):
        """Displays the NotebookLM Artifacts Studio generator modal."""
        dialog = tk.Toplevel(self)
        dialog.title("⚡ Aviation 365: NotebookLM Studio Engine")
        dialog.geometry("780x620")
        dialog.minsize(700, 520)
        dialog.configure(bg=BG_PANEL)
        dialog.transient(self)
        dialog.grab_set()

        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 390
            y = self.winfo_y() + (self.winfo_height() // 2) - 310
            dialog.geometry(f"780x620+{max(30, x)}+{max(30, y)}")
        except Exception:
            pass

        # Header
        header = tk.Frame(dialog, bg="#1e293b", height=60, bd=0, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        header.pack(fill="x")

        hdr_left = tk.Frame(header, bg="#1e293b")
        hdr_left.pack(side="left", padx=20, pady=10)

        tk.Label(hdr_left, text="⚡ NotebookLM Studio Engine", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#1e293b").pack(anchor="w")
        tk.Label(hdr_left, text="Synthesize executive Slide Decks, high-res Infographics, and dual-host Video Overviews.",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w")

        d_num = self.current_day
        tk.Label(header, text=f"DAY {d_num:03d}", font=("Segoe UI", 10, "bold"),
                 fg="#090d16", bg=ACCENT_CYAN, padx=10, pady=4).pack(side="right", padx=20, pady=12)

        # Status of Artifacts Frame
        status_box = tk.Frame(dialog, bg=BG_PANEL)
        status_box.pack(fill="x", padx=20, pady=14)

        tk.Label(status_box, text="CURRENT ARTIFACT AVAILABILITY FOR TODAY", font=("Segoe UI", 8, "bold"),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(0, 6))

        w_num = ((d_num - 1) // 7) + 1
        if w_num > 52: w_num = 52
        day_dir = LEARNED_DIR / f"week-{w_num:02d}" / f"day-{d_num:03d}"

        has_slides = (day_dir / "slides.json").exists() or (day_dir / "slides.md").exists()
        has_info = (day_dir / "infographic.svg").exists() or (day_dir / "infographic.png").exists() or (day_dir / "infographic.json").exists()
        has_video = (day_dir / "video_overview.wav").exists() or (day_dir / "video_overview.webp").exists() or (day_dir / "video_overview.json").exists()

        cards_frame = tk.Frame(status_box, bg=BG_PANEL)
        cards_frame.pack(fill="x")

        def make_stat_card(parent, title, fname, exists):
            c = tk.Frame(parent, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER)
            c.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg="#0f172a").pack(padx=10, pady=(8, 2))
            tk.Label(c, text=fname, font=("Segoe UI", 7), fg=TEXT_MUTED, bg="#0f172a").pack(padx=10, pady=(0, 4))
            status_text = "✅ Available" if exists else "⚪ Missing"
            status_col = ACCENT_EMERALD if exists else TEXT_MUTED
            tk.Label(c, text=status_text, font=("Segoe UI", 8, "bold"), fg=status_col, bg="#0f172a").pack(padx=10, pady=(0, 8))
            return c

        make_stat_card(cards_frame, "📽️ Slide Deck", "slides.json / .md", has_slides)
        make_stat_card(cards_frame, "🖼️ Infographic", "infographic.svg / .png", has_info)
        make_stat_card(cards_frame, "🎬 Video & Audio", "video.webp / .wav", has_video)

        # Grounding & Strict Prompting Notice
        notice_box = tk.Frame(dialog, bg="#061a1f", highlightthickness=1, highlightbackground=ACCENT_CYAN)
        notice_box.pack(fill="x", padx=24, pady=10)
        tk.Label(
            notice_box,
            text="🔒 STRICT GROUNDING GUARANTEE:\nArtifacts are synthesized strictly from Day " + f"{d_num:03d}'s README.md, technical analysis, math formulas, and architecture canvas. Structured outputs enforce valid Pydantic schemas with zero hallucination.",
            font=("Segoe UI", 8), fg=ACCENT_CYAN, bg="#061a1f", justify="left", padx=12, pady=8
        ).pack(fill="x")

        # Action Buttons
        btn_frame = tk.Frame(dialog, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=24, pady=10)

        buttons = []

        btn_all = tk.Button(
            btn_frame, text="⚡ Generate Full Suite (All 3 Artifacts)", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg="#7c3aed", activebackground="#6d28d9", activeforeground="#ffffff",
            bd=0, padx=16, pady=8, cursor="hand2"
        )
        btn_all.pack(fill="x", pady=4)
        buttons.append(btn_all)

        sub_btns = tk.Frame(btn_frame, bg=BG_PANEL)
        sub_btns.pack(fill="x", pady=4)

        btn_s = tk.Button(
            sub_btns, text="📽️ Generate Slide Deck", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
            bd=1, relief="solid", padx=10, pady=6, cursor="hand2"
        )
        btn_s.pack(side="left", fill="x", expand=True, padx=2)
        buttons.append(btn_s)

        btn_i = tk.Button(
            sub_btns, text="🖼️ Generate Infographic", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
            bd=1, relief="solid", padx=10, pady=6, cursor="hand2"
        )
        btn_i.pack(side="left", fill="x", expand=True, padx=2)
        buttons.append(btn_i)

        btn_v = tk.Button(
            sub_btns, text="🎬 Generate Video Overview", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MAIN, bg="#1e293b", activebackground="#334155", activeforeground="#ffffff",
            bd=1, relief="solid", padx=10, pady=6, cursor="hand2"
        )
        btn_v.pack(side="left", fill="x", expand=True, padx=2)
        buttons.append(btn_v)

        # Progress indicator & Live Status
        prog_frame = tk.Frame(dialog, bg=BG_PANEL)
        prog_frame.pack(fill="x", padx=24, pady=10)

        pbar = ttk.Progressbar(prog_frame, mode="indeterminate")
        pbar.pack(fill="x", pady=4)

        lbl_gen_status = tk.Label(
            prog_frame, text="Ready · Select an artifact generation target above",
            font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL
        )
        lbl_gen_status.pack(pady=4)

        btn_all.config(command=lambda: self._start_notebooklm_generation(["all"], lbl_gen_status, pbar, buttons, dialog))
        btn_s.config(command=lambda: self._start_notebooklm_generation(["slides"], lbl_gen_status, pbar, buttons, dialog))
        btn_i.config(command=lambda: self._start_notebooklm_generation(["infographic"], lbl_gen_status, pbar, buttons, dialog))
        btn_v.config(command=lambda: self._start_notebooklm_generation(["video"], lbl_gen_status, pbar, buttons, dialog))

    def _start_notebooklm_generation(self, targets: list, status_lbl, pbar, btn_list, dialog):
        if not self.gemini_key or not self.gemini_client:
            messagebox.showwarning("Gemini Required", "A valid Gemini API key is required to synthesize NotebookLM artifacts.\nClick '🔑 Set Gemini Key' in the toolbar.", parent=dialog)
            return

        for b in btn_list:
            b.config(state="disabled")
        pbar.start(10)
        status_lbl.config(text="Synthesizing with Gemini & Pydantic structured schemas...", fg=ACCENT_CYAN)

        def worker():
            def cb(msg):
                self.after(0, lambda m=msg: status_lbl.config(text=m, fg=ACCENT_CYAN))

            try:
                res = notebooklm_studio.generate_notebooklm_artifacts_for_day(
                    day_num=self.current_day,
                    root_dir=ROOT_DIR,
                    client=self.gemini_client,
                    model=self.gemini_model,
                    progress_callback=cb,
                    targets=targets
                )
                self.after(0, lambda: self._on_notebooklm_generation_complete(res, status_lbl, pbar, btn_list, dialog, targets))
            except Exception as e:
                err_msg = str(e)
                self.after(0, lambda: self._on_notebooklm_generation_error(err_msg, status_lbl, pbar, btn_list))

        threading.Thread(target=worker, daemon=True).start()

    def _on_notebooklm_generation_complete(self, results, status_lbl, pbar, btn_list, dialog, targets):
        pbar.stop()
        for b in btn_list:
            b.config(state="normal")
        status_lbl.config(text="✅ Artifact synthesis complete!", fg=ACCENT_EMERALD)

        # Refresh day to re-scan files and enable tabs
        self.load_day(self.current_day)

        # Auto-switch to newly generated tab
        if "slides" in targets:
            self._select_tab_if_enabled(self.tab_slides)
        elif "infographic" in targets:
            self._select_tab_if_enabled(self.tab_infographic)
        elif "video" in targets:
            self._select_tab_if_enabled(self.tab_video)
        elif "all" in targets:
            self._select_tab_if_enabled(self.tab_slides)

        messagebox.showinfo(
            "Generation Complete",
            f"NotebookLM artifacts successfully synthesized for Day {self.current_day:03d}!\nThe corresponding studio tabs have been enabled.",
            parent=dialog
        )
        try:
            dialog.destroy()
        except Exception:
            pass

    def _on_notebooklm_generation_error(self, err_msg, status_lbl, pbar, btn_list):
        pbar.stop()
        for b in btn_list:
            b.config(state="normal")
        status_lbl.config(text=f"❌ Error: {err_msg[:60]}...", fg=ACCENT_RED)
        messagebox.showerror("Synthesis Error", f"Failed to generate artifacts:\n{err_msg}")

    # =========================================================================
    # CURRICULUM & LESSON SUITE GENERATOR FROM SYLLABUS PLANS
    # =========================================================================

    def _on_tree_right_click(self, event):
        """Displays contextual right-click actions on curriculum tree nodes."""
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        item = self.tree.item(item_id)
        values = item.get("values", [])

        menu = tk.Menu(self, tearoff=0, bg="#0f172a", fg=TEXT_MAIN,
                       activebackground=ACCENT_CYAN, activeforeground="#090d16", font=("Segoe UI", 9))

        if values and len(values) > 0:
            val_str = str(values[0])
            if val_str.isdigit():
                day_num = int(val_str)
                menu.add_command(
                    label=f"🌱 Generate Lesson Suite for Day {day_num:03d} from Plan...",
                    command=lambda d=day_num: self._open_lesson_generator_dialog(initial_day=d)
                )
                menu.add_command(
                    label=f"⚡ Generate NotebookLM Suite for Day {day_num:03d}...",
                    command=lambda d=day_num: self._open_notebooklm_for_day(d)
                )
                menu.add_separator()
                menu.add_command(
                    label=f"📖 Load Day {day_num:03d}",
                    command=lambda d=day_num: self.load_day(d)
                )
            elif val_str.startswith("week-") or len(values) > 1:
                w_num = int(values[1]) if len(values) > 1 else int(val_str.replace("week-", ""))
                menu.add_command(
                    label=f"🌱 Generate Entire Week {w_num:02d} (All 7 Days) from Plans...",
                    command=lambda w=w_num: self._open_lesson_generator_dialog(initial_week=w)
                )
                menu.add_command(
                    label=f"🌱 Generate Only Missing Days in Week {w_num:02d}...",
                    command=lambda w=w_num: self._open_lesson_generator_dialog(initial_week=w, only_missing=True)
                )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _open_notebooklm_for_day(self, day_num: int):
        """Loads a specific day and immediately opens the NotebookLM Studio modal."""
        self.load_day(day_num)
        self._open_notebooklm_dialog()

    def _open_lesson_generator_dialog(self, initial_day=None, initial_week=None, only_missing=False):
        """Displays the Autonomous Curriculum & Lesson Suite Generator modal dialog."""
        if not GENAI_AVAILABLE:
            messagebox.showerror(
                "Gemini SDK Not Found",
                "The 'google-genai' library is required to synthesize lessons with Gemini.\n\n"
                "Please install it in your environment:\n"
                "  pip install google-genai"
            )
            return

        if not self.gemini_key:
            env_key = os.environ.get("GEMINI_API_KEY", "").strip()
            if env_key:
                self.gemini_key = env_key
                self._init_gemini_client()
            else:
                self._open_gemini_key_dialog()
                if not self.gemini_key:
                    messagebox.showwarning(
                        "API Key Required",
                        "Please configure your Gemini API Key in settings to generate lessons from syllabus plans."
                    )
                    return

        dialog = tk.Toplevel(self)
        dialog.title("🌱 Aviation 365: Curriculum & Lesson Suite Generator")
        dialog.geometry("860x700")
        dialog.minsize(780, 600)
        dialog.configure(bg=BG_PANEL)
        dialog.transient(self)
        dialog.grab_set()

        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 430
            y = self.winfo_y() + (self.winfo_height() // 2) - 350
            dialog.geometry(f"860x700+{max(30, x)}+{max(30, y)}")
        except Exception:
            pass

        # Top Header Bar
        header = tk.Frame(dialog, bg="#1e293b", height=65, bd=0, highlightthickness=1, highlightbackground=BORDER_BRIGHT)
        header.pack(fill="x")

        hdr_left = tk.Frame(header, bg="#1e293b")
        hdr_left.pack(side="left", padx=20, pady=10)

        tk.Label(hdr_left, text="🌱 Autonomous Lesson & Curriculum Generator", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#1e293b").pack(anchor="w")
        tk.Label(hdr_left, text="Grounds lesson creation strictly in official syllabus plans, generating lessons, technical analyses, code, and canvases.",
                 font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#1e293b").pack(anchor="w")

        arch_name = self.student_profile.get("archetype", "🛠️ Hands-On Systems Builder")
        tk.Label(header, text=f"🎯 {arch_name}", font=("Segoe UI", 9, "bold"),
                 fg=ACCENT_CYAN, bg="#0f172a", padx=10, pady=4, bd=1, relief="solid").pack(side="right", padx=20, pady=14)

        # Main Body Notebook/Panels
        body = tk.Frame(dialog, bg=BG_PANEL)
        body.pack(fill="both", expand=True, padx=20, pady=12)

        # 1. Scope Selector Frame
        scope_box = tk.LabelFrame(body, text=" 1. TARGET SCOPE & SYLLABUS CONTRACT ", font=("Segoe UI", 8, "bold"),
                                  fg=TEXT_MUTED, bg=BG_PANEL, bd=1, relief="solid")
        scope_box.pack(fill="x", pady=(0, 10), ipady=4)

        cur_day = initial_day or self.current_day
        cur_week = initial_week or (((cur_day - 1) // 7) + 1)
        if cur_week > 52: cur_week = 52

        scope_var = tk.StringVar(value="week" if initial_week is not None else "day")

        row1 = tk.Frame(scope_box, bg=BG_PANEL)
        row1.pack(fill="x", padx=14, pady=3)

        rb_day = tk.Radiobutton(row1, text="Single Day:", variable=scope_var, value="day",
                                font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_PANEL,
                                activebackground=BG_PANEL, activeforeground=ACCENT_CYAN, selectcolor="#1e293b")
        rb_day.pack(side="left")

        spin_target_day = tk.Spinbox(row1, from_=1, to=365, width=6, font=("Segoe UI", 9, "bold"),
                                     bg=BG_CODE, fg=ACCENT_CYAN, buttonbackground="#1e293b", bd=1, relief="solid")
        spin_target_day.delete(0, "end")
        spin_target_day.insert(0, str(cur_day))
        spin_target_day.pack(side="left", padx=(6, 16))

        rb_week = tk.Radiobutton(row1, text="Entire Week (7 Days):", variable=scope_var, value="week",
                                 font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_PANEL,
                                 activebackground=BG_PANEL, activeforeground=ACCENT_CYAN, selectcolor="#1e293b")
        rb_week.pack(side="left")

        week_options = [f"Week {w:02d} (Days {(w-1)*7+1:03d}–{min(365, w*7):03d})" for w in range(1, 53)]
        combo_target_week = ttk.Combobox(row1, values=week_options, state="readonly", width=30)
        combo_target_week.current(cur_week - 1)
        combo_target_week.pack(side="left", padx=(6, 16))

        var_only_missing = tk.BooleanVar(value=only_missing)
        chk_missing = tk.Checkbutton(row1, text="Generate only missing days in week", variable=var_only_missing,
                                     font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL, activebackground=BG_PANEL,
                                     activeforeground=TEXT_MAIN, selectcolor="#1e293b")
        chk_missing.pack(side="left")

        # 2. Options Frame
        opts_box = tk.LabelFrame(body, text=" 2. ARTIFACT SUITE OPTIONS ", font=("Segoe UI", 8, "bold"),
                                 fg=TEXT_MUTED, bg=BG_PANEL, bd=1, relief="solid")
        opts_box.pack(fill="x", pady=(0, 10), ipady=4)

        opt_row = tk.Frame(opts_box, bg=BG_PANEL)
        opt_row.pack(fill="x", padx=14, pady=3)

        var_canvas = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_row, text="🗺️ Architecture Canvas (architecture.mermaid)", variable=var_canvas,
                       font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_PANEL, activebackground=BG_PANEL,
                       activeforeground=TEXT_MAIN, selectcolor="#1e293b").pack(side="left", padx=(0, 20))

        var_notebooklm = tk.BooleanVar(value=False)
        tk.Checkbutton(opt_row, text="⚡ NotebookLM Suite (Slides, Infographic, Video Overview)", variable=var_notebooklm,
                       font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_PANEL, activebackground=BG_PANEL,
                       activeforeground=TEXT_MAIN, selectcolor="#1e293b").pack(side="left", padx=(0, 20))

        var_overwrite = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_row, text="🔁 Overwrite existing files", variable=var_overwrite,
                       font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_PANEL, activebackground=BG_PANEL,
                       activeforeground=TEXT_MAIN, selectcolor="#1e293b").pack(side="left")

        # 3. Plan Preview & Summary Box
        info_frame = tk.Frame(body, bg="#0f172a", bd=1, relief="solid", highlightthickness=1, highlightbackground=BORDER)
        info_frame.pack(fill="x", pady=(0, 10), padx=2)

        lbl_plan_summary = tk.Label(info_frame, text="Syllabus Contract: Reading...", font=("Segoe UI", 9),
                                    fg=TEXT_MAIN, bg="#0f172a", justify="left", anchor="w", padx=12, pady=8)
        lbl_plan_summary.pack(fill="x")

        def update_plan_preview(*args):
            try:
                sc = scope_var.get()
                if sc == "day":
                    d = int(spin_target_day.get())
                    w = ((d - 1) // 7) + 1
                    if w > 52: w = 52
                    plan_file = LESSONS_DIR / f"week-{w:02d}" / f"day-{d:03d}.md"
                    plan_info = curriculum_generator.parse_lesson_plan(plan_file)
                    t_dir = LEARNED_DIR / f"week-{w:02d}" / f"day-{d:03d}"
                    has_readme = (t_dir / "README.md").exists()
                    has_analysis = (t_dir / "analysis.md").exists()
                    has_exp = (t_dir / "experiment.py").exists()
                    status_str = f"Status: {'✅ Suite Present' if has_readme and has_analysis and has_exp else '⚪ Blank Slate / Incomplete'}"
                    lbl_plan_summary.config(
                        text=f"📘 DAY {d:03d} (Week {w:02d}) · {plan_info.get('title', 'Unknown')}\n"
                             f"⚖️ Anchor: {plan_info.get('regulatory_anchor', 'General Civil Aviation')}\n"
                             f"📁 Plan: lessons/week-{w:02d}/day-{d:03d}.md · {status_str}"
                    )
                else:
                    sel_idx = combo_target_week.current() + 1
                    w_start = (sel_idx - 1) * 7 + 1
                    w_end = min(365, sel_idx * 7)
                    missing_count = 0
                    for dd in range(w_start, w_end + 1):
                        td = LEARNED_DIR / f"week-{sel_idx:02d}" / f"day-{dd:03d}"
                        if not (td / "README.md").exists():
                            missing_count += 1
                    lbl_plan_summary.config(
                        text=f"📁 WEEK {sel_idx:02d} (Days {w_start:03d} to {w_end:03d}) · 7 Days Curriculum Batch\n"
                             f"📊 Content Status: {7 - missing_count}/7 Days Generated · {missing_count} Days Blank / Missing\n"
                             f"Mode: {'Generating all 7 days' if not var_only_missing.get() else f'Generating only {missing_count} missing days'}"
                    )
            except Exception as e:
                lbl_plan_summary.config(text=f"Syllabus Preview: {e}")

        spin_target_day.bind("<KeyRelease>", update_plan_preview)
        spin_target_day.bind("<ButtonRelease>", update_plan_preview)
        combo_target_week.bind("<<ComboboxSelected>>", update_plan_preview)
        scope_var.trace_add("write", lambda *a: update_plan_preview())
        var_only_missing.trace_add("write", lambda *a: update_plan_preview())
        update_plan_preview()

        # 4. Real-time Progress Bar & Activity Feed
        progress_box = tk.Frame(body, bg=BG_PANEL)
        progress_box.pack(fill="both", expand=True)

        pbar_hdr = tk.Frame(progress_box, bg=BG_PANEL)
        pbar_hdr.pack(fill="x", pady=(0, 4))

        lbl_gen_status = tk.Label(pbar_hdr, text="Ready to generate. Select options and click 'Start Generation'.",
                                  font=("Segoe UI", 9, "italic"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w")
        lbl_gen_status.pack(side="left")

        lbl_pbar_pct = tk.Label(pbar_hdr, text="0%", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL)
        lbl_pbar_pct.pack(side="right")

        pbar = ttk.Progressbar(progress_box, orient="horizontal", mode="determinate")
        pbar.pack(fill="x", pady=(0, 8))

        log_container = tk.Frame(progress_box, bg="#020617", bd=1, relief="solid")
        log_container.pack(fill="both", expand=True)

        log_scroll = ttk.Scrollbar(log_container)
        log_scroll.pack(side="right", fill="y")

        txt_log = tk.Text(log_container, bg="#020617", fg=TEXT_MAIN, font=("Consolas", 9),
                          bd=0, highlightthickness=0, wrap="word", yscrollcommand=log_scroll.set)
        txt_log.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        log_scroll.config(command=txt_log.yview)

        txt_log.tag_config("ok", foreground=ACCENT_EMERALD, font=("Consolas", 9, "bold"))
        txt_log.tag_config("err", foreground=ACCENT_RED, font=("Consolas", 9, "bold"))
        txt_log.tag_config("info", foreground=ACCENT_CYAN)
        txt_log.tag_config("warn", foreground=ACCENT_AMBER)

        # Bottom Action Bar
        bottom_bar = tk.Frame(dialog, bg="#1e293b", height=50, bd=0, highlightthickness=1, highlightbackground=BORDER)
        bottom_bar.pack(fill="x", side="bottom")

        btn_close = tk.Button(bottom_bar, text="✕ Close", font=("Segoe UI", 9), fg=TEXT_MAIN, bg="#334155",
                              activebackground="#475569", activeforeground="#ffffff", bd=1, relief="solid",
                              padx=14, pady=5, cursor="hand2", command=dialog.destroy)
        btn_close.pack(side="right", padx=(6, 20), pady=10)

        btn_cancel = tk.Button(bottom_bar, text="⏹ Stop / Cancel", font=("Segoe UI", 9), fg=TEXT_MUTED, bg="#1e293b",
                               activebackground="#334155", activeforeground="#ffffff", bd=1, relief="solid",
                               padx=14, pady=5, state="disabled")
        btn_cancel.pack(side="right", padx=6, pady=10)

        btn_start = tk.Button(bottom_bar, text="🚀 Start Generation", font=("Segoe UI", 9, "bold"),
                              fg="#ffffff", bg="#059669", activebackground="#047857", activeforeground="#ffffff",
                              bd=0, padx=18, pady=5, cursor="hand2")
        btn_start.pack(side="right", padx=6, pady=10)

        def log_msg(msg: str, tag: str = "info"):
            try:
                txt_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n", tag)
                txt_log.see("end")
            except Exception:
                pass

        def on_cancel():
            self._gen_cancel_requested = True
            log_msg("Cancellation requested. Stopping after current operation...", "warn")
            btn_cancel.config(state="disabled", text="Stopping...")

        btn_cancel.config(command=on_cancel)

        def start_worker():
            try:
                sc = scope_var.get()
                t_day = int(spin_target_day.get()) if sc == "day" else self.current_day
                t_week = combo_target_week.current() + 1 if sc == "week" else (((t_day - 1) // 7) + 1)
                do_missing = var_only_missing.get()
                do_canvas = var_canvas.get()
                do_notebooklm = var_notebooklm.get()
                do_overwrite = var_overwrite.get()

                btn_start.config(state="disabled")
                btn_cancel.config(state="normal", text="⏹ Stop / Cancel")
                self._gen_cancel_requested = False
                pbar["value"] = 0
                lbl_pbar_pct.config(text="0%")

                threading.Thread(
                    target=self._run_curriculum_generation_worker,
                    args=(sc, t_day, t_week, do_missing, do_canvas, do_notebooklm, do_overwrite,
                          lbl_gen_status, lbl_pbar_pct, pbar, log_msg, btn_start, btn_cancel, dialog),
                    daemon=True
                ).start()
            except Exception as e:
                messagebox.showerror("Invalid Input", f"Please check input parameters: {e}")

        btn_start.config(command=start_worker)

    def _run_curriculum_generation_worker(
        self, scope, target_day, target_week, only_missing, include_canvas,
        generate_notebooklm, overwrite, status_lbl, pct_lbl, pbar, log_msg,
        btn_start, btn_cancel, dialog
    ):
        """Background thread executing curriculum generation for day or week."""
        try:
            client = genai.Client(api_key=self.gemini_key)

            if scope == "day":
                dialog.after(0, lambda: status_lbl.config(text=f"Generating Day {target_day:03d} with Gemini ({self.gemini_model})...", fg=ACCENT_CYAN))
                dialog.after(0, lambda: pbar.config(maximum=100, value=25))
                dialog.after(0, lambda: pct_lbl.config(text="25%"))
                log_msg(f"Initiating synthesis for Day {target_day:03d}...", "info")

                def cb(m):
                    dialog.after(0, lambda msg=m: log_msg(msg, "ok" if "✓" in msg or "✨" in msg else "info"))

                res = curriculum_generator.generate_lesson_suite_for_day(
                    day_num=target_day,
                    root_dir=ROOT_DIR,
                    client=client,
                    model=self.gemini_model,
                    progress_callback=cb,
                    include_canvas=include_canvas,
                    generate_notebooklm=generate_notebooklm,
                    overwrite=overwrite
                )

                dialog.after(0, lambda: pbar.config(value=100))
                dialog.after(0, lambda: pct_lbl.config(text="100%"))
                dialog.after(0, lambda: status_lbl.config(text=f"✨ Day {target_day:03d} successfully generated!", fg=ACCENT_EMERALD))
                log_msg(f"✨ Day {target_day:03d} generation completed!", "ok")

                # Refresh studio
                self.after(0, self._populate_curriculum_tree)
                self.after(0, lambda d=target_day: self.load_day(d))

            else:
                start_day = (target_week - 1) * 7 + 1
                end_day = min(365, target_week * 7)
                total_days = end_day - start_day + 1

                dialog.after(0, lambda: status_lbl.config(text=f"Generating Week {target_week:02d} ({total_days} days)...", fg=ACCENT_CYAN))
                dialog.after(0, lambda: pbar.config(maximum=total_days, value=0))

                def day_cb(curr_idx, tot_days, d_num):
                    pct = int((curr_idx / tot_days) * 100)
                    dialog.after(0, lambda idx=curr_idx, p=pct, d=d_num: (
                        pbar.config(value=idx),
                        pct_lbl.config(text=f"{p}%"),
                        status_lbl.config(text=f"Processing Day {d:03d} ({idx}/{tot_days})...")
                    ))

                def cb(m):
                    dialog.after(0, lambda msg=m: log_msg(msg, "ok" if "✓" in msg or "✨" in msg else "info"))

                res = curriculum_generator.generate_lesson_suite_for_week(
                    week_num=target_week,
                    root_dir=ROOT_DIR,
                    client=client,
                    model=self.gemini_model,
                    progress_callback=cb,
                    day_progress_callback=day_cb,
                    cancel_check=lambda: self._gen_cancel_requested,
                    only_missing=only_missing,
                    include_canvas=include_canvas,
                    generate_notebooklm=generate_notebooklm,
                    overwrite=overwrite
                )

                dialog.after(0, lambda: pbar.config(value=total_days))
                dialog.after(0, lambda: pct_lbl.config(text="100%"))
                dialog.after(0, lambda: status_lbl.config(text=f"✨ Week {target_week:02d} batch complete!", fg=ACCENT_EMERALD))
                log_msg(f"✨ Week {target_week:02d} batch complete. Processed {res.get('processed', 0)}/{total_days} days.", "ok")

                # Refresh studio
                self.after(0, self._populate_curriculum_tree)
                self.after(0, lambda d=start_day: self.load_day(d))

        except Exception as e:
            err_str = str(e)
            dialog.after(0, lambda msg=err_str: (
                status_lbl.config(text=f"❌ Error: {msg[:60]}...", fg=ACCENT_RED),
                log_msg(f"❌ Error: {msg}", "err"),
                messagebox.showerror("Generation Error", f"Failed to generate curriculum suite:\n{msg}", parent=dialog)
            ))
        finally:
            dialog.after(0, lambda: (
                btn_start.config(state="normal"),
                btn_cancel.config(state="disabled", text="⏹ Stop / Cancel")
            ))

    def _on_close(self):
        """Clean shutdown terminating any active child processes."""
        if self.active_process and self.active_process.poll() is None:
            try:
                self.active_process.terminate()
            except Exception:
                pass
        self.destroy()

def main():
    initial_day = 1
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().replace("day-", "").replace("day", "").strip()
        try:
            val = int(arg)
            if 1 <= val <= 365:
                initial_day = val
        except ValueError:
            pass
    app = PracticAIStudio(initial_day=initial_day)
    app.mainloop()

if __name__ == "__main__":
    main()
