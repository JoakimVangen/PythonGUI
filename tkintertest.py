import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
# Importerer modulene som trengs for oppgaven


# Funksjon som kobler til databasen
def connect_to_database():
    conn = sqlite3.connect('personer.db') # Kobler til databasen
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, postal_number TEXT)''') # Lager tabellen hvis den ikke finnes med de riktige kolonnene
    conn.commit() # Lagrer endringene
    return conn, c 

# Funksjon for å søke etter en bruker
def search_user(conn, c):
    user_name = user_name_entry.get() # Henter brukernavnet fra input-feltet
    c.execute("SELECT * FROM users WHERE name=?", (user_name,)) # Søker etter brukeren i databasen
    result = c.fetchall() # Henter resultatet fra søket
    if result:
        display_result(result) # Viser resultatet
    else:
        messagebox.showinfo("Information", "No user found with this name.") # Gir en melding hvis brukeren ikke finnes

# Funksjon som viser resultatet i en tabell
def display_result(result): 
    for widget in result_frame.winfo_children(): # Fjerner tidligere resultater
        widget.destroy() 

    tree = ttk.Treeview(result_frame, columns=("ID", "Name", "Email", "Postal Number"), show="headings") # Lager en tabell som viser resultatet
    tree.heading("ID", text="ID") 
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Postal Number", text="Postal Number")
    tree.pack(side="left", fill="both", expand=True) 

    for row in result:
        tree.insert("", "end", values=row) # Legger til radene i tabellen

# Funksjon som legger til en bruker
def add_user(conn, c): 
    user_name = new_user_name_entry.get() # Henter brukernavnet fra input-feltet
    user_email = new_user_email_entry.get() # Henter e-posten fra input-feltet
    user_postal_number = new_user_postal_number_entry.get() # Henter postnummeret fra input-feltet
    c.execute("INSERT INTO users (name, email, postal_number) VALUES (?, ?, ?)", (user_name, user_email, user_postal_number)) # Legger til dataen i databasen
    conn.commit() 
    if not user_name or not user_email or not user_postal_number: # Gir en feilmelding hvis ikke alle feltene er fylt ut
        messagebox.showerror("Error", "Please fill in all fields.")
        return False
    else: 
        messagebox.showinfo("Information", "User added successfully.") # Gir en melding om at brukeren er lagt til

# Funskjon som sletter en bruker
def delete_user(conn, c):
    user_id = delete_user_id_entry.get() # Henter bruker-IDen fra input-feltet
    c.execute("SELECT * FROM users WHERE id=?", (user_id,)) # Sjekker om brukeren finnes
    result = c.fetchone()
    if result:
        c.execute("DELETE FROM users WHERE id=?", (user_id,)) # Sletter brukeren hvis den finnes
        conn.commit()
        messagebox.showinfo("Information", "User deleted successfully.") # Gir en melding om at brukeren er slettet
    else:
        messagebox.showerror("Error", "User ID does not exist.") # Gir en feilmelding hvis brukeren ikke finnes

# Lager tkinter GUI vinduet
root = tk.Tk()
root.title("User Management") # Setter tittelen på vinduet

# Kobler til databasen
conn, c = connect_to_database() 

# Lager input-feltene og knappene
user_search_label = ttk.Label(root, text="Search User:") # Lager et felt for å søke etter brukere
user_search_label.grid(row=0, column=0, padx=5, pady=5, sticky="e") # Plasserer knappen
user_name_entry = ttk.Entry(root)
user_name_entry.grid(row=0, column=1, padx=5, pady=5)
search_button = ttk.Button(root, text="Search", command=lambda: search_user(conn, c)) # Lager en knappen som brukeren kan trykke på
search_button.grid(row=0, column=2, padx=5, pady=5) 

result_frame = ttk.Frame(root) # Lager et ramme for resultatet
result_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

new_user_name_label = ttk.Label(root, text="New User Name:") # Lager et nytt brukernavn felt for laging av nye brukere
new_user_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e") # Plasserer feltet
new_user_name_entry = ttk.Entry(root)
new_user_name_entry.grid(row=2, column=1, padx=5, pady=5)

new_user_email_label = ttk.Label(root, text="New User Email:") # Lager et nytt e-post felt for laging av nye brukere
new_user_email_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")  # Plasserer feltet
new_user_email_entry = ttk.Entry(root)
new_user_email_entry.grid(row=3, column=1, padx=5, pady=5)

new_user_postal_number_label = ttk.Label(root, text="New User Postal Number:") # Lager et nytt postnummer felt for laging av nye brukere
new_user_postal_number_label.grid(row=4, column=0, padx=5, pady=5, sticky="e") # Plasserer feltet
new_user_postal_number_entry = ttk.Entry(root)
new_user_postal_number_entry.grid(row=4, column=1, padx=5, pady=5)

add_button = ttk.Button(root, text="Add User", command=lambda: add_user(conn, c)) # Lager en knapp for å legge til brukere
add_button.grid(row=4, column=2, padx=5, pady=5) # Plasserer knappen

delete_user_id_label = ttk.Label(root, text="User ID to Delete:") # Lager et felt for å slette brukere
delete_user_id_label.grid(row=5, column=0, padx=5, pady=5, sticky="e") # Plasserer feltet
delete_user_id_entry = ttk.Entry(root)
delete_user_id_entry.grid(row=5, column=1, padx=5, pady=5)

delete_button = ttk.Button(root, text="Delete User", command=lambda: delete_user(conn, c)) # Lager en knapp for å slette brukere
delete_button.grid(row=5, column=2, padx=5, pady=5)

root.mainloop() # Starter GUI-vinduet

# Close the database connection when the program exits
conn.close() # Lukker databasetilkoblingen når programmet avsluttes
