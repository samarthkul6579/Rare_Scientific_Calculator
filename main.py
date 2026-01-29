import customtkinter as ctk
import numpy as np
import math

# Theme Settings 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main part 
app = ctk.CTk()
app.title(" Rare Scientific Calculator")
app.geometry("950x680")
app.resizable(False, False)

# Global Mode 
angle_mode = "DEG"   # Default Degree Mode

# Main Layout
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)


# HISTORY PANEL                 
history_frame = ctk.CTkFrame(main_frame, width=260)
history_frame.pack(side="left", fill="y", padx=10)

history_label = ctk.CTkLabel(history_frame, text="History", font=("Arial", 22))
history_label.pack(pady=10)

history_box = ctk.CTkTextbox(history_frame, width=240, height=420, font=("Arial", 15))
history_box.pack(pady=10)
history_box.insert("end", "No calculations yet...\n")


# Theme Toggle
def toggle_theme():
    if theme_switch.get() == "on":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

theme_switch = ctk.CTkSwitch(history_frame, text="Light/Dark", command=toggle_theme)
theme_switch.pack(pady=5)


# Degree/Radian Toggle 
def toggle_angle():
    global angle_mode
    if angle_switch.get() == "on":
        angle_mode = "RAD"
    else:
        angle_mode = "DEG"

angle_switch = ctk.CTkSwitch(history_frame, text="Radian Mode", command=toggle_angle)
angle_switch.pack(pady=5)


# CALCULATOR PANEL                 
calc_frame = ctk.CTkFrame(main_frame)
calc_frame.pack(side="right", fill="both", expand=True)

# Display 
display = ctk.CTkEntry(calc_frame, width=600, height=70,
                      font=("Arial", 26), justify="right")
display.pack(pady=20)


#FUNCTIONS                     

def press(value):
    display.insert("end", str(value))


def clear():
    display.delete(0, "end")


# Safe Evaluation
def safe_eval(expr):
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("π", str(math.pi))

    if angle_mode == "DEG":
        def sin(x): return math.sin(math.radians(x))
        def cos(x): return math.cos(math.radians(x))
        def tan(x): return math.tan(math.radians(x))
    else:
        sin, cos, tan = math.sin, math.cos, math.tan

    allowed = {
        "sqrt": math.sqrt,
        "log": math.log,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "__builtins__": None
    }

    return eval(expr, allowed)


def calculate():
    try:
        expression = display.get()
        result = safe_eval(expression)

        display.delete(0, "end")
        display.insert(0, str(result))

        history_box.insert("end", f"{expression} = {result}\n")
        history_box.see("end")

    except:
        display.delete(0, "end")
        display.insert(0, "Error")


# keyboard
def key_input(event):
    key = event.keysym

    if key == "Return":
        calculate()

    elif key == "BackSpace":
        current = display.get()
        display.delete(0, "end")
        display.insert(0, current[:-1])

    elif key == "Escape":
        clear()

    # ---- Scientific Shortcuts ----
    elif key.lower() == "s":
        press("sin(")

    elif key.lower() == "c":
        press("cos(")

    elif key.lower() == "t":
        press("tan(")

    elif key.lower() == "l":
        press("log(")

    elif key.lower() == "q":
        press("sqrt(")

    else:
        char = event.char
        if char in "0123456789+-*/().":
            press(char)
app.bind("<Key>", key_input)



#MATRIX MODE                     
def open_matrix_mode():
    matrix_win = ctk.CTkToplevel(app)
    matrix_win.title("Matrix Mode")
    matrix_win.geometry("520x520")

    label = ctk.CTkLabel(matrix_win, text="Enter Matrices (rows in new line)",
                         font=("Arial", 18))
    label.pack(pady=10)

    # Matrix A
    matA_label = ctk.CTkLabel(matrix_win, text="Matrix A:", font=("Arial", 16))
    matA_label.pack()
    matA_entry = ctk.CTkTextbox(matrix_win, width=420, height=80)
    matA_entry.pack(pady=5)

    # Matrix B
    matB_label = ctk.CTkLabel(matrix_win, text="Matrix B:", font=("Arial", 16))
    matB_label.pack()
    matB_entry = ctk.CTkTextbox(matrix_win, width=420, height=80)
    matB_entry.pack(pady=5)

    # Result Box
    result_box = ctk.CTkTextbox(matrix_win, width=420, height=100)
    result_box.pack(pady=10)

    # Parse Matrix Function
    def parse_matrix(text):
        rows = text.strip().split("\n")
        return np.array([[float(x) for x in row.split(",")] for row in rows])

    # Add Matrices
    def add_matrices():
        try:
            A = parse_matrix(matA_entry.get("1.0", "end"))
            B = parse_matrix(matB_entry.get("1.0", "end"))
            res = A + B
            result_box.delete("1.0", "end")
            result_box.insert("end", str(res))
            history_box.insert("end", f"A + B = {res}\n")
        except:
            result_box.delete("1.0", "end")
            result_box.insert("end", "Matrix Addition Error")

    # Multiply Matrices
    def multiply_matrices():
        try:
            A = parse_matrix(matA_entry.get("1.0", "end"))
            B = parse_matrix(matB_entry.get("1.0", "end"))
            res = np.dot(A, B)
            result_box.delete("1.0", "end")
            result_box.insert("end", str(res))
            history_box.insert("end", f"A × B = {res}\n")
        except:
            result_box.delete("1.0", "end")
            result_box.insert("end", "Matrix Multiplication Error")

    # Buttons
    add_btn = ctk.CTkButton(matrix_win, text="A + B", command=add_matrices)
    add_btn.pack(pady=5)

    mul_btn = ctk.CTkButton(matrix_win, text="A × B", command=multiply_matrices)
    mul_btn.pack(pady=5)



#BUTTONS                        
btn_frame = ctk.CTkFrame(calc_frame)
btn_frame.pack()

buttons = [
    ["MATRIX", "", "", ""],
    ["sin(", "cos(", "tan(", "log("],
    ["sqrt(", "π", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["=",]
]

for row in range(len(buttons)):
    for col in range(len(buttons[row])):

        text = buttons[row][col]
        if text == "":
            continue

        # MATRIX MODE Button
        if text == "MATRIX":
            btn = ctk.CTkButton(btn_frame, text="MATRIX MODE",
                                width=560, height=55,
                                font=("Arial", 18),
                                command=open_matrix_mode)
            btn.grid(row=row, column=0, columnspan=4, pady=10)
            continue

        # Clear Button
        if text == "C":
            btn = ctk.CTkButton(btn_frame, text=text,
                                width=130, height=55,
                                command=clear)

        # Equal Button
        elif text == "=":
            btn = ctk.CTkButton(btn_frame, text=text,
                                width=560, height=60,
                                font=("Arial", 22),
                                command=calculate)
            btn.grid(row=row, column=0, columnspan=4, pady=12)
            continue

        # Normal Buttons
        else:
            btn = ctk.CTkButton(btn_frame, text=text,
                                width=130, height=55,
                                command=lambda val=text: press(val))

        btn.grid(row=row, column=col, padx=6, pady=6)



#RUN APP                         
app.mainloop()