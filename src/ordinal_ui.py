import tkinter as tk
from tkinter import StringVar


def reorder_listbox(listbox, direction):
    """Reorder selected item in a listbox."""
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]

    # Move up
    if direction == "up" and index > 0:
        value = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index - 1, value)
        listbox.selection_set(index - 1)

    # Move down
    elif direction == "down" and index < listbox.size() - 1:
        value = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index + 1, value)
        listbox.selection_set(index + 1)


def prompt_user_for_recode(column_name, unique_values):
    """
    Create a UI to prompt the user for recoding options and ordering for each column.
    Returns the ordered values and whether the column should be recoded as ordinal.
    """
    root = tk.Tk()
    root.title(f"Recode and Order Column")

    # Get screen height for dynamic base height calculation
    screen_height = root.winfo_screenheight()

    # Dynamically calculate base height as a percentage of screen height (e.g., 60%)
    base_height = int(
        screen_height * 0.6
    )  # 60% of the screen height for base UI
    listbox_height = len(unique_values) * 25  # Estimate 25px per listbox item
    total_height = (
        base_height + listbox_height + 100
    )  # Total window height with padding

    # Set minimum and maximum window width
    window_width = 720  # 20% wider than the original 600px
    root.geometry(f"{window_width}x{total_height}+100+100")

    # Force window to the front
    root.lift()
    root.attributes("-topmost", True)

    # Layout for Yes/No and Confirm buttons
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    # Label with text wrapping for long column names
    label_text = (
        f"Do you want to recode '{column_name}' as an ordinal variable?"
    )
    label = tk.Label(
        top_frame,
        text=label_text,
        wraplength=window_width - 100,
        justify="left",
    )
    label.grid(row=0, column=0, columnspan=2)

    # Stack Yes/No vertically
    recode_var = StringVar(value="no")  # Default to "No"
    yes_button = tk.Radiobutton(
        top_frame, text="Yes", variable=recode_var, value="yes", width=10
    )
    no_button = tk.Radiobutton(
        top_frame, text="No", variable=recode_var, value="no", width=10
    )
    yes_button.grid(row=1, column=0, pady=5)
    no_button.grid(row=2, column=0, pady=5)

    # Place Confirm button to the right, centered between Yes/No
    confirm_button = tk.Button(
        top_frame, text="Confirm", command=lambda: root.quit(), width=10
    )
    confirm_button.grid(row=1, column=1, rowspan=2, padx=20, pady=10)

    # Label for reorder instructions
    tk.Label(
        root, text="Reorder the unique values (top is smallest ordinal):"
    ).pack(pady=10)

    # Create listbox for unique values
    listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    for val in unique_values:
        listbox.insert(tk.END, str(val))
    listbox.pack(expand=True, fill="both", padx=10, pady=10)

    # Add reorder buttons at the bottom
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(
        button_frame,
        text="Move Up",
        command=lambda: reorder_listbox(listbox, "up"),
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Move Down",
        command=lambda: reorder_listbox(listbox, "down"),
    ).grid(row=0, column=1, padx=5)

    # Start the tkinter event loop
    root.mainloop()

    # Retrieve the order before the window is destroyed
    ordered_values = [listbox.get(i) for i in range(listbox.size())]

    # Now it's safe to destroy the window after we're done
    root.destroy()

    # Return user selection and ordering
    return ordered_values, recode_var.get()
