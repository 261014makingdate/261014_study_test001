from calculator.ui import main

if __name__ == "__main__":
    import sys
    if "--smoke-test" in sys.argv:
        import tkinter as tk
        from calculator.ui import CalculatorApp
        from calculator.engine import CalculatorEngine
        root = tk.Tk()
        try:
            app = CalculatorApp(root, CalculatorEngine())
            root.update()
            app._mode.set("공학")
            app._switch_mode()
            app._expression.set("sin(30)+2^3")
            app._calculate()
            root.update()
            if app._result.get() != "8.5":
                raise RuntimeError("Scientific calculation smoke test failed")
            app._mode.set("일반")
            app._switch_mode()
            root.update()
        finally:
            root.destroy()
    else:
        main()
