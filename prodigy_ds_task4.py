# -*- coding: utf-8 -*-
"""prodigy-ds-task4

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10R6MYJcWiQDrV99JHw3D5nbk0U1nVrKj
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from google.colab import files
uploaded = files.upload()

data = pd.read_csv("twitter_training.csv")
data

data.head()

data.info()

positive_words = ["happy", "excited", "love"]
negative_words = ["sad", "angry", "hate"]

def sentiment_score(text):
  score = 0
  for word in text.split():
    if word.lower() in positive_words:
      score += 1
    elif word.lower() in negative_words:
      score -= 1
  return score

print(data.columns)

# Apply sentiment score using modified function
data["sentiment_score"] = data["Borderlands"].apply(sentiment_score)

sentiment_counts = data["sentiment_score"].value_counts()

#bar charts
sentiment_counts.plot(kind="bar")
plt.xlabel("Sentiment Score")
plt.ylabel("Count")
plt.title("Sentiment Distribution of Tweets")
plt.show()

def clean_text(text):
  import string
  text = text.translate(str.maketrans('', '', string.punctuation))
  return text.lower()

# Function to join cleaned texts for word cloud
def get_text_for_wordcloud(data_subset):
  cleaned_text = " ".join([clean_text(text) for text in data_subset["Borderlands"]])
  return cleaned_text if cleaned_text else ""

# Generate text for each sentiment category
positive_text = get_text_for_wordcloud(data[data["sentiment_score"] > 0])
negative_text = get_text_for_wordcloud(data[data["sentiment_score"] < 0])
neutral_text = get_text_for_wordcloud(data[data["sentiment_score"] == 0])

try:
  positive_cloud = WordCloud(width=800, height=600).generate(positive_text)
except ValueError:
  print("Positive sentiment has no words to visualize.")
  positive_cloud = None  # Or set positive_cloud to an empty image

try:
  negative_cloud = WordCloud(width=800, height=600).generate(negative_text)
except ValueError:
  print("Negative sentiment has no words to visualize.")
  negative_cloud = None

try:
  neutral_cloud = WordCloud(width=800, height=600).generate(neutral_text)
except ValueError:
  print("Neutral sentiment has no words to visualize.")
  neutral_cloud = None

plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title("Positive Words")
if positive_cloud is not None:
    plt.imshow(positive_cloud)
    plt.axis("off")
else:
    plt.text(0.5, 0.5, "No positive words to display", ha='center', va='center')
plt.show()

plt.subplot(1, 3, 2)
plt.title("Negative Words")
if negative_cloud is not None:
    plt.imshow(negative_cloud)
    plt.axis("off")
else:
    plt.text(0.5, 0.5, "No negative words to display", ha='center', va='center')
plt.show()

plt.subplot(1, 2, 2)
plt.title("Neutral Words")
plt.imshow(neutral_cloud)
plt.axis("off")
plt.show()