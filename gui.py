import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
        master.geometry("900x650")

        # Create notebook with tabs
        self.notebook = tb.Notebook(master, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tab_input = tb.Frame(self.notebook)
        self.tab_settings = tb.Frame(self.notebook)
        self.tab_plot = tb.Frame(self.notebook)

        self.notebook.add(self.tab_input, text="📚 Recommendations")
        self.notebook.add(self.tab_settings, text="⚙️ Preprocessing")
        self.notebook.add(self.tab_plot, text="📊 Plot")

        self.build_input_tab()
        self.build_settings_tab()
        self.build_plot_tab()

    def build_input_tab(self):
        # Article input
        tb.Label(self.tab_input, text="Enter articles you've read (comma-separated):", font=("Helvetica", 12)).pack(pady=10)
        self.entry = tb.Entry(self.tab_input, width=100)
        self.entry.pack()

        # Number of recommendations
        tb.Label(self.tab_input, text="Number of recommendations:", font=("Helvetica", 10)).pack(pady=(15, 0))
        self.top_n_entry = tb.Entry(self.tab_input)
        self.top_n_entry.insert(0, "5")
        self.top_n_entry.pack()

        # Number of explanation terms
        tb.Label(self.tab_input, text="Number of explanation terms:", font=("Helvetica", 10)).pack(pady=(15, 0))
        self.expl_terms_entry = tb.Entry(self.tab_input)
        self.expl_terms_entry.insert(0, "0")
        self.expl_terms_entry.pack()

        # Submit button
        self.submit_button = tb.Button(self.tab_input, text="✨ Get Recommendations", bootstyle="success", command=self.get_recommendations)
        self.submit_button.pack(pady=20)

        # Output area
        self.output = tk.Text(self.tab_input, height=18, width=110, wrap="word")
        self.output.pack(pady=5)
        self.output.tag_config("bold", font=("Helvetica", 10, "bold"))
        self.output.tag_config("explain", foreground="gray")

    def build_settings_tab(self):
        # Stemmer
        self.stemmer_var = tk.StringVar(value="porter")
        tb.Label(self.tab_settings, text="Select stemmer:", font=("Helvetica", 11)).pack(pady=10)
        for stemmer in ["porter", "lancaster", "none"]:
            tb.Radiobutton(self.tab_settings, text=stemmer.capitalize(), variable=self.stemmer_var, value=stemmer).pack()

        # Tokenizer
        self.tokenizer_var = tk.StringVar(value="word_tokenize")
        tb.Label(self.tab_settings, text="Select tokenizer:", font=("Helvetica", 11)).pack(pady=10)
        tb.OptionMenu(self.tab_settings, self.tokenizer_var, "word_tokenize", "wordpunct_tokenize").pack()

        # Lemmatizer
        self.use_lemmatizer_var = tk.BooleanVar()
        tb.Checkbutton(self.tab_settings, text="Use lemmatizer instead of stemmer", variable=self.use_lemmatizer_var).pack(pady=15)

    def build_plot_tab(self):
        self.plot_frame = tb.Frame(self.tab_plot)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

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
                if explanation_terms > 0:
                    self.output.insert(tk.END, f"Top terms: {explanation}\n\n", "explain")

                self.output.tag_add(f"link{index}", start_index + f"+{len(title)+3}c", start_index + f"+{len(title)+3+len(url)}c")
                self.output.tag_config(f"link{index}", foreground="blue", underline=True)
                self.output.tag_bind(f"link{index}", "<Button-1>", lambda e, url=url: webbrowser.open(url))

            # --- Embedded plot ---
            self.show_plot(recs)



        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def show_plot(self, recs):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4))
        titles = recs['title']
        scores = recs['similarity']

        ax.barh(titles[::-1], scores[::-1])
        ax.set_xlabel("Similarity")
        ax.set_title("Recommended Article Similarity Scores")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



