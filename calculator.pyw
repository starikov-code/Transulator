import tkinter as tk
from tkinter import messagebox

# ——— Color Themes ———
LIGHT_THEME = {
    "bg": "#f0f0f0",
    "fg": "black",
    "entry_bg": "white",
    "entry_fg": "black",
    "button_bg": "#e0e0e0",
    "label_fg": "black",
    "footer_bg": "lightgray",
    "footer_fg": "dimgray",
    "result_fg": "blue",
    "error_fg": "red"
}

DARK_THEME = {
    "bg": "#2b2b2b",
    "fg": "white",
    "entry_bg": "#3c3c3c",
    "entry_fg": "white",
    "button_bg": "#444444",
    "label_fg": "white",
    "footer_bg": "#333333",
    "footer_fg": "lightgray",
    "result_fg": "cyan",
    "error_fg": "orange"
}

# Save original messagebox functions BEFORE overriding them
_original_showinfo = messagebox.showinfo
_original_showwarning = messagebox.showwarning
_original_showerror = messagebox.showerror
_original_askquestion = messagebox.askquestion


# Centered messagebox function
def centered_messagebox(title, message, parent=None, icon='info'):
    """
    Show a messagebox centered over the parent window
    """
    if parent is None:
        parent = root

    # Create a temporary toplevel window
    temp = tk.Toplevel(parent)
    temp.withdraw()  # Hide it
    temp.transient(parent)  # Set as transient to parent

    # Get parent window position and size
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # Update to get accurate dimensions
    parent.update_idletasks()

    # Calculate center position
    x = parent_x + (parent_width // 2)
    y = parent_y + (parent_height // 2)

    # Set temporary window position (this affects messagebox positioning)
    temp.geometry(f"+{x}+{y}")
    temp.update_idletasks()

    # Show the messagebox using ORIGINAL functions to avoid recursion
    if icon == 'info':
        result = _original_showinfo(title, message, parent=temp)
    elif icon == 'warning':
        result = _original_showwarning(title, message, parent=temp)
    elif icon == 'error':
        result = _original_showerror(title, message, parent=temp)
    elif icon == 'question':
        result = _original_askquestion(title, message, parent=temp)

    # Clean up
    temp.destroy()

    return result


# Override with centered versions - MUST use original functions internally
def showinfo(title, message, **kwargs):
    parent = kwargs.get('parent', root)
    return centered_messagebox(title, message, parent, 'info')


def showwarning(title, message, **kwargs):
    parent = kwargs.get('parent', root)
    return centered_messagebox(title, message, parent, 'warning')


def showerror(title, message, **kwargs):
    parent = kwargs.get('parent', root)
    return centered_messagebox(title, message, parent, 'error')


def askquestion(title, message, **kwargs):
    parent = kwargs.get('parent', root)
    return centered_messagebox(title, message, parent, 'question')


# Monkey patch - do this AFTER defining the override functions
messagebox.showinfo = showinfo
messagebox.showwarning = showwarning
messagebox.showerror = showerror
messagebox.askquestion = askquestion

current_theme = LIGHT_THEME
suppress_mode_updates = False  # Global flag to suppress mode updates during reset


def apply_theme():
    """Apply current theme to all widgets"""
    root.config(bg=current_theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            if widget.cget("text").startswith("Cost:") or "Error" in widget.cget("text"):
                widget.config(fg=current_theme["result_fg"], bg=current_theme["bg"])
            elif widget.cget("text").startswith("Pages:"):
                widget.config(fg=current_theme["result_fg"], bg=current_theme["bg"])
            elif "Created by" in widget.cget("text"):
                widget.config(fg=current_theme["footer_fg"], bg=current_theme["footer_bg"])
            else:
                widget.config(fg=current_theme["label_fg"], bg=current_theme["bg"])
        elif isinstance(widget, tk.Entry):
            widget.config(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"],
                          insertbackground=current_theme["fg"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=current_theme["button_bg"], fg=current_theme["fg"])
        elif isinstance(widget, tk.Frame):
            widget.config(bg=current_theme["bg"])

    # Theme divisor frame
    for child in divisor_frame.winfo_children():
        if isinstance(child, tk.Label):
            child.config(fg=current_theme["label_fg"], bg=current_theme["bg"])
        elif isinstance(child, tk.Entry):
            child.config(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"])
    footer_label.config(bg=current_theme["footer_bg"], fg=current_theme["footer_fg"])


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return

        # Position tooltip slightly below and centered on the widget
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5  # 5px below

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text,
                         background="lightyellow", relief="solid", borderwidth=1,
                         font=("Verdana", 9))
        label.pack(padx=5, pady=5)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

import subprocess
import platform

def open_calculator():
        """Open the system's native calculator"""
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen("calc.exe")
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Calculator"])
            elif system == "Linux":
                subprocess.Popen(["gnome-calculator"])
            else:
                messagebox.showerror("Error", f"Calculator not supported on {system}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open calculator: {str(e)}")

def parse_number(value: str) -> float:
    """Convert string to float, accepting both '.' and ',' as decimal separators"""
    if not value:
        raise ValueError("Empty input")
    cleaned = value.strip().replace(' ', '').replace(',', '.')
    return float(cleaned)


def update_price_fields(*args):
    """Block mode switch if input fields are not empty, unless suppressed"""
    global suppress_mode_updates

    # If we're in a silent reset, skip protection
    if suppress_mode_updates:
        return

    inputs_filled = any(
        entry.get().strip()
        for entry in (entry_value, entry_rate, entry_price_per_word)
    )

    if inputs_filled:
        messagebox.showinfo(
            "Switching Not Allowed",
            "Please click 'Clear' or press 'Esc' to clear input fields\nbefore switching the unit type.",
            parent=root
        )
        mode_var.set(previous_mode_var.get())  # Revert
        return

    # Safe to proceed
    mode = mode_var.get()
    if mode == "words":
        entry_rate.config(state="disabled")
        entry_price_per_word.config(state="normal")
        entry_value.focus()
    else:
        entry_rate.config(state="normal")
        entry_price_per_word.config(state="disabled")
        entry_value.focus()

    previous_mode_var.set(mode)


# Default divisors
DIVISORS = {
    "words": 250,
    "chars_with_spaces": 1800,
    "chars_without_spaces": 1540
}

# ——— GLOBAL VARIABLES ———
root = tk.Tk()
root.title("Translator Calculator")
root.geometry("450x715")
root.minsize(350, 700)
root.maxsize(600, 715)
root.resizable(True, False)
# Add calculator button to top-right corner
calc_button_frame = tk.Frame(root)
calc_button_frame.pack(fill="x", padx=10, pady=5)

# Spacer to push calculator button to the right
spacer_label = tk.Label(calc_button_frame, text="", bg=current_theme["bg"])
spacer_label.pack(side="left", expand=True)

# Calculator button
calc_icon_btn = tk.Button(
    calc_button_frame,
    text="🧮",
    font=("Verdana", 12),
    bg="#444444",
    fg="white",
    width=3,
    height=1,
    command=open_calculator
)
calc_icon_btn.pack(side="right")
Tooltip(calc_icon_btn, "Open system calculator")

try:
    root.iconbitmap("my_icon.ico")
except tk.TclError:
    print("Icon not found, skipping...")

# Unit type label
tk.Label(root, text="Unit type:", font=("Verdana", 11, "bold")).pack(pady=(0, 5))

# Radio buttons frame for chars
chars_frame = tk.Frame(root, relief="groove", borderwidth=2)
chars_frame.pack(pady=2)

# Radio buttons
mode_var = tk.StringVar(value="chars_with_spaces")
previous_mode_var = tk.StringVar(value="chars_with_spaces")  # Tracks last safe mode

radio_chars_with = tk.Radiobutton(chars_frame, text="Chars with spaces", variable=mode_var, value="chars_with_spaces",
                                  font=("Verdana", 11), indicatoron=1)
radio_chars_with.pack(pady=2)
Tooltip(radio_chars_with, "For text including spaces — (1800 chars ≈ 1 page)")

radio_chars_without = tk.Radiobutton(chars_frame, text="Chars without spaces", variable=mode_var,
                                     value="chars_without_spaces",
                                     font=("Verdana", 11), indicatoron=1)
radio_chars_without.pack(pady=2)
Tooltip(radio_chars_without, "For text without spaces — approx. 1540 per page")

radio_words = tk.Radiobutton(root, text="Words", variable=mode_var, value="words",
                             font=("Verdana", 11), indicatoron=1)
radio_words.pack(pady=2)
Tooltip(radio_words, "Calculation: total words × price per word")

# Input: Value
tk.Label(root, text="Enter number of selected units", font=("Verdana", 11)).pack(pady=(8, 4))
entry_value = tk.Entry(root, font=("Verdana", 12), width=25, justify='center')
entry_value.pack(pady=6)
Tooltip(entry_value, "Enter the total number of words or characters")

# Input fields frame (positioned just below the enter value field)
input_frame = tk.Frame(root, relief="groove", borderwidth=2)
input_frame.pack(pady=5)

# Price input fields
tk.Label(input_frame, text="Enter Price per Page", font=("Verdana", 11)).pack(pady=(7, 4))
entry_rate = tk.Entry(input_frame, font=("Verdana", 11), width=25, justify='center')
entry_rate.pack(pady=4)
entry_rate.bind("<Return>", lambda event: calculate())

tk.Label(input_frame, text="Enter Price per Word", font=("Verdana", 11)).pack(pady=(4, 7))
entry_price_per_word = tk.Entry(input_frame, font=("Verdana", 11), width=25, justify='center')
entry_price_per_word.pack(pady=4)
entry_price_per_word.bind("<Return>", lambda event: calculate())

# Enter key navigation
entry_value.bind("<Return>", lambda event:
entry_price_per_word.focus() if mode_var.get() == "words" else entry_rate.focus())

# ——— Divisor Settings ———
tk.Label(root, text="Divisors (edit as needed):", font=("Verdana", 10, "bold")).pack(pady=(15, 3))
divisor_frame = tk.Frame(root)
divisor_frame.pack(pady=4)

word_div_var = tk.IntVar(value=DIVISORS["words"])
chars_with_spaces_div_var = tk.IntVar(value=DIVISORS["chars_with_spaces"])
chars_without_spaces_div_var = tk.IntVar(value=DIVISORS["chars_without_spaces"])

# Words
tk.Label(divisor_frame, text="Words:", font=("Verdana", 9)).grid(row=0, column=0, sticky="w", padx=(0, 5))
entry_word_div = tk.Entry(divisor_frame, textvariable=word_div_var, width=8, justify='center')
entry_word_div.grid(row=0, column=1, padx=2)
Tooltip(entry_word_div, "Number of words that count as one page (standard = 250)")

# Chars with spaces
tk.Label(divisor_frame, text="Chars + spaces:", font=("Verdana", 9)).grid(row=1, column=0, sticky="w", padx=(0, 5))
entry_chars_with = tk.Entry(divisor_frame, textvariable=chars_with_spaces_div_var, width=8, justify='center')
entry_chars_with.grid(row=1, column=1, padx=2)
Tooltip(entry_chars_with, "Changing this value is not recommended as it is an industry standard")

# Chars without spaces
tk.Label(divisor_frame, text="Chars w/o spaces:", font=("Verdana", 9)).grid(row=2, column=0, sticky="w", padx=(0, 5))
entry_chars_without = tk.Entry(divisor_frame, textvariable=chars_without_spaces_div_var, width=8, justify='center')
entry_chars_without.grid(row=2, column=1, padx=2)
Tooltip(entry_chars_without, "Number of characters without spaces per page (approx. = 1540)")

# ✅ CORRECT PLACE: Attach trace AFTER function is defined, but OUTSIDE the function
mode_var.trace_add("write", update_price_fields)
update_price_fields()  # Initialize field states (disable/enable correct entries)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

# Theme toggle
theme_frame = tk.Frame(root)
theme_frame.pack(pady=4)


def toggle_theme():
    global current_theme
    if current_theme == LIGHT_THEME:
        current_theme = DARK_THEME
        theme_btn.config(text="☀️ Light Mode")
    else:
        current_theme = LIGHT_THEME
        theme_btn.config(text="🌙 Dark Mode")
    apply_theme()


theme_btn = tk.Button(theme_frame, text="🌙 Dark Mode", font=("Verdana", 10),
                      command=toggle_theme, width=12, height=1)
theme_btn.pack()


# ——— FUNCTION DEFINITIONS (must come before being used in widgets) ———
def calculate():
    try:
        num_value = parse_number(entry_value.get())
        selected_mode = mode_var.get()

        if selected_mode == "words":
            price_per_word = parse_number(entry_price_per_word.get())
            result = num_value * price_per_word
            divisor = word_div_var.get()
        else:
            price_rate = parse_number(entry_rate.get())
            divisors = {
                "chars_with_spaces": chars_with_spaces_div_var.get(),
                "chars_without_spaces": chars_without_spaces_div_var.get()
            }
            divisor = divisors[selected_mode]
            result = (num_value / divisor) * price_rate

        pages = num_value / divisor
        update_result_text(f"Cost: {result:.2f} ₽")
        update_pages_text(f"Pages: {pages:.2f}")

        root.clipboard_clear()
        root.clipboard_append(f"{result:.2f}")
        root.update()

    except ValueError:
        update_result_text("Error: Invalid input")
        update_pages_text("Pages: ?")
    except Exception:
        update_result_text("Error")
        update_pages_text("Pages: ?")


def clear_fields():
    """Clear all input fields and reset result"""
    entry_value.delete(0, tk.END)
    entry_rate.delete(0, tk.END)
    entry_price_per_word.delete(0, tk.END)
    update_result_text("Cost: 0.00 ₽")
    update_pages_text("Pages: 0")
    mode_var.set("chars_with_spaces")
    previous_mode_var.set("chars_with_spaces")  # Reset safe mode
    root.clipboard_clear()
    root.update()


def full_reset():
    """Reset everything: inputs, results, AND divisors"""
    global suppress_mode_updates

    suppress_mode_updates = True
    try:
        word_div_var.set(DIVISORS["words"])
        chars_with_spaces_div_var.set(DIVISORS["chars_with_spaces"])
        chars_without_spaces_div_var.set(DIVISORS["chars_without_spaces"])
    finally:
        suppress_mode_updates = False

    clear_fields()  # Already resets inputs and mode
    root.focus_force()  # Add this before messagebox calls
    messagebox.showinfo("Reset", "All fields and divisors have been reset to defaults.", parent=root)


# ——— Now safely create buttons using defined functions ———
button_frame_inner = tk.Frame(button_frame)
button_frame_inner.pack()

calc_btn = tk.Button(button_frame_inner, text="Calculate", font=("Verdana", 12), bg="#4CAF50", fg="white",
                     width=10, height=2, command=calculate)
calc_btn.pack(side=tk.LEFT, padx=5)
Tooltip(calc_btn, "Calculate the cost/press ENTER")

clear_btn = tk.Button(button_frame_inner, text="Clear", font=("Verdana", 12), bg="#FF9800", fg="white",
                      width=10, height=2, command=clear_fields)
clear_btn.pack(side=tk.LEFT, padx=5)
Tooltip(clear_btn, "Clear all input fields/press ESC")

reset_btn = tk.Button(button_frame_inner, text="Reset", font=("Verdana", 12), bg="#f44336", fg="white",
                      width=10, height=2, command=full_reset)
reset_btn.pack(side=tk.LEFT, padx=5)
Tooltip(reset_btn, "Clear all input fields and reset the divisors to defaults")

# Result and Pages (Selectable Text Widgets)
# Cost output
result_text = tk.Text(root, height=1, width=20, font=("Verdana", 16, "bold"),
                      fg="dark green", bg=current_theme["bg"], bd=0, highlightthickness=0,
                      wrap=tk.WORD, relief=tk.FLAT, state=tk.DISABLED)
result_text.pack(pady=3)

# Pages output
pages_text = tk.Text(root, height=1, width=20, font=("Verdana", 16, "bold"),
                     fg="navy blue", bg=current_theme["bg"], bd=0, highlightthickness=0,
                     wrap=tk.WORD, relief=tk.FLAT, state=tk.DISABLED)
pages_text.pack(pady=3)

# Make them look like labels but allow selection
def update_result_text(text):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(1.0, text)
    result_text.config(state=tk.DISABLED)

def update_pages_text(text):
    pages_text.config(state=tk.NORMAL)
    pages_text.delete(1.0, tk.END)
    pages_text.insert(1.0, text)
    pages_text.config(state=tk.DISABLED)

def create_context_menu(text_widget):
    menu = tk.Menu(text_widget, tearoff=0)
    menu.add_command(label="Copy", command=lambda: text_widget.event_generate("<<Copy>>"))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    text_widget.bind("<Button-3>", show_menu)


# Add context menus
create_context_menu(result_text)
create_context_menu(pages_text)
# Footer
footer_label = tk.Label(
    root,
    text="© 2025 Created by AStar/Kartalo Studio",
    font=("Verdana", 8, "italic"),
    fg="dimgray",
    bg="lightgray"
)
footer_label.pack(side="bottom", fill="x", ipady=5)

# Initialize
clear_fields()
apply_theme()
root.bind("<Escape>", lambda event: clear_fields())

# Run
root.mainloop()