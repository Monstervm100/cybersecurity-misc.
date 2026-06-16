import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime


class KeyloggerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Event Demo — Educational")
        self.root.geometry("700x600")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)

        self.press_count = 0

        self._build_ui()
        self._bind_events()

    def _build_ui(self):
        mono = tkfont.Font(family="Consolas", size=11)
        bold = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        tk.Label(
            self.root,
            text="DEMO",
            bg="#0d1f2d",
            fg="#7ecfed",
            font=bold,
            pady=6,
            anchor="center",
        ).pack(fill="x", side="top")

        tk.Label(
            self.root,
            text="Keyboard Event Listener Demo",
            bg="#0a0a0a",
            fg="#7ecfed",
            font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
            pady=8,
        ).pack()

        stats_frame = tk.Frame(self.root, bg="#111111", pady=6)
        stats_frame.pack(fill="x", padx=10)

        tk.Label(stats_frame, text="Total key presses:", bg="#111111", fg="#4a9ab5",
                 font=bold).pack(side="left", padx=(10, 4))

        self.counter_var = tk.StringVar(value="0")
        tk.Label(stats_frame, textvariable=self.counter_var, bg="#111111",
                 fg="#7ecfed", font=tkfont.Font(family="Consolas", size=12, weight="bold"),
                 width=6).pack(side="left")

        tk.Label(stats_frame, text="Last key:", bg="#111111", fg="#4a9ab5",
                 font=bold).pack(side="left", padx=(20, 4))
        self.last_key_var = tk.StringVar(value="—")
        tk.Label(stats_frame, textvariable=self.last_key_var, bg="#111111",
                 fg="#a8d8ea", font=tkfont.Font(family="Consolas", size=12, weight="bold"),
                 width=18).pack(side="left")

        self.focus_var = tk.StringVar(value="● FOCUSED")
        self.focus_label = tk.Label(
            stats_frame, textvariable=self.focus_var,
            bg="#111111", fg="#7ecfed",
            font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
        )
        self.focus_label.pack(side="right", padx=10)

        tk.Label(self.root, text="Event Log", bg="#0a0a0a", fg="#7ecfed",
                 font=bold, anchor="w").pack(fill="x", padx=12, pady=(10, 2))

        log_frame = tk.Frame(self.root, bg="#0a0a0a")
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_text = tk.Text(
            log_frame,
            bg="#050505",
            fg="#c0c0c0",
            font=mono,
            wrap="word",
            state="disabled",
            relief="flat",
            bd=0,
            yscrollcommand=scrollbar.set,
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)

        self.log_text.tag_config("timestamp", foreground="#2a5a70")
        self.log_text.tag_config("key_normal", foreground="#7ecfed")
        self.log_text.tag_config("key_special", foreground="#a8d8ea")
        self.log_text.tag_config("key_modifier", foreground="#4a9ab5")
        self.log_text.tag_config("event_type", foreground="#3d8fa6")

        btn_frame = tk.Frame(self.root, bg="#0a0a0a")
        btn_frame.pack(pady=(0, 10))

        tk.Button(
            btn_frame, text="Clear Log", command=self._clear_log,
            bg="#0d1f2d", fg="#7ecfed",
            activebackground="#1a3a50", activeforeground="#a8d8ea",
            relief="flat", padx=14, pady=4, font=bold, cursor="hand2",
        ).pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="Quit", command=self.root.destroy,
            bg="#0a0a0a", fg="#4a9ab5",
            activebackground="#111111", activeforeground="#7ecfed",
            relief="flat", padx=14, pady=4, font=bold, cursor="hand2",
        ).pack(side="left", padx=6)

        tk.Label(
            self.root,
            text="How it works: tkinter binds <KeyPress>/<KeyRelease> to this window object.\n"
                 "Events fire only while this window has OS focus — no system-wide hooks used.",
            bg="#0a0a0a", fg="#2a5a70",
            font=tkfont.Font(family="Segoe UI", size=8),
            justify="center",
        ).pack(pady=(0, 8))

    def _bind_events(self):
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.bind("<FocusIn>", self._on_focus_in)
        self.root.bind("<FocusOut>", self._on_focus_out)

    def _on_key_press(self, event):
        self.press_count += 1
        self.counter_var.set(str(self.press_count))
        display, tag = self._describe_key(event)
        self.last_key_var.set(display)
        self._append_log(event, display, tag, "PRESS")

    def _on_key_release(self, event):
        display, tag = self._describe_key(event)
        self._append_log(event, display, tag, "RELEASE")

    def _on_focus_in(self, event):
        self.focus_var.set("● FOCUSED")
        self.focus_label.config(fg="#7ecfed")

    def _on_focus_out(self, event):
        self.focus_var.set("○ UNFOCUSED  (not capturing)")
        self.focus_label.config(fg="#2a5a70")

    @staticmethod
    def _describe_key(event):
        modifiers = []
        state = event.state
        if state & 0x0001:
            modifiers.append("Shift")
        if state & 0x0004:
            modifiers.append("Ctrl")
        if state & 0x0008:
            modifiers.append("Alt")

        keysym = event.keysym

        SPECIAL_KEYS = {
            "Return": "Enter", "BackSpace": "Backspace", "Delete": "Delete",
            "Tab": "Tab", "Escape": "Escape", "space": "Space",
            "Up": "↑", "Down": "↓", "Left": "←", "Right": "→",
            "Home": "Home", "End": "End", "Prior": "PageUp", "Next": "PageDown",
            "Insert": "Insert", "caps_lock": "CapsLock",
        }
        MODIFIER_KEYS = {
            "Shift_L", "Shift_R", "Control_L", "Control_R",
            "Alt_L", "Alt_R", "Super_L", "Super_R", "Meta_L", "Meta_R",
        }

        if keysym in MODIFIER_KEYS:
            label = keysym.replace("_L", " (Left)").replace("_R", " (Right)")
            return f"[{label}]", "key_modifier"

        if keysym in SPECIAL_KEYS:
            base = SPECIAL_KEYS[keysym]
            parts = modifiers + [base]
            return "+".join(parts), "key_special"

        char = event.char if event.char and event.char.isprintable() else keysym
        if modifiers:
            return "+".join(modifiers) + f"+{char.upper()}", "key_special"
        return char, "key_normal"

    def _append_log(self, event, display, tag, action):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"[{ts}]  ", "timestamp")
        self.log_text.insert("end", f"{action:<8}", "event_type")
        self.log_text.insert("end", "  key=", "timestamp")
        self.log_text.insert("end", f"{display:<20}", tag)
        self.log_text.insert("end",
            f"  keysym={event.keysym:<18}  keycode={event.keycode}\n", "timestamp")
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.press_count = 0
        self.counter_var.set("0")
        self.last_key_var.set("—")


def main():
    root = tk.Tk()
    KeyloggerDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
