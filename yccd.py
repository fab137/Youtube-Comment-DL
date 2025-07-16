from youtube_comment_downloader import YoutubeCommentDownloader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import DBSCAN
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog
import networkx as nx
import re
import time

# ---------------------------
# 1. Setup & Stopwords
# ---------------------------
nltk.download('stopwords')
stop_words_it = stopwords.words('italian')

# ---------------------------
# 2. Download Comments
# ---------------------------
video_url = input("📺 Enter the full YouTube video URL: ").strip()

# Extract video ID
import re
match = re.search(r"v=([a-zA-Z0-9_-]{11})", video_url)
if not match:
    print("❌ Invalid YouTube URL. Must contain '?v=VIDEO_ID'")
    exit()

video_id = match.group(1)

downloader = YoutubeCommentDownloader()

print("🔽 Downloading comments...")
try:
    comments = downloader.get_comments_from_url(
        f"https://www.youtube.com/watch?v={video_id}", sort_by=0
    )
    comments = list(comments)  # Convert generator to list
except Exception as e:
    print("❌ Error downloading comments:", e)
    comments = []

# Double check structure
if comments:
    print("🔍 Example comment object:")
    print(comments[0])

# ---------------------------
# 3. Parse into DataFrame
# ---------------------------
data = []
for comment in comments:
    text = comment["text"].strip()
    if len(text) > 10:
        author_name = comment.get("author", "Unknown")
        author_id = comment.get("author_id")
        if author_id:
            channel_url = f"https://www.youtube.com/channel/{author_id}"
        else:
            search_name = author_name.replace(" ", "+")
            channel_url = f"https://www.youtube.com/results?search_query={search_name}"

        data.append({
            "user": author_name,
            "channel_url": channel_url,
            "text": text,
            "time": comment.get("time", ""),
            "votes": comment.get("votes", 0)
        })

df = pd.DataFrame(data)
df.drop_duplicates(subset="text", inplace=True)
df = df[["user", "channel_url", "text", "time", "votes"]]

# ---------------------------
# 4. TF-IDF + SVD + DBSCAN
# ---------------------------
print("🔤 Vectorizing text...")
vectorizer = TfidfVectorizer(stop_words=stop_words_it, lowercase=True)
X = vectorizer.fit_transform(df["text"])

n_features = X.shape[1]
n_components = min(100, n_features - 1)
print(f"⚙️ Reducing dimensions to {n_components} components...")
svd = TruncatedSVD(n_components=n_components)
X_reduced = svd.fit_transform(X)

start = time.time()
print("🧠 Clustering with DBSCAN...")
clustering = DBSCAN(eps=0.6, min_samples=2, metric='euclidean').fit(X_reduced)
print(f"✅ Clustering complete in {time.time() - start:.2f} seconds")
df["cluster"] = clustering.labels_

# ---------------------------
# 5. Save CSV (User Prompt)
# ---------------------------
root = tk.Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv")],
    title="💾 Save clustered comment data as..."
)

if file_path:
    df.to_csv(file_path, index=False)
    print(f"✅ CSV saved to: {file_path}")
else:
    print("❌ Save cancelled.")

# ---------------------------
# 6. Export Graph for Gephi
# ---------------------------
print("🌐 Exporting coordination graph for Gephi...")

G = nx.Graph()

# Create nodes
for idx, row in df[df["cluster"] != -1].iterrows():
    G.add_node(row["user"], label=row["user"], cluster=row["cluster"])

# Add edges between users in the same cluster
clusters = df[df["cluster"] != -1].groupby("cluster")
for cluster_id, group in clusters:
    users = group["user"].tolist()
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            if users[i] != users[j]:
                G.add_edge(users[i], users[j], cluster=cluster_id)

# Save graph as GEXF
gexf_path = re.sub(r"\.csv$", ".gexf", file_path)
nx.write_gexf(G, gexf_path)
print(f"🗺️ Graph saved to: {gexf_path}")

# ---------------------------
# 7. Plot (Optional)
# ---------------------------
print("📊 Plotting cluster distribution...")
cluster_counts = df["cluster"].value_counts()
cluster_counts.sort_index(inplace=True)
cluster_counts.plot(kind='bar', title="Numero di commenti per cluster")

for i, count in enumerate(cluster_counts):
    plt.text(i, count + 0.5, str(int(count)), ha='center', va='bottom', fontsize=8)

plt.xlabel("ID del cluster")
plt.ylabel("Conteggio commenti")
plt.tight_layout()
plt.show()
