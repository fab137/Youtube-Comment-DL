# YouTube Comment Coordination Detector (🇮🇹 Italian Language)

This Python script analyzes comments from **any YouTube video** to detect potential coordination, propaganda patterns, or bot activity. It supports **Italian-language** content and is ideal for digital investigations and OSINT research.

---

## 🚀 Features

- ✅ Prompt-based input of YouTube video URL
- ✅ Clusters comments by semantic similarity (using TF-IDF + SVD + DBSCAN)
- ✅ Flags coordinated clusters of commenters
- ✅ Includes commenter usernames and profile URLs
- ✅ Exports .gexf graph for Gephi network visualization
- ✅ Bar chart visualization of clusters

---

## 📦 Dependencies

Install required packages:

- pip install youtube-comment-downloader
- pip install pandas
- pip install matplotlib
- pip install scikit-learn
- pip install nltk
- pip install networkx
- pip install pillow
- pip install reportlab

---

Also download Italian stopwords for NLP:

- python youtube-comment-dl_dynamic_url.py

---

## 🧪 How to Use

1. Run the script with: python youtube-comment-dl_dynamic_url.py
2. Paste the full YouTube video URL (e.g. https://www.youtube.com/watch?v=XXXXXX)
3. Choose a location to save the results when prompted.

---

## 📁 Outputs

- .csv file with clustered comments, channel URLs, and votes
- .gexf file for graph analysis in Gephi
- Optional .png or .pdf for visual reports (future)

---

## 📊 Example Applications

- Detecting coordinated political commenting
- Investigating state-sponsored propaganda
- Mapping ideological influence operations
- Researching online public opinion manipulation

---

## 🛡️ License

MIT License — free to use, modify, and share for research or educational purposes.

---

## 🙌 Credits

Built using:

- youtube-comment-downloader (https://github.com/egbertbouman/youtube-comment-downloader)
- scikit-learn, nltk, networkx, matplotlib

Feel free to contribute or fork!
