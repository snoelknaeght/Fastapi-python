import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000"

def fetch_tasks():
    response = requests.get(f"{API_URL}/task")
    if response.status_code == 200:
        tasks = response.json()
        result_text.delete(1.0, tk.END)
        for task in tasks:
            result_text.insert(tk.END, f"ID: {task[0]}, Description: {task[1]}, Statut: {task[2]}, Priorité: {task[3]}, UserId: {task[4]}\n")
    else:
        messagebox.showerror("Impossible de récupérer les tâches")

def add_task():
    description = description_entry.get()
    statut = status_entry.get()
    priorite = priority_entry.get()
    user_id = user_id_entry.get()

    if not description or not statut or not priorite or not user_id:
        messagebox.showwarning("Tous les champs sont obligatoires")
        return

    data = {
        "Description": description,
        "Status": statut,
        "Priority": int(priorite),
        "UserId": int(user_id)
    }
    response = requests.post(f"{API_URL}/task", json=data)
    if response.status_code == 201:
        messagebox.showinfo("Tâche ajoutée avec succès")
        fetch_tasks()
    else:
        messagebox.showerror(response.json().get("detail", "Erreur inconnue"))

root = tk.Tk()
root.title("Gestion des tâches")

tk.Label(root, text="Description:").grid(row=0, column=0, padx=5, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Statut:").grid(row=1, column=0, padx=5, pady=5)
status_entry = tk.Entry(root)
status_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Priorité:").grid(row=2, column=0, padx=5, pady=5)
priority_entry = tk.Entry(root)
priority_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="UserId:").grid(row=3, column=0, padx=5, pady=5)
user_id_entry = tk.Entry(root)
user_id_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Ajouter une tâche", command=add_task)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
