# 📚 Wikipedia Article Recommender

This is a fun and functional little project that recommends Wikipedia articles based on the stuff you've already read. It runs in a pretty Tkinter GUI, has interactive options for tweaking how text is processed, and shows your results with a nice plot. It's powered by (classical) NLP magic (well, TF-IDF mostly) and looks way nicer than your average Python app, thanks to ttkbootstrap.

Whether you're into linguistics, data science, or just constantly end up down Wikipedia rabbit holes, this tool is for you.

---

## 💡 Why Use This?

- Tired of manually searching for interesting Wikipedia reads? Let this do it for you - get **personalized article suggestions**.
- Get recommendations tailored to your reading history using TF-IDF and cosine similarity.
- Tweak the text preprocessing pipeline however you like:
    - Choose between different tokenizers (e.g. word_tokenize, wordpunct_tokenize).
    - Use one of the built-in stemmers (Porter, Lancaster, or none).
    - Toggle lemmatization if you prefer smarter word reduction.
- Built-in visualization shows how similar the articles are.
- Enjoy a clean, modern **Tkinter GUI** styled with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/).

---

## 🚀 How to Use

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/wikipedia-recommender.git
cd wikipedia-recommender
```
## 📂 Folder Structure:
```
.
├── gui.py
├── main.py 
├── recommender/
│   ├── crawler.py
│   ├── expansion.py    
│   ├── recommender.py
│   ├── preprocessing.py
│   ├── vectorizer.py
│   └── utils.py
├── data/
│   ├── articles.csv   
│   └── processedArticles.csv  # Input dataset
└── requirements.txt
```


### 2. Install requirements
```bash
pip install -r requirements.txt
```
### 3. Run the app
```bash
python main.py
```

## Contact
Feel free to reach out if you have ideas, issues, or just want to geek out over Wikipedia 🤓🤓

📧 mmartyna.stasiak@gmail.com

## License
This project is licensed under the MIT License.