import tkinter as tk
from gui import RecommenderGUI
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')  # ← optional but good for lemmatizer
nltk.download('punkt_tab')  # ← fix for your issue
import ttkbootstrap as tb


if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = RecommenderGUI(root)
    root.mainloop()
    root.protocol("WM_DELETE_WINDOW", root.destroy)