import tkinter as tk
from tkinter import ttk, messagebox
import threading
from scraper import NewsScraper
from risk_assessment import SecurityRiskAssessment

# Contoh data users
users = [
    {"id": 1, "name": "Admin 1", "email": "admin1@example.com"},
    {"id": 2, "name": "Admin 2", "email": "admin2@example.com"},
    {"id": 3, "name": "User 1", "email": "user1@example.com"}
]

# Global variables
current_headlines = []
risk_assessor = SecurityRiskAssessment()

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


def update_risk_assessment():
    """Update risk assessment display based on current headlines"""
    global current_headlines
    
    if not current_headlines:
        # Clear the risk assessment display
        risk_score_label.config(text="--", bg="#CCCCCC")
        risk_level_label.config(text="Data belum tersedia")
        risk_status_label.config(text="")
        risk_description_label.config(text="Fetch berita terlebih dahulu untuk melihat penilaian keamanan")
        
        # Clear breakdown
        for row in tree_breakdown.get_children():
            tree_breakdown.delete(row)
        
        # Clear articles
        for row in tree_risk_articles.get_children():
            tree_risk_articles.delete(row)
        
        return
    
    # Calculate risk assessment
    risk_result = risk_assessor.analyze_articles_with_risk(current_headlines)
    risk_score = risk_result['risk_score']
    level_info = risk_result['level_info']
    
    # Update main risk score display
    risk_score_label.config(text=str(risk_score), bg=level_info['color'], fg="white")
    risk_level_label.config(text=level_info['level'], fg=level_info['color'])
    risk_status_label.config(text=level_info['description'])
    risk_description_label.config(text=risk_result['details'])
    
    # Update keyword breakdown
    for row in tree_breakdown.get_children():
        tree_breakdown.delete(row)
    
    for category, count in risk_result['keyword_breakdown'].items():
        tree_breakdown.insert("", tk.END, values=(category.capitalize(), count))
    
    # Update risky articles
    for row in tree_risk_articles.get_children():
        tree_risk_articles.delete(row)
    
    risky_articles = [a for a in risk_result['articles'] if a.get('has_risk_keywords', False)]
    for idx, article in enumerate(risky_articles, 1):
        keywords_str = ", ".join([k[1] for k in article.get('risk_keywords', [])])
        tree_risk_articles.insert("", tk.END, values=(
            idx,
            article['title'][:40] + "..." if len(article['title']) > 40 else article['title'],
            article['source'],
            keywords_str[:30] + "..." if len(keywords_str) > 30 else keywords_str
        ))

# Fungsi scraping news headlines
def fetch_news():
    """Fetch news headlines in a separate thread"""
    try:
        btn_fetch_news.config(state=tk.DISABLED, text="Loading...")
        
        def scrape_in_thread():
            global current_headlines
            try:
                scraper = NewsScraper()
                headlines = scraper.get_all_headlines()
                current_headlines = headlines
                
                # Clear existing items in news tab
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
                
                # Update risk assessment
                update_risk_assessment()
                
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

# ==================== TAB 2: SECURITY RISK ASSESSMENT ====================
tab_risk = ttk.Frame(notebook)
notebook.add(tab_risk, text="Security Risk Assessment")

# Main risk score display
frame_risk_main = tk.Frame(tab_risk)
frame_risk_main.pack(pady=20)

tk.Label(frame_risk_main, text="Tingkat Keamanan Daerah:", font=("Arial", 12, "bold")).pack()

# Risk score in big circle
risk_score_label = tk.Label(frame_risk_main, text="--", font=("Arial", 60, "bold"), 
                            width=5, height=2, bg="#CCCCCC", fg="white", relief=tk.RAISED)
risk_score_label.pack(pady=10)

tk.Label(frame_risk_main, text="Skala 0-5", font=("Arial", 10)).pack()

risk_level_label = tk.Label(frame_risk_main, text="Data belum tersedia", font=("Arial", 16, "bold"), fg="#999999")
risk_level_label.pack(pady=5)

risk_status_label = tk.Label(frame_risk_main, text="", font=("Arial", 11))
risk_status_label.pack(pady=5)

risk_description_label = tk.Label(frame_risk_main, text="Fetch berita terlebih dahulu untuk melihat penilaian keamanan", 
                                  font=("Arial", 9), fg="#666666", wraplength=400)
risk_description_label.pack(pady=10)

# Frame for breakdown
frame_breakdown = tk.LabelFrame(tab_risk, text="Breakdown Jenis Kejahatan", font=("Arial", 11, "bold"))
frame_breakdown.pack(pady=10, padx=10, fill=tk.X)

breakdown_columns = ("Kategori", "Jumlah")
tree_breakdown = ttk.Treeview(frame_breakdown, columns=breakdown_columns, show="headings", height=5)
for col in breakdown_columns:
    tree_breakdown.heading(col, text=col)
    if col == "Kategori":
        tree_breakdown.column(col, width=150)
    else:
        tree_breakdown.column(col, width=80)
tree_breakdown.pack(fill=tk.X, padx=5, pady=5)

# Frame for risky articles
frame_risk_articles = tk.LabelFrame(tab_risk, text="Artikel yang Mengandung Kata Kunci Risiko", font=("Arial", 11, "bold"))
frame_risk_articles.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar_risk = ttk.Scrollbar(frame_risk_articles)
scrollbar_risk.pack(side=tk.RIGHT, fill=tk.Y)

risk_articles_columns = ("No", "Judul", "Sumber", "Kata Kunci")
tree_risk_articles = ttk.Treeview(frame_risk_articles, columns=risk_articles_columns, show="headings", 
                                  height=10, yscrollcommand=scrollbar_risk.set)
scrollbar_risk.config(command=tree_risk_articles.yview)
for col in risk_articles_columns:
    tree_risk_articles.heading(col, text=col)
    if col == "Judul":
        tree_risk_articles.column(col, width=250)
    elif col == "Kata Kunci":
        tree_risk_articles.column(col, width=150)
    else:
        tree_risk_articles.column(col, width=80)
tree_risk_articles.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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