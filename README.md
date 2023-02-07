# 🗞️ Article 
Tool to parse + perform NLP on web articles.

## 🔩 Usage 
Follow the following steps to set up the module:
```bash
git clone https://github.com/MananSuri27/Article.git
cd Article
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm 
```
Now, to initialise and work with Article,
```python
from article import Article

art = Article("ARTICLE_URL")
```

## 🧰 Toolkit

Lets explore the different functions available by performing analysis on an article from the day this document was made, [
Turkey and Syria earthquake: what we know so far on day two](https://www.theguardian.com/world/2023/feb/07/earthquakes-in-turkey-and-syria-what-we-know-so-far) published in [The Guardian](https://www.theguardian.com/international).
![Snapchot of the article](https://cdn.discordapp.com/attachments/891317274936483871/1072575484690432094/image.png)

We use different heuristics to automatically find the article title and article text. You can view the article by simply printing the article object.
```python
print(art)
```
Truncated output:
```
Title: Turkey and Syria earthquake: what we know so far on day two 
Article:Turkey-Syria earthquake 2023Turkey and Syria earthquake: what we know so far on day twoUN says death toll could rise to more than 20,000 from one of the most powerful earthquakes to hit the region in at least a century

Turkey and Syria earthquake live updates: follow the latest news
Emergency personnel during a search and rescue operation at the site of a building that collapsed  in Iskenderun, Hatay, in the Turkey-Syria earthquake. Photograph: Erdem Şahin/EPAEmergency personnel during a search and rescue operation at the site of a building that collapsed  in Iskenderun, Hatay, in the Turkey-Syria earthquake. Photograph: Erdem Şahin/EPAHelen Sullivan and Martin BelamTue 7 Feb 2023 00.47 GMTLast modified on Tue 7 Feb 2023 14.27 GMT
Aftershocks, freezing temperatures and damaged roads are hampering efforts to reach and rescue those affected by Monday’s earthquake in southern Turkey and northern Syria, which has killed more than 5,000 people and destroyed ...
```

### 🗣️ Classic NLP Techniques
#### 🔢 N-Grams
N-grams are continuous sequences of words or symbols or tokens in a document.  They give information about co-occurence of different words in the document. The n-gram function accepts an argument n to determine the value of n. It returns a sorted list of tuples and their frequencies.
```python
art.get_ngrams(n=3)
```
Truncated Output:
```
[(('personnel', 'search', 'rescue'), 24),
 (('search', 'rescue', 'operation'), 24),
 (('rescue', 'operation', 'site'), 24),
 (('operation', 'site', 'building'), 24),
 (('site', 'building', 'collapsed'), 24),
 (('building', 'collapsed', 'iskenderun'), 24),
 (('collapsed', 'iskenderun', ','), 24),
 .
 .
 . ]
```

#### 🌃 Named Entity Recognition
Named entities are pre defined categories such as person names, organisations, locations etc. We use the spaCy implementation of NER which uses multi layer CNNs. The function performs NER on the article title.
```python
article.get_ner()
```
Output:
```
[('Turkey', 'GPE'), ('Syria', 'GPE'), ('day two', 'DATE')]
```

#### 📝 Extractive Summarisation
Exctractive Summarisation picks the top p% of sentences in a document, weighted by similarity to other sentences. It's a compute efficient way of generating short summaries.
```python
article.get_summary()
```
Output:
```
'Adelheid Marschang, a WHO senior emergency officer, has said about 23 million people, including 1.4 million children, are likely to be affected by the quake. On Tuesday morning, Turkey’s vice-president, Fuat Oktay, said 3,419 people had been killed in the quake, with another 20,534 injured. The students, members of a volleyball team, were in the city to compete in a sports event when their eight-floor hotel collapsed. Turkey’s disaster management agency said it had 11,342 reports of collapsed buildings, of which 5,775 had been confirmed. The number was expected to rise with the arrival of additional people, the disaster management agency official Orhan Tatar said. The four individuals were held after officers found accounts that shared “provocative posts aiming to create fear and panic”, the police said. Photograph: Erdem Şahin/EPAEmergency personnel during a search and rescue operation at the site of a building that collapsed  in Iskenderun, Hatay, in the Turkey-Syria earthquake.'
```

#### 🔑 Keyword Extraction
Keyword extraction refers to the task of extracting important words from the document. We implement two popular algorithms, RAKE and YAKE.
```python
article.get_keywords("yake")
```
Truncated Output
```
[('Turkey Syria Syria', 0.0007545710012582912),
 ('Turkey Turkey Syria', 0.0008799549406467142),
 ('Syria', 0.0009543548862587613),
 ('Turkey', 0.0009992165376132955),
 ('Erdem Şahin', 0.0017732125672323214),
 .
 .
 . ]
```
```python
article.get_keywords("rake")
```
Truncated Output
```
[('television images showed thick black smoke rising', 49.0),
 ('television images showed thick black smoke rising', 49.0),
 .
 .
 . ]
```

#### ⛅️ Word Cloud
A word cloud is a graphical representation of word frequencies in a document.
```python
article.get_word_cloud()
```
Output:
![Word cloud](https://media.discordapp.net/attachments/891317274936483871/1072583370317504512/JqWILuA8kAAAAASUVORK5CYII.png)

### 🍊 Classification Algorithms
We build classification pipelines for text classification using scikit-learn modules. The text input is processed with a CountVectorizer, followed by a TfidfTransformer to build a bag-of-words representation for the test. This is done only to make the pipeline efficient to use in a production environment. Better algorithms such as finetuned transformers are better suited for performance metrics.

Classification Algorithms used: Naive Bayes, Decision tree, Logistic Regression, Support Vector Machine
Domains: [Clickbait identification](https://www.kaggle.com/datasets/amananandrai/clickbait-dataset), [Fake news identification](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

```python
>>> article.predict_fake_news("svm")
>>> 1
```
```python
>>> article.predict_clickbait("nb")
>>> 0
```
For implementation, refer to [these notebooks](https://github.com/MananSuri27/Article/tree/main/notebooks).









