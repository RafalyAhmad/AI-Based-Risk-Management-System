import tkinter as tk
from tkinter import ttk, messagebox
import threading
from scraper import NewsScraper

# Contoh data users
users = [
    {"id": 1, "name": "Admin 1", "email": "admin1@example.com"},
    {"id": 2, "name": "Admin 2", "email": "admin2@example.com"},
    {"id": 3, "name": "User 1", "email": "user1@example.com"}
]

# Fungsi tambah user
def add_user():
    new_id = len(users) + 1
    name = name_entry.get()
    email = email_entry.get()
    if not name or not email:
        messagebox.showwarning("Warning", "Name and Email cannot be empty!")
        return
    users.append({"id": new_id, "name": name, "email": email})
    refresh_table()
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Refresh tabel
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for user in users:
        tree.insert("", tk.END, values=(user["id"], user["name"], user["email"]))

# Fungsi scraping news headlines
def fetch_news():
    """Fetch news headlines in a separate thread"""
    try:
        btn_fetch_news.config(state=tk.DISABLED, text="Loading...")
        
        def scrape_in_thread():
            try:
                scraper = NewsScraper()
                headlines = scraper.get_all_headlines()
                
                # Clear existing items
                for row in tree_news.get_children():
                    tree_news.delete(row)
                
                # Insert new headlines
                for idx, article in enumerate(headlines, 1):
                    tree_news.insert("", tk.END, values=(
                        idx,
                        article['title'][:50] + "..." if len(article['title']) > 50 else article['title'],
                        article['source'],
                        article['category']
                    ))
                
                messagebox.showinfo("Success", f"Fetched {len(headlines)} news headlines!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch news: {str(e)}")
            finally:
                btn_fetch_news.config(state=tk.NORMAL, text="Fetch News")
        
        thread = threading.Thread(target=scrape_in_thread, daemon=True)
        thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
        btn_fetch_news.config(state=tk.NORMAL, text="Fetch News")


# Window utama
root = tk.Tk()
root.title("Admin Dashboard with News Scraper")
root.geometry("800x600")

# Create Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# ==================== TAB 1: USER MANAGEMENT ====================
tab_users = ttk.Frame(notebook)
notebook.add(tab_users, text="User Management")

# Frame tabel
frame_table = tk.Frame(tab_users)
frame_table.pack(pady=10)

# Treeview (tabel)
columns = ("ID", "Name", "Email")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=220)
tree.pack()

# Frame input
frame_input = tk.Frame(tab_users)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame_input)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Email:").grid(row=1, column=0, padx=5, pady=5)
email_entry = tk.Entry(frame_input)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Add User", command=add_user).grid(row=2, column=0, columnspan=2, pady=10)

# ==================== TAB 2: NEWS SCRAPER ====================
tab_news = ttk.Frame(notebook)
notebook.add(tab_news, text="News Headlines Scraper")

# Frame for news controls
frame_news_controls = tk.Frame(tab_news)
frame_news_controls.pack(pady=10)

tk.Label(frame_news_controls, text="Select News Sources:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

btn_fetch_news = tk.Button(frame_news_controls, text="All Sources (BBC, CNN, Detik)", command=fetch_news, 
                           bg="#4CAF50", fg="white", padx=10, pady=5)
btn_fetch_news.pack(side=tk.LEFT, padx=5)

# Frame for news table
frame_news_table = tk.Frame(tab_news)
frame_news_table.pack(pady=10, fill=tk.BOTH, expand=True)

# Scrollbar for news table
scrollbar = ttk.Scrollbar(frame_news_table)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview for news results
news_columns = ("No", "Headline", "Source", "Category")
tree_news = ttk.Treeview(frame_news_table, columns=news_columns, show="headings", height=18, yscrollcommand=scrollbar.set)
scrollbar.config(command=tree_news.yview)
for col in news_columns:
    tree_news.heading(col, text=col)
    if col == "Headline":
        tree_news.column(col, width=350)
    else:
        tree_news.column(col, width=100)
tree_news.pack(fill=tk.BOTH, expand=True)

# Tampilkan data awal
refresh_table()

# Jalankan GUI
root.mainloop()