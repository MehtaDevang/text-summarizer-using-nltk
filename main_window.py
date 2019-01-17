from tkinter import *
import bs4 as bs
import urllib.request
import re
import os
import nltk
import heapq


root = Tk()
# root.config(height = 480, width = 640)
root.title('Text Summarizer')

def summarize(obj, article_text):
    obj['text'] = "Generating Summary for you ..."

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentense_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}

    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1

            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] /= maximum_frequency

    sentence_scores = {}

    for sent in sentense_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]

                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)

    print("Working ...")
    # print(summary)
    obj['text'] = summary


frame = Frame(root)
frame.pack()
main_text = Label(frame, text="Exter Text to summarize")
# entry_main_text = Entry(frame, width=300, bd=2)
text = Text(root)
main_text.pack()
text.pack(pady=10)

# entry_main_text.pack(padx=20, pady=5)

frame2 = Frame(root)
frame2.pack()
summarized_label = Label(frame2, text="Summarized Text")
entry_summary = Label(frame2, text="", width=150, height=200, anchor=W, bd=2, justify=LEFT, relief=SUNKEN, wraplength=1000, padx=20)

summarize_button = Button(frame, text="Summarize",
                          command=lambda: summarize(entry_summary, text.get("1.0","end-1c")))
summarize_button.pack()

entry_summary.pack()

root.mainloop()