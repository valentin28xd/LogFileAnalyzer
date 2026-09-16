from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .analysis import LogAnalyzer
from .parser import LogParser


class LogAnalyzerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Log File Analyzer")
        self.geometry("860x560")
        self.result = None
        self._build_ui()

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Open log", command=self.open_file).pack(side="left")
        ttk.Label(toolbar, text="Keyword").pack(side="left", padx=(18, 4))
        self.keyword = tk.StringVar()
        ttk.Entry(toolbar, textvariable=self.keyword, width=24).pack(side="left")
        ttk.Button(toolbar, text="Apply filter", command=self.refresh).pack(side="left", padx=8)
        self.summary = tk.StringVar(value="Open a .log file to begin.")
        ttk.Label(self, textvariable=self.summary, padding=(10, 0)).pack(anchor="w")
        self.output = tk.Text(self, wrap="none", state="disabled", padx=10, pady=10)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def open_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Log files", "*.log"), ("All files", "*.*")])
        if path:
            self.result = LogParser().parse_file(Path(path))
            self.refresh()

    def refresh(self) -> None:
        if self.result is None:
            return
        analyzer = LogAnalyzer(self.result.entries)
        selected = analyzer.filter(self.keyword.get())
        selected_analyzer = LogAnalyzer(selected)
        counts = selected_analyzer.counts_by_level()
        self.summary.set(f"Entries: {len(selected)} | INFO: {counts['INFO']} | WARNING: {counts['WARNING']} | ERROR: {counts['ERROR']} | Malformed: {len(self.result.malformed_lines)}")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        for entry in selected:
            self.output.insert("end", f"{entry.timestamp.isoformat()}  {entry.level:<7} {entry.message}\n")
        self.output.configure(state="disabled")


def launch() -> None:
    try:
        LogAnalyzerApp().mainloop()
    except tk.TclError as error:
        messagebox.showerror("GUI unavailable", str(error))
