import tkinter as tk
from tkinter import messagebox
import pandas as pd
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from recommender.recommender import recommendArticles
from recommender.preprocessing import get_stemmer, get_lemmatizer
import webbrowser

def open_link(event):
    url = event.widget.get("current line")  # Or however you get the URL
    webbrowser.open(url)

class RecommenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wikipedia Article Recommender")

        # --- User input ---
        self.label = tk.Label(master, text="Enter articles you've read (comma-separated):")
        self.label.pack()

        self.entry = tk.Entry(master, width=80)
        self.entry.pack()

        # --- Stemmer selection ---
        self.stemmer_var = tk.StringVar(value="porter")
        tk.Label(master, text="Select stemmer:").pack()
        for stemmer in ["porter", "lancaster", "none"]:
            tk.Radiobutton(master, text=stemmer.capitalize(), variable=self.stemmer_var, value=stemmer).pack()

        # --- Tokenizer dropdown ---
        self.tokenizer_var = tk.StringVar(value="word_tokenize")
        tk.Label(master, text="Select tokenizer:").pack()
        tk.OptionMenu(master, self.tokenizer_var, "word_tokenize", "wordpunct_tokenize").pack()

        # --- Lemmatizer toggle ---
        self.use_lemmatizer_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Use lemmatizer instead of stemmer", variable=self.use_lemmatizer_var).pack()

        # --- Submit button ---
        self.submit_button = tk.Button(master, text="Get Recommendations", command=self.get_recommendations)
        self.submit_button.pack()

        # --- Output area ---
        self.output = tk.Text(master, height=15, width=100)
        self.output.pack()

    def get_recommendations(self):
        history = [h.strip() for h in self.entry.get().split(",")]
        stemmer_choice = self.stemmer_var.get()
        tokenizer_choice = self.tokenizer_var.get()
        use_lemmatizer = self.use_lemmatizer_var.get()

        # Get the actual tokenizer function
        if tokenizer_choice == "word_tokenize":
            tokenizer = word_tokenize
        else:
            tokenizer = wordpunct_tokenize

        # Get the actual stemmer or lemmatizer object
        stemmer = None if stemmer_choice == "none" else get_stemmer(stemmer_choice)
        lemmatizer = get_lemmatizer("") if use_lemmatizer else None

        try:
            df = pd.read_csv("data/processedArticles.csv")
            recs = recommendArticles(
                history,
                df,
                tokenizer=tokenizer,
                stemmer=stemmer,
                lemmatizer=lemmatizer,
                useLemmatizer=use_lemmatizer,
                top_n=5
            )

            self.output.delete(1.0, tk.END)

            for index, row in recs.iterrows():
                title = row['title']
                url = row['link']
                similarity = row['similarity']

                # Insert article info
                start_index = self.output.index(tk.END)
                self.output.insert(tk.END, f"{title} - ", "bold")
                self.output.insert(tk.END, f"{url}", f"link{index}")
                self.output.insert(tk.END, f" - Score: {similarity:.2f}\n\n")

                # Add tag and binding for clickable link
                self.output.tag_add(f"link{index}", start_index + f"+{len(title)+3}c", start_index + f"+{len(title)+3+len(url)}c")
                self.output.tag_config(f"link{index}", foreground="blue", underline=True)
                self.output.tag_bind(f"link{index}", "<Button-1>", lambda e, url=url: webbrowser.open(url))

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

