import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from recommender.recommender import recommendArticles
from recommender.preprocessing import get_stemmer, get_lemmatizer
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RecommenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wikipedia Article Recommender")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=1, fill="both")

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

    def create_tab1(self):
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="📚 Recommendations")

        # History input
        tk.Label(self.tab1, text="Enter articles you've read (comma-separated):").pack(pady=(10, 0))
        self.entry = tk.Entry(self.tab1, width=80)
        self.entry.pack(pady=(0, 10))

        # Top N recommendations
        tk.Label(self.tab1, text="Number of recommendations (default 5):").pack()
        self.top_n_entry = tk.Entry(self.tab1)
        self.top_n_entry.insert(0, "5")
        self.top_n_entry.pack()

        # Explanation terms
        tk.Label(self.tab1, text="Number of explanation terms (default 0):").pack()
        self.expl_terms_entry = tk.Entry(self.tab1)
        self.expl_terms_entry.insert(0, "0")
        self.expl_terms_entry.pack(pady=(0, 10))

        # Button
        self.submit_button = tk.Button(self.tab1, text="Get Recommendations", command=self.get_recommendations)
        self.submit_button.pack(pady=(5, 10))

        # Output area
        self.output = tk.Text(self.tab1, height=15, width=100, wrap="word")
        self.output.pack()
        self.output.tag_config("bold", font=("Helvetica", 10, "bold"))
        self.output.tag_config("explain", foreground="gray")

    def create_tab2(self):
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="⚙️ Preprocessing Settings")

        # Stemmer
        self.stemmer_var = tk.StringVar(value="porter")
        tk.Label(self.tab2, text="Select stemmer:").pack(pady=(10, 0))
        for stemmer in ["porter", "lancaster", "none"]:
            tk.Radiobutton(self.tab2, text=stemmer.capitalize(), variable=self.stemmer_var, value=stemmer).pack()

        # Tokenizer
        self.tokenizer_var = tk.StringVar(value="word_tokenize")
        tk.Label(self.tab2, text="Select tokenizer:").pack(pady=(10, 0))
        tk.OptionMenu(self.tab2, self.tokenizer_var, "word_tokenize", "wordpunct_tokenize").pack()

        # Lemmatizer
        self.use_lemmatizer_var = tk.BooleanVar()
        tk.Checkbutton(self.tab2, text="Use lemmatizer instead of stemmer", variable=self.use_lemmatizer_var).pack(pady=10)

    def create_tab3(self):
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="📊 Similarity Plot")

        self.figure = plt.Figure(figsize=(8, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.tab3)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

    def get_recommendations(self):
        history = [h.strip() for h in self.entry.get().split(",")]
        stemmer_choice = self.stemmer_var.get()
        tokenizer_choice = self.tokenizer_var.get()
        use_lemmatizer = self.use_lemmatizer_var.get()

        tokenizer = word_tokenize if tokenizer_choice == "word_tokenize" else wordpunct_tokenize
        stemmer = None if stemmer_choice == "none" else get_stemmer(stemmer_choice)
        lemmatizer = get_lemmatizer("") if use_lemmatizer else None

        try:
            top_n = int(self.top_n_entry.get())
        except ValueError:
            top_n = 5

        try:
            explanation_terms = int(self.expl_terms_entry.get())
        except ValueError:
            explanation_terms = 0

        try:
            df = pd.read_csv("data/processedArticles.csv")
            recs = recommendArticles(
                history,
                df,
                tokenizer=tokenizer,
                stemmer=stemmer,
                lemmatizer=lemmatizer,
                useLemmatizer=use_lemmatizer,
                top_n=top_n,
                explanation_terms=explanation_terms
            )

            self.output.delete(1.0, tk.END)

            for index, row in recs.iterrows():
                title = row['title']
                url = row['link']
                similarity = row['similarity']
                explanation = row['explanation']

                start_index = self.output.index(tk.END)
                self.output.insert(tk.END, f"{title} - ", "bold")
                self.output.insert(tk.END, f"{url}", f"link{index}")
                self.output.insert(tk.END, f" - Score: {similarity:.2f}\n\n")
                self.output.insert(tk.END, f"Top terms: {explanation}\n\n", "explain")

                url_start = start_index + f"+{len(title)+3}c"
                url_end = url_start + f"+{len(url)}c"
                self.output.tag_add(f"link{index}", url_start, url_end)
                self.output.tag_config(f"link{index}", foreground="blue", underline=True)
                self.output.tag_bind(f"link{index}", "<Button-1>", lambda e, url=url: webbrowser.open(url))

            # Update embedded plot
            self.ax.clear()
            titles = recs['title']
            scores = recs['similarity']
            self.ax.barh(titles[::-1], scores[::-1])
            self.ax.set_xlabel("Similarity")
            self.ax.set_title("Recommended Article Similarity Scores")
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
