import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Create Main App Window
root = tk.Tk()
root.title("Smart Fitness Tracker")
root.geometry("400x450")

# Data Storage
fitness_data = []

# Function to Add Entry
def add_entry():
    name = name_entry.get()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        # Convert height from cm to meters if needed
        if height > 3:  
            height = height / 100  

        steps = int(steps_entry.get())
        calories = int(calories_entry.get())

        bmi = round(weight / (height ** 2), 2)  # Corrected BMI Calculation
        fitness_data.append({"Name": name, "Weight": weight, "Height": height, "Steps": steps, "Calories": calories, "BMI": bmi})

        messagebox.showinfo("Success", f"{name}'s Data Submitted Successfully! BMI: {bmi}")

        # Clear Input Fields After Submission
        name_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        steps_entry.delete(0, tk.END)
        calories_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values!")

# Function to Show Summary & Graph
def show_summary():
    if not fitness_data:
        messagebox.showwarning("No Data", "No entries found!")
        return

    df = pd.DataFrame(fitness_data)
    print("\n📊 Fitness Summary:\n", df)

    # Graph: Steps vs Calories
    df.plot(x="Name", y=["Steps", "Calories"], kind="bar", figsize=(8, 5), title="Steps vs Calories Burned")
    plt.xlabel("User")
    plt.ylabel("Count")
    plt.show()

# Create Form Labels & Entries
tk.Label(root, text="Enter Your Fitness Data", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Weight (kg):").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m or cm):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Steps Walked:").pack()
steps_entry = tk.Entry(root)
steps_entry.pack()

tk.Label(root, text="Calories Burned:").pack()
calories_entry = tk.Entry(root)
calories_entry.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=add_entry, bg="green", fg="white", font=("Arial", 10, "bold"))
submit_button.pack(pady=5)

# Show Summary Button
summary_button = tk.Button(root, text="Show Summary", command=show_summary, bg="blue", fg="white", font=("Arial", 10, "bold"))
summary_button.pack(pady=5)

# Run GUI App
root.mainloop()
