import tkinter as tk
from tkinter import ttk

def Label(tk, container, label):
    label = tk.Label(container, text=label)
    label.pack(padx=5, pady=5)
    return label

def Field(tk, container, label, default_value = None):
    Label(tk, container, label)
    entry = tk.Entry(container)
    if default_value is not None:
      entry.insert(0, default_value)
    entry.pack(padx=5, pady=5)
    return entry

def Button(tk, container, text, command):
    button = tk.Button(container, text=text, command=command)
    button.pack(padx=5, pady=10)
    return button

def Dropdown(tk, container, label, values, has_label=False, default="", textvariable= None):
    if has_label:
        Label(tk, container, label)
    
    dropdown = ttk.Combobox(container, values=values, textvariable=textvariable)
    if default:
        dropdown.set(default)
    dropdown.pack(padx=5, pady=5)
    return dropdown

def Form(tk, parent, title):
    form = tk.Toplevel(parent)
    form.title(title)
    return form