"""
app.py — Tkinter GUI for the To-Do List Application

Liquid Glass theme — light-blue frosted-glass aesthetic with
translucent panels, soft gradients, and airy typography.

This module builds the entire desktop interface:
- Dashboard summary cards
- Task entry form with dropdowns and date picker
- Action buttons (Add, Update, Complete, Delete, Clear)
- Search bar and filter controls
- Task table (ttk.Treeview) with scrollbars
- Event handlers wired to task_manager functions
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime

import task_manager


# ══════════════════════════════════════════════
#  MAIN APPLICATION CLASS
# ══════════════════════════════════════════════

class TodoApp:
    """Main application window for the To-Do List."""

    # ─── Dark teal dashboard palette ───────────────────────────
    BG_PRIMARY    = "#0B1416"
    BG_GLASS      = "#122124"
    BG_GLASS_ALT  = "#193034"
    GLASS_BORDER  = "#25464A"
    GLASS_SHADOW  = "#071012"

    # Header
    HEADER_BG     = "#0D191B"
    HEADER_FG     = "#E8F4F2"
    HEADER_SUB    = "#789596"

    # Dashboard cards
    CARD_1        = "#163236"
    CARD_2        = "#193034"
    CARD_3        = "#1A383A"
    CARD_4        = "#174247"
    CARD_5        = "#3B292C"
    CARD_FG       = "#E5F2EF"
    CARD_FG_LIGHT = "#A7E5E1"

    # Action buttons
    BTN_ADD       = "#08B9C1"
    BTN_UPDATE    = "#167D86"
    BTN_COMPLETE  = "#176B68"
    BTN_DELETE    = "#A84750"
    BTN_CLEAR     = "#29464A"
    BTN_FG        = "#F2FAF8"
    BTN_FG_CLEAR  = "#B5CCCA"

    # Text
    TEXT_DARK     = "#E0EEEB"
    TEXT_MID      = "#A5BFBC"
    TEXT_LIGHT    = "#789391"

    # Table
    TABLE_HEADER  = "#19383B"
    TABLE_EVEN    = "#122124"
    TABLE_ODD     = "#17282B"
    TABLE_SELECT  = "#17565B"
    TABLE_FG      = "#DCEAE7"

    # Fonts
    FONT_FAMILY   = "Segoe UI"

    def __init__(self, root):
        self.root = root
        self.root.title("📋 To-Do List Manager")
        self.root.geometry("1150x750")
        self.root.minsize(1050, 680)
        self.root.configure(bg=self.BG_PRIMARY)

        # Currently selected task ID
        self.selected_task_id = None

        # Apply the liquid-glass ttk styles before building widgets
        self._configure_styles()

        # Build all sections
        self._build_header()
        self._build_dashboard()
        self._build_form_and_table()
        self._build_search_filter_bar()
        self._build_task_table()

        # Initial data load
        self.refresh_dashboard()
        self.load_tasks()

    # ──────────────────────────────────────────
    #  TTK STYLE CONFIGURATION
    # ──────────────────────────────────────────

    def _configure_styles(self):
        """Set up custom ttk styles for the liquid-glass look."""
        style = ttk.Style()
        style.theme_use("clam")  # clam allows the most colour control

        # Treeview
        style.configure(
            "Glass.Treeview",
            background=self.TABLE_EVEN,
            foreground=self.TABLE_FG,
            fieldbackground=self.TABLE_EVEN,
            font=(self.FONT_FAMILY, 10),
            rowheight=28,
            borderwidth=0,
        )
        style.configure(
            "Glass.Treeview.Heading",
            background=self.TABLE_HEADER,
            foreground="#FFFFFF",
            font=(self.FONT_FAMILY, 10, "bold"),
            relief="flat",
            borderwidth=0,
        )
        style.map(
            "Glass.Treeview.Heading",
            background=[("active", "#3D7CC2")],
        )
        style.map(
            "Glass.Treeview",
            background=[("selected", self.TABLE_SELECT)],
            foreground=[("selected", self.TEXT_DARK)],
        )

        # Entry
        style.configure(
            "Glass.TEntry",
            fieldbackground=self.BG_PRIMARY,
            foreground=self.TEXT_DARK,
            bordercolor=self.GLASS_BORDER,
            lightcolor=self.GLASS_BORDER,
            darkcolor=self.GLASS_BORDER,
            borderwidth=1,
            padding=5,
        )
        style.map(
            "Glass.TEntry",
            bordercolor=[("focus", self.HEADER_BG)],
            lightcolor=[("focus", self.HEADER_BG)],
        )

        # Combobox
        style.configure(
            "Glass.TCombobox",
            fieldbackground=self.BG_PRIMARY,
            background=self.BG_GLASS,
            foreground=self.TEXT_DARK,
            bordercolor=self.GLASS_BORDER,
            lightcolor=self.GLASS_BORDER,
            arrowcolor=self.HEADER_BG,
            padding=4,
        )
        style.map(
            "Glass.TCombobox",
            fieldbackground=[("readonly", self.BG_PRIMARY)],
            foreground=[("readonly", self.TEXT_DARK)],
            bordercolor=[("focus", self.HEADER_BG)],
            lightcolor=[("focus", self.HEADER_BG)],
        )

        # Checkbutton
        style.configure(
            "Glass.TCheckbutton",
            background=self.BG_GLASS,
            foreground=self.TEXT_MID,
            font=(self.FONT_FAMILY, 9),
        )
        style.map(
            "Glass.TCheckbutton",
            background=[("active", self.BG_GLASS)],
        )

        # Scrollbar
        style.configure(
            "Glass.Vertical.TScrollbar",
            troughcolor=self.BG_GLASS,
            background=self.GLASS_BORDER,
            bordercolor=self.BG_GLASS,
            arrowcolor=self.TEXT_MID,
            relief="flat",
        )
        style.map(
            "Glass.Vertical.TScrollbar",
            background=[("active", self.GLASS_SHADOW)],
        )
        style.configure(
            "Glass.Horizontal.TScrollbar",
            troughcolor=self.BG_GLASS,
            background=self.GLASS_BORDER,
            bordercolor=self.BG_GLASS,
            arrowcolor=self.TEXT_MID,
            relief="flat",
        )
        style.map(
            "Glass.Horizontal.TScrollbar",
            background=[("active", self.GLASS_SHADOW)],
        )

        # LabelFrame
        style.configure(
            "Glass.TLabelframe",
            background=self.BG_GLASS,
            foreground=self.TEXT_DARK,
            bordercolor=self.GLASS_BORDER,
            relief="groove",
        )
        style.configure(
            "Glass.TLabelframe.Label",
            background=self.BG_GLASS,
            foreground=self.TEXT_DARK,
            font=(self.FONT_FAMILY, 11, "bold"),
        )

    # ──────────────────────────────────────────
    #  HEADER
    # ──────────────────────────────────────────

    def _build_header(self):
        """Semi-transparent-feeling blue header bar."""
        header = tk.Frame(self.root, bg=self.HEADER_BG, height=62)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Left: title
        tk.Label(
            header,
            text="📋  To-Do List Manager",
            font=(self.FONT_FAMILY, 20, "bold"),
            bg=self.HEADER_BG, fg=self.HEADER_FG,
        ).pack(side=tk.LEFT, padx=20)

        # Right: subtitle
        tk.Label(
            header,
            text="Python  •  Tkinter  •  MySQL",
            font=(self.FONT_FAMILY, 10),
            bg=self.HEADER_BG, fg=self.HEADER_SUB,
        ).pack(side=tk.RIGHT, padx=20)

        # Thin glass-edge line under the header
        tk.Frame(self.root, bg=self.GLASS_BORDER, height=2).pack(fill=tk.X)

    # ──────────────────────────────────────────
    #  DASHBOARD CARDS
    # ──────────────────────────────────────────

    def _build_dashboard(self):
        """Five frosted-glass summary cards in a blue gradient."""
        self.dashboard_frame = tk.Frame(self.root, bg=self.BG_PRIMARY)
        self.dashboard_frame.pack(fill=tk.X, padx=18, pady=(12, 6))

        card_defs = [
            ("Total Tasks",  "total",       self.CARD_1, self.CARD_FG_LIGHT),
            ("Pending",      "pending",     self.CARD_2, self.CARD_FG),
            ("In Progress",  "in_progress", self.CARD_3, self.CARD_FG),
            ("Completed",    "completed",   self.CARD_4, self.CARD_FG),
            ("Overdue",      "overdue",     self.CARD_5, self.CARD_FG),
        ]

        self.card_labels = {}

        for label_text, key, bg_colour, fg_colour in card_defs:
            # Outer "glow" frame to fake a soft shadow
            shadow = tk.Frame(self.dashboard_frame, bg=self.GLASS_SHADOW, bd=0)
            shadow.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

            card = tk.Frame(
                shadow, bg=bg_colour, bd=0,
                highlightthickness=1, highlightbackground=self.GLASS_BORDER,
                padx=16, pady=10,
            )
            card.pack(fill=tk.BOTH, padx=1, pady=1)

            tk.Label(
                card, text=label_text,
                font=(self.FONT_FAMILY, 9, "bold"), bg=bg_colour, fg=fg_colour,
            ).pack()

            value_label = tk.Label(
                card, text="0",
                font=(self.FONT_FAMILY, 24, "bold"), bg=bg_colour, fg=fg_colour,
            )
            value_label.pack(pady=(2, 0))
            self.card_labels[key] = value_label

    def refresh_dashboard(self):
        """Fetch stats from the database and update every card."""
        stats = task_manager.get_dashboard_stats()
        for key, label in self.card_labels.items():
            label.config(text=str(stats.get(key, 0)))

    # ──────────────────────────────────────────
    #  FORM + TABLE CONTAINER
    # ──────────────────────────────────────────

    def _build_form_and_table(self):
        """
        Two-column layout:
          Left  → Frosted-glass task form
          Right → Search bar + task table
        """
        self.main_frame = tk.Frame(self.root, bg=self.BG_PRIMARY)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=6)

        # ── Left: Form ──
        form_outer = tk.Frame(
            self.main_frame, bg=self.GLASS_BORDER,
            highlightthickness=0,
        )
        form_outer.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        form_frame = tk.Frame(
            form_outer, bg=self.BG_GLASS,
            padx=18, pady=14,
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Section title
        tk.Label(
            form_frame, text="✦  Task Details",
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.BG_GLASS, fg=self.TEXT_DARK,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Thin separator
        sep = tk.Frame(form_frame, bg=self.GLASS_BORDER, height=1)
        sep.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 12))

        # --- Title ---
        tk.Label(
            form_frame, text="Title *",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 3))

        self.entry_title = ttk.Entry(
            form_frame, width=32, font=(self.FONT_FAMILY, 10),
            style="Glass.TEntry",
        )
        self.entry_title.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))

        # --- Description ---
        tk.Label(
            form_frame, text="Description",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).grid(row=4, column=0, sticky=tk.W, pady=(0, 3))

        self.text_desc = tk.Text(
            form_frame, width=32, height=4,
            font=(self.FONT_FAMILY, 10), wrap=tk.WORD,
            bg=self.BG_PRIMARY, fg=self.TEXT_DARK,
            bd=0, relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.GLASS_BORDER,
            highlightcolor=self.BTN_ADD,
            insertbackground=self.TEXT_DARK,
            padx=6, pady=6,
        )
        self.text_desc.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))

        # --- Priority & Status side by side ---
        tk.Label(
            form_frame, text="Priority",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).grid(row=6, column=0, sticky=tk.W, pady=(0, 3))

        tk.Label(
            form_frame, text="Status",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).grid(row=6, column=1, sticky=tk.W, padx=(12, 0), pady=(0, 3))

        self.combo_priority = ttk.Combobox(
            form_frame, values=["Low", "Medium", "High"],
            state="readonly", width=14, font=(self.FONT_FAMILY, 10),
            style="Glass.TCombobox",
        )
        self.combo_priority.set("Medium")
        self.combo_priority.grid(row=7, column=0, sticky=tk.W, pady=(0, 10))

        self.combo_status = ttk.Combobox(
            form_frame, values=["Pending", "In Progress", "Completed"],
            state="readonly", width=14, font=(self.FONT_FAMILY, 10),
            style="Glass.TCombobox",
        )
        self.combo_status.set("Pending")
        self.combo_status.grid(row=7, column=1, sticky=tk.W, padx=(12, 0), pady=(0, 10))

        # --- Due Date ---
        tk.Label(
            form_frame, text="Due Date",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).grid(row=8, column=0, sticky=tk.W, pady=(0, 3))

        self.date_entry = DateEntry(
            form_frame, width=14, font=(self.FONT_FAMILY, 10),
            date_pattern="yyyy-mm-dd",
            background=self.TABLE_HEADER, foreground=self.HEADER_FG,
            headersbackground=self.TABLE_HEADER,
            headersforeground=self.HEADER_FG,
            bordercolor=self.GLASS_BORDER,
            normalbackground=self.BG_PRIMARY,
            normalforeground=self.TEXT_DARK,
            selectbackground=self.TABLE_SELECT,
            selectforeground=self.TEXT_DARK,
        )
        self.date_entry.grid(row=9, column=0, sticky=tk.W, pady=(0, 10))

        self.no_due_date_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form_frame, text="No due date",
            variable=self.no_due_date_var,
            style="Glass.TCheckbutton",
        ).grid(row=9, column=1, sticky=tk.W, padx=(12, 0), pady=(0, 10))

        # --- Action Buttons ---
        sep2 = tk.Frame(form_frame, bg=self.GLASS_BORDER, height=1)
        sep2.grid(row=10, column=0, columnspan=2, sticky=tk.EW, pady=(4, 12))

        btn_frame = tk.Frame(form_frame, bg=self.BG_GLASS)
        btn_frame.grid(row=11, column=0, columnspan=2, sticky=tk.EW)

        buttons = [
            ("➕  Add",      self.BTN_ADD,      self.BTN_FG,       self.on_add),
            ("✏️  Update",   self.BTN_UPDATE,   self.BTN_FG,       self.on_update),
            ("✅  Complete",  self.BTN_COMPLETE, self.BTN_FG,       self.on_complete),
            ("🗑️  Delete",   self.BTN_DELETE,   self.BTN_FG,       self.on_delete),
            ("🔄  Clear",    self.BTN_CLEAR,    self.BTN_FG_CLEAR, self.clear_form),
        ]
        for text, bg, fg, cmd in buttons:
            self._make_glass_button(btn_frame, text, bg, fg, cmd).pack(
                fill=tk.X, pady=3,
            )

        # ── Right: search + table ──
        self.right_frame = tk.Frame(self.main_frame, bg=self.BG_PRIMARY)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _make_glass_button(self, parent, text, bg, fg, command):
        """Create a liquid-glass styled button with hover effect."""
        btn = tk.Button(
            parent, text=text,
            font=(self.FONT_FAMILY, 10, "bold"),
            bg=bg, fg=fg,
            activebackground=self.GLASS_SHADOW,
            activeforeground="#FFFFFF",
            relief=tk.FLAT, cursor="hand2",
            command=command, padx=12, pady=6,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.GLASS_BORDER,
        )
        # Hover feedback
        darker = self._darken(bg, 0.12)
        btn.bind("<Enter>", lambda e, b=btn, c=darker: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg:     b.config(bg=c))
        return btn

    @staticmethod
    def _darken(hex_color, amount):
        """Darken a hex colour by `amount` (0–1)."""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ──────────────────────────────────────────
    #  SEARCH & FILTER BAR
    # ──────────────────────────────────────────

    def _build_search_filter_bar(self):
        """Frosted search/filter strip above the table."""
        bar_outer = tk.Frame(self.right_frame, bg=self.GLASS_BORDER)
        bar_outer.pack(fill=tk.X, pady=(0, 6))

        bar = tk.Frame(bar_outer, bg=self.BG_GLASS, padx=10, pady=8)
        bar.pack(fill=tk.X, padx=1, pady=1)

        # Search
        tk.Label(
            bar, text="🔍  Search:",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).pack(side=tk.LEFT)

        self.entry_search = ttk.Entry(
            bar, width=20, font=(self.FONT_FAMILY, 10), style="Glass.TEntry",
        )
        self.entry_search.pack(side=tk.LEFT, padx=(6, 10))
        self.entry_search.bind("<Return>", lambda e: self.on_search())

        self._make_glass_button(
            bar, "Search", self.BTN_UPDATE, self.BTN_FG, self.on_search,
        ).pack(side=tk.LEFT, padx=(0, 18))

        # Filter: Status
        tk.Label(
            bar, text="Status:",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).pack(side=tk.LEFT)

        self.filter_status = ttk.Combobox(
            bar, values=["All", "Pending", "In Progress", "Completed"],
            state="readonly", width=12, font=(self.FONT_FAMILY, 10),
            style="Glass.TCombobox",
        )
        self.filter_status.set("All")
        self.filter_status.pack(side=tk.LEFT, padx=(6, 14))
        self.filter_status.bind("<<ComboboxSelected>>", lambda e: self.on_filter())

        # Filter: Priority
        tk.Label(
            bar, text="Priority:",
            font=(self.FONT_FAMILY, 10), bg=self.BG_GLASS, fg=self.TEXT_MID,
        ).pack(side=tk.LEFT)

        self.filter_priority = ttk.Combobox(
            bar, values=["All", "Low", "Medium", "High"],
            state="readonly", width=10, font=(self.FONT_FAMILY, 10),
            style="Glass.TCombobox",
        )
        self.filter_priority.set("All")
        self.filter_priority.pack(side=tk.LEFT, padx=(6, 14))
        self.filter_priority.bind("<<ComboboxSelected>>", lambda e: self.on_filter())

        # Show All
        self._make_glass_button(
            bar, "Show All", self.BTN_CLEAR, self.BTN_FG_CLEAR, self.on_show_all,
        ).pack(side=tk.LEFT)

    # ──────────────────────────────────────────
    #  TASK TABLE (Treeview)
    # ──────────────────────────────────────────

    def _build_task_table(self):
        """Frosted-glass table panel with scrollable Treeview."""
        table_outer = tk.Frame(self.right_frame, bg=self.GLASS_BORDER)
        table_outer.pack(fill=tk.BOTH, expand=True)

        table_frame = tk.Frame(table_outer, bg=self.BG_GLASS)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        columns = ("id", "title", "priority", "status", "due_date", "created_at")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            selectmode="browse", height=18,
            style="Glass.Treeview",
        )

        col_config = {
            "id":         ("ID",           55,  tk.CENTER),
            "title":      ("Title",        220, tk.W),
            "priority":   ("Priority",     90,  tk.CENTER),
            "status":     ("Status",       110, tk.CENTER),
            "due_date":   ("Due Date",     100, tk.CENTER),
            "created_at": ("Created Date", 145, tk.CENTER),
        }
        for col, (heading, width, anchor) in col_config.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=anchor, minwidth=45)

        # Scrollbars
        vsb = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview,
            style="Glass.Vertical.TScrollbar",
        )
        hsb = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview,
            style="Glass.Horizontal.TScrollbar",
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Alternating row colours — light-blue tints
        self.tree.tag_configure("evenrow", background=self.TABLE_EVEN)
        self.tree.tag_configure("oddrow",  background=self.TABLE_ODD)

        # Click → populate form
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # ──────────────────────────────────────────
    #  DATA LOADING
    # ──────────────────────────────────────────

    def load_tasks(self, tasks=None):
        """
        Clear the table and load tasks into it.
        If `tasks` is None, fetch all from the database.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        if tasks is None:
            ok, result = task_manager.get_all_tasks()
            if not ok:
                messagebox.showerror("Error", result)
                return
            tasks = result

        for idx, task in enumerate(tasks):
            due = task["due_date"]
            due_str = due.strftime("%Y-%m-%d") if due else ""
            created = task["created_at"]
            created_str = (
                created.strftime("%Y-%m-%d %H:%M")
                if isinstance(created, datetime)
                else str(created)
            )

            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, iid=task["id"], values=(
                task["id"],
                task["title"],
                task["priority"],
                task["status"],
                due_str,
                created_str,
            ), tags=(tag,))

    # ──────────────────────────────────────────
    #  FORM HELPERS
    # ──────────────────────────────────────────

    def clear_form(self):
        """Reset all form fields and deselect the table row."""
        self.selected_task_id = None
        self.entry_title.delete(0, tk.END)
        self.text_desc.delete("1.0", tk.END)
        self.combo_priority.set("Medium")
        self.combo_status.set("Pending")
        self.date_entry.set_date(date.today())
        self.no_due_date_var.set(False)
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _get_form_data(self):
        """Read current values from the form and return a dict."""
        due_str = "" if self.no_due_date_var.get() else self.date_entry.get()
        return {
            "title":        self.entry_title.get(),
            "description":  self.text_desc.get("1.0", tk.END).strip(),
            "priority":     self.combo_priority.get(),
            "status":       self.combo_status.get(),
            "due_date_str": due_str,
        }

    def _after_action(self):
        """Common refresh after any CRUD operation."""
        self.refresh_dashboard()
        self.load_tasks()
        self.clear_form()

    # ──────────────────────────────────────────
    #  EVENT HANDLERS
    # ──────────────────────────────────────────

    def on_tree_select(self, event):
        """When a row is clicked, populate the form with that task's data."""
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        ok, task = task_manager.get_task_by_id(task_id)
        if not ok:
            messagebox.showerror("Error", task)
            return

        self.selected_task_id = task_id

        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, task["title"])

        self.text_desc.delete("1.0", tk.END)
        if task["description"]:
            self.text_desc.insert("1.0", task["description"])

        self.combo_priority.set(task["priority"])
        self.combo_status.set(task["status"])

        if task["due_date"]:
            self.date_entry.set_date(task["due_date"])
            self.no_due_date_var.set(False)
        else:
            self.date_entry.set_date(date.today())
            self.no_due_date_var.set(True)

    def on_add(self):
        """Add a new task to the database."""
        data = self._get_form_data()
        ok, msg = task_manager.add_task(
            data["title"], data["description"],
            data["priority"], data["due_date_str"],
        )
        if ok:
            messagebox.showinfo("Success", msg)
            self._after_action()
        else:
            messagebox.showwarning("Validation Error", msg)

    def on_update(self):
        """Update the currently selected task."""
        if self.selected_task_id is None:
            messagebox.showwarning("No Selection",
                                   "Please select a task from the table to update.")
            return
        data = self._get_form_data()
        ok, msg = task_manager.update_task(
            self.selected_task_id,
            data["title"], data["description"],
            data["priority"], data["status"], data["due_date_str"],
        )
        if ok:
            messagebox.showinfo("Success", msg)
            self._after_action()
        else:
            messagebox.showwarning("Update Error", msg)

    def on_complete(self):
        """Mark the selected task as Completed."""
        if self.selected_task_id is None:
            messagebox.showwarning("No Selection",
                                   "Please select a task to mark as completed.")
            return
        ok, task = task_manager.get_task_by_id(self.selected_task_id)
        if not ok:
            messagebox.showerror("Error", task)
            return

        due_str = task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else ""
        ok, msg = task_manager.update_task(
            self.selected_task_id,
            task["title"], task["description"] or "",
            task["priority"], "Completed", due_str,
        )
        if ok:
            messagebox.showinfo("Success", f"Task '{task['title']}' marked as Completed!")
            self._after_action()
        else:
            messagebox.showwarning("Error", msg)

    def on_delete(self):
        """Delete the selected task after confirmation."""
        if self.selected_task_id is None:
            messagebox.showwarning("No Selection",
                                   "Please select a task to delete.")
            return
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this task?\nThis action cannot be undone.",
        )
        if not confirm:
            return
        ok, msg = task_manager.delete_task(self.selected_task_id)
        if ok:
            messagebox.showinfo("Deleted", msg)
            self._after_action()
        else:
            messagebox.showerror("Error", msg)

    # ── Search & Filter ──

    def on_search(self):
        """Search tasks by title keyword."""
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Search", "Please enter a search keyword.")
            return
        ok, result = task_manager.search_tasks(keyword)
        if ok:
            self.load_tasks(result)
            self.refresh_dashboard()
        else:
            messagebox.showerror("Search Error", result)

    def on_filter(self):
        """Filter tasks by the selected status and/or priority."""
        status = self.filter_status.get()
        priority = self.filter_priority.get()
        ok, result = task_manager.filter_tasks(
            status if status != "All" else None,
            priority if priority != "All" else None,
        )
        if ok:
            self.load_tasks(result)
        else:
            messagebox.showerror("Filter Error", result)

    def on_show_all(self):
        """Reset filters and show every task."""
        self.entry_search.delete(0, tk.END)
        self.filter_status.set("All")
        self.filter_priority.set("All")
        self.load_tasks()
        self.refresh_dashboard()


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
