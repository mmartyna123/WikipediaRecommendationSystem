import tkinter as tk
from gui import RecommenderGUI
import nltk
# Automatically download necessary NLTK data if not already downloaded
nltk_packages = ['punkt', 'stopwords', 'wordnet']

for pkg in nltk_packages:
    try:
        nltk.data.find(f'tokenizers/{pkg}' if pkg == 'punkt' else f'corpora/{pkg}')
    except LookupError:
        nltk.download(pkg)




if __name__ == "__main__":
    root = tk.Tk()
    app = RecommenderGUI(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
    