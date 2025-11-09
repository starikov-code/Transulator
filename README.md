# kartalo
Translator calculator Transulator

A Python desktop application built with Tkinter for calculating translation costs based on different units (words, characters with/without spaces) with customizable page divisors.

Features
Multiple Calculation Modes: Words, characters with spaces, or characters without spaces
Customizable Divisors: Edit the number of units per page (default: 250 words, 1800 chars with spaces, 1540 chars without spaces)
Dual Themes: Light and dark mode toggle
System Calculator Integration: Opens native OS calculator (Windows/macOS/Linux)
Input Validation: Accepts both comma and dot as decimal separators
Auto-Copy: Results automatically copied to clipboard
Context Menus: Right-click to copy results
Tooltips: Hover over elements for usage hints
Keyboard Shortcuts:
Enter to calculate
Esc to clear fields
Requirements
Python 3.x
Tkinter (usually included with Python)
Usage
Select calculation mode (words/chars)
Enter the number of units and price per page/word
Click "Calculate" or press Enter
Results show total cost and page count
Toggle between light/dark themes using the theme button
Notes
Unit type switching is disabled when input fields contain data to prevent calculation errors
Custom divisor values are preserved during session
Results are automatically copied to clipboard for easy transfer 
