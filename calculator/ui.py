"""Tk presentation layer; only the engine owns arithmetic behavior."""
import tkinter as tk
from tkinter import ttk

from .engine import CalculationError, CalculatorEngine


class CalculatorApp:
    def __init__(self, root, engine):
        self._root = root
        self._engine = engine
        self._expression = tk.StringVar()
        self._result = tk.StringVar(value="0")
        self._mode = tk.StringVar(value="일반")
        self._angle = tk.StringVar(value="DEG")
        self._records = []
        root.title("공학용 계산기")
        root.geometry("520x720")
        root.minsize(440, 620)
        root.configure(bg="#f1f5f9")
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=8)
        outer = ttk.Frame(root, padding=20)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="CALCULATOR", font=("Arial", 20, "bold")).pack(anchor="w")
        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=12)
        for mode in ("일반", "공학"):
            ttk.Radiobutton(controls, text=mode, variable=self._mode, value=mode,
                            command=self._switch_mode).pack(side="left", padx=5)
        self._angle_box = ttk.Combobox(controls, textvariable=self._angle,
                                      values=("DEG", "RAD"), state="readonly", width=6)
        self._entry = ttk.Entry(outer, textvariable=self._expression, font=("Arial", 20))
        self._entry.pack(fill="x", pady=8)
        ttk.Label(outer, textvariable=self._result, font=("Arial", 24, "bold"),
                  anchor="e", wraplength=440).pack(fill="x", pady=8)
        self._science = ttk.Frame(outer)
        scientific = [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("π", "pi"),
                      ("asin", "asin("), ("acos", "acos("), ("atan", "atan("), ("e", "e"),
                      ("√", "sqrt("), ("log", "log("), ("ln", "ln("), ("xʸ", "^"),
                      ("n!", "fact("), ("exp", "exp("), ("abs", "abs("), ("mod", "%")]
        self._buttons(self._science, scientific)
        keypad = ttk.Frame(outer)
        self._keypad = keypad
        keypad.pack(fill="x", pady=8)
        keys = [("AC", self._clear), ("⌫", self._backspace), ("(", "("), (")", ")"),
                ("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"),
                ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"),
                ("1", "1"), ("2", "2"), ("3", "3"), ("−", "-"),
                ("0", "0"), (".", "."), ("%", "/100"), ("+", "+"),
                ("Ans", "ans"), ("±", self._negate), ("기록 삭제", self._clear_history), ("=", self._calculate)]
        self._buttons(keypad, keys)
        ttk.Label(outer, text="계산 기록 · 더블클릭으로 수식 재사용").pack(anchor="w", pady=(8, 4))
        self._history = tk.Listbox(outer, height=5, font=("Arial", 11), borderwidth=0)
        self._history.pack(fill="both", expand=True)
        self._history.bind("<Double-Button-1>", self._reuse)
        root.bind("<Return>", lambda _: self._calculate())
        root.bind("<KP_Enter>", lambda _: self._calculate())
        root.bind("<Escape>", lambda _: self._clear())
        self._entry.focus_set()

    def _buttons(self, frame, keys):
        for col in range(4):
            frame.columnconfigure(col, weight=1)
        for i, (label, action) in enumerate(keys):
            command = action if callable(action) else lambda text=action: self._insert(text)
            ttk.Button(frame, text=label, command=command).grid(
                row=i // 4, column=i % 4, sticky="nsew", padx=2, pady=2)

    def _switch_mode(self):
        if self._mode.get() == "공학":
            self._science.pack(fill="x", before=self._keypad)
            self._angle_box.pack(side="right")
            self._root.geometry("520x920")
        else:
            self._science.pack_forget()
            self._angle_box.pack_forget()
            self._root.geometry("520x720")

    def _insert(self, text):
        if self._entry.selection_present():
            self._entry.delete("sel.first", "sel.last")
        self._entry.insert(tk.INSERT, text)
        self._entry.focus_set()

    def _clear(self):
        self._expression.set("")
        self._result.set("0")
        self._entry.focus_set()

    def _backspace(self):
        if self._entry.selection_present():
            self._entry.delete("sel.first", "sel.last")
        else:
            pos = self._entry.index(tk.INSERT)
            if pos:
                self._entry.delete(pos - 1, pos)
        self._entry.focus_set()

    def _negate(self):
        self._expression.set(f"-({self._expression.get() or '0'})")
        self._entry.icursor(tk.END)

    def _calculate(self):
        expression = self._expression.get()
        try:
            result = self._engine.calculate(expression, degrees=self._angle.get() == "DEG")
        except CalculationError as error:
            self._result.set(str(error))
            return
        formatted = format(result, ".12g")
        self._result.set(formatted)
        self._records.insert(0, expression)
        self._history.insert(0, f"{expression} = {formatted}  [{self._angle.get()}]")
        if len(self._records) > 100:
            self._records.pop()
            self._history.delete(100)

    def _clear_history(self):
        self._records.clear()
        self._history.delete(0, tk.END)

    def _reuse(self, _event):
        selected = self._history.curselection()
        if selected:
            self._expression.set(self._records[selected[0]])
            self._entry.icursor(tk.END)
            self._entry.focus_set()


def main():
    root = tk.Tk()
    CalculatorApp(root, CalculatorEngine())
    root.mainloop()
