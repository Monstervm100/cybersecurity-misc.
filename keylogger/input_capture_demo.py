import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime


BG        = "#0a0a0a"
BG2       = "#0d0d0d"
PANEL     = "#0d1f2d"
BORDER    = "#1a3a50"
BLUE_DIM  = "#2a5a70"
BLUE_MID  = "#4a9ab5"
BLUE_MAIN = "#7ecfed"
BLUE_LITE = "#a8d8ea"
FG_DIM    = "#2a5a70"
FG_MID    = "#4a9ab5"
FG        = "#c0c0c0"


class InputCaptureDemo:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Input Capture Demo — LEFT PANEL (type here)")
        self.root.geometry("480x500+100+100")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._build_input_panel()
        self._open_output_panel()
        self._attach_traces()

    def _build_input_panel(self):
        bold  = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        mono  = tkfont.Font(family="Consolas", size=11)
        large = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        tk.Label(
            self.root,
            text="DEMO",
            bg=PANEL, fg=BLUE_MAIN, font=bold, pady=6, anchor="center",
        ).pack(fill="x")

        tk.Label(self.root, text="Input Capture Demo — Left Panel",
                 bg=BG, fg=BLUE_MAIN, font=large, pady=10).pack()

        tk.Label(
            self.root,
            text="Type in the fields below.\nEvery character is mirrored live on the right-panel window.",
            bg=BG, fg=BLUE_MID, font=tkfont.Font(family="Segoe UI", size=9),
            justify="center",
        ).pack(pady=(0, 14))

        tk.Label(self.root, text="Username", bg=BG, fg=BLUE_MID,
                 font=bold, anchor="w").pack(fill="x", padx=60)

        self.user_entry = tk.Entry(
            self.root, textvariable=self.username_var,
            bg=PANEL, fg=BLUE_LITE, insertbackground=BLUE_MAIN,
            font=mono, relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=BLUE_MAIN,
        )
        self.user_entry.pack(fill="x", padx=60, ipady=6, pady=(2, 14))

        tk.Label(self.root, text="Password  (shown in plain text on right panel)",
                 bg=BG, fg=BLUE_MID, font=bold, anchor="w").pack(fill="x", padx=60)

        self.pass_entry = tk.Entry(
            self.root, textvariable=self.password_var, show="●",
            bg=PANEL, fg=BLUE_LITE, insertbackground=BLUE_MAIN,
            font=mono, relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=BLUE_MAIN,
        )
        self.pass_entry.pack(fill="x", padx=60, ipady=6, pady=(2, 20))

        tk.Button(
            self.root, text="Submit (demo — does nothing)",
            bg=PANEL, fg=BLUE_MID,
            activebackground=BORDER, activeforeground=BLUE_MAIN,
            relief="flat", padx=14, pady=6,
            font=bold, cursor="hand2",
            command=self._on_submit,
        ).pack(pady=(0, 20))

        btn = tk.Frame(self.root, bg=BG)
        btn.pack()

        tk.Button(btn, text="Clear All", command=self._clear_all,
                  bg=BG2, fg=BLUE_MID,
                  activebackground=PANEL, activeforeground=BLUE_MAIN,
                  relief="flat", padx=12, pady=4, font=bold, cursor="hand2",
                  ).pack(side="left", padx=6)

        tk.Button(btn, text="Quit", command=self.root.destroy,
                  bg=BG2, fg=FG_MID,
                  activebackground=PANEL, activeforeground=BLUE_MAIN,
                  relief="flat", padx=12, pady=4, font=bold, cursor="hand2",
                  ).pack(side="left", padx=6)

        tk.Label(
            self.root,
            text="How it works: StringVar.trace_add('write', callback) fires whenever\n"
                 "the Entry changes. No keylogger hooks — just variable observers.",
            bg=BG, fg=FG_DIM,
            font=tkfont.Font(family="Segoe UI", size=8),
            justify="center",
        ).pack(pady=(20, 8))

    def _open_output_panel(self):
        self.out_win = tk.Toplevel(self.root)
        self.out_win.title("Captured Input — RIGHT PANEL (read-only)")
        self.out_win.geometry("520x500+620+100")
        self.out_win.configure(bg=BG)
        self.out_win.resizable(True, True)
        self.out_win.protocol("WM_DELETE_WINDOW", lambda: None)

        bold  = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        mono  = tkfont.Font(family="Consolas", size=11)
        large = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        tk.Label(
            self.out_win,
            text="DEMO",
            bg=PANEL, fg=BLUE_MAIN, font=bold, pady=6, anchor="center",
        ).pack(fill="x")

        tk.Label(self.out_win, text="Captured Input — Right Panel",
                 bg=BG, fg=BLUE_MAIN, font=large, pady=10).pack()

        tk.Label(self.out_win, text="Username (live):", bg=BG, fg=BLUE_MID,
                 font=bold, anchor="w").pack(fill="x", padx=20, pady=(6, 0))

        self.live_user_var = tk.StringVar(value="")
        tk.Label(self.out_win, textvariable=self.live_user_var,
                 bg=PANEL, fg=BLUE_LITE, font=mono,
                 anchor="w", pady=6, padx=10,
                 ).pack(fill="x", padx=20, pady=(2, 14))

        tk.Label(self.out_win, text="Password (plain text):", bg=BG, fg=BLUE_MID,
                 font=bold, anchor="w").pack(fill="x", padx=20)

        self.live_pass_var = tk.StringVar(value="")
        tk.Label(self.out_win, textvariable=self.live_pass_var,
                 bg=PANEL, fg=BLUE_LITE, font=mono,
                 anchor="w", pady=6, padx=10,
                 ).pack(fill="x", padx=20, pady=(2, 14))

        tk.Label(self.out_win, text="Change Event Log:", bg=BG, fg=BLUE_MID,
                 font=bold, anchor="w").pack(fill="x", padx=20)

        log_frame = tk.Frame(self.out_win, bg=BG)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(4, 20))

        sb = tk.Scrollbar(log_frame)
        sb.pack(side="right", fill="y")

        self.out_log = tk.Text(
            log_frame, bg="#050505", fg=FG,
            font=mono, state="disabled", relief="flat", bd=0,
            wrap="word", yscrollcommand=sb.set,
        )
        self.out_log.pack(side="left", fill="both", expand=True)
        sb.config(command=self.out_log.yview)

        self.out_log.tag_config("ts",    foreground=FG_DIM)
        self.out_log.tag_config("field", foreground=BLUE_MID)
        self.out_log.tag_config("value", foreground=BLUE_MAIN)
        self.out_log.tag_config("len",   foreground=BLUE_DIM)

    def _attach_traces(self):
        self.username_var.trace_add("write", self._on_user_change)
        self.password_var.trace_add("write", self._on_pass_change)

    def _on_user_change(self, *_):
        val = self.username_var.get()
        self.live_user_var.set(val)
        self._log_change("username", val, mask=False)

    def _on_pass_change(self, *_):
        val = self.password_var.get()
        self.live_pass_var.set(val)
        self._log_change("password", val, mask=False)

    def _log_change(self, field: str, value: str, mask: bool):
        ts      = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        display = ("●" * len(value)) if mask else value

        self.out_log.config(state="normal")
        self.out_log.insert("end", f"[{ts}]  ", "ts")
        self.out_log.insert("end", f"{field:<10}", "field")
        self.out_log.insert("end", "  →  ", "ts")
        self.out_log.insert("end", f"{display:<30}", "value")
        self.out_log.insert("end", f"  len={len(value)}\n", "len")
        self.out_log.config(state="disabled")
        self.out_log.see("end")

    def _on_submit(self):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.out_log.config(state="normal")
        self.out_log.insert("end", f"[{ts}]  ", "ts")
        self.out_log.insert("end", "SUBMIT pressed — demo only, nothing sent.\n", "field")
        self.out_log.config(state="disabled")
        self.out_log.see("end")

    def _clear_all(self):
        self.username_var.set("")
        self.password_var.set("")
        self.out_log.config(state="normal")
        self.out_log.delete("1.0", "end")
        self.out_log.config(state="disabled")


def main():
    root = tk.Tk()
    InputCaptureDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
