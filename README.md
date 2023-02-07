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

### 🧶 Topic Modelling using BERT
We use BERTopic to perform topic modelling on the document. The pipeline used by BERTopic consists of: 
1. Sentence embeddings using a sentence transformer such as SBERT.
2. Dimensionality reduction using MAP.
3. Clustering using HDBSCAN
4. Tokenising within topics, and using tokenised keywords to make topic representations.

When the function is called, we print a hierarchial representation of the different topics, and return a dataframe that has the the topic IDs (-1 is to be ignored), frequency and representatitive words for the topic.

```python
topic_model = article.get_topics()
```
Printed topic hierarchy:
```
├─and_earthquake_rescue_in_turkeysyria
│    ├─■──and_feb_2023_efforts_by ── Topic: 3
│    └─earthquake_turkeysyria_personnel_search_in
│         ├─earthquake_to_toll_death_turkey
│         │    ├─■──earthquake_toll_death_syria_to ── Topic: 9
│         │    └─■──deployed_24400_area_more_than ── Topic: 10
│         └─■──building_during_iskenderun_hatay_operation ── Topic: 7
└─the_of_said_in_to
     ├─the_of_said_in_as
     │    ├─the_in_city_as_of
     │    │    ├─■──from_the_thick_black_burning ── Topic: 8
     │    │    └─in_city_the_as_of
     │    │         ├─■──sites_heritage_damage_unesco_world ── Topic: 6
     │    │         └─■──in_hotel_being_students_city ── Topic: 0
     │    └─had_said_disaster_management_people
     │         ├─■──people_million_said_with_quake ── Topic: 2
     │         └─■──had_11342_5775_reports_of ── Topic: 4
     └─aid_the_control_four_police
          ├─■──aid_is_syrian_government_control ── Topic: 1
          └─■──police_posts_provocative_four_accounts ── Topic: 5
```
Topic Model:
```
Topic	Count	Name
	0	30	0_in_hotel_being_students
	1	30	1_aid_is_syrian_government
	2	30	2_people_million_said_with
	3	21	3_and_feb_2023_efforts
	4	21	4_had_11342_5775_reports
	5	20	5_police_posts_provocative_four
	6	20	6_sites_heritage_damage_unesco
	7	20	7_building_during_iskenderun_hatay
	8	20	8_from_the_thick_black
	9	14	9_earthquake_toll_death_syria
 10	12	10_deployed_24400_area_more
```
### 🌐 Mining additional data 
#### 🤹 Similar Articles [1]
We extract keywords and perform web searches to find similar articles. 
```python
article.get_similar_articles()
```
Truncated output:
```
https://serpapi.com/search
[{'url': 'https://www.wsj.com/story/turkey-and-syria-earthquakes-race-is-on-to-rescue-people-from-the-rubble-7fdc009d',
  'title': 'Turkey and Syria Earthquakes in Photos: Race Is on to ...',
  'snippet': 'Turkey and Syria Earthquakes in Photos: Race Is on to Rescue People From the Rubble. Thousands of people are confirmed dead so far as a ...',
  'snippet_highlighted_words': ['Turkey', 'Syria']},
 {'url': 'http://www.erdemsahin.net/?page_id=403',
  'title': 'Syrian Conflict and Refugee Crisis - Erdem Şahin',
  'snippet': 'Turkish-backed Syrian fighters wave as they are on the way to Northern Syria for. An explosion after an apparent US-led coalition airstrike on Kobane, Syria, as.',
  'snippet_highlighted_words': ['Turkish', 'Syrian', 'Syria', 'Syria']},
 .
 .
 .]
```

### 🪄 State of the Art NLP: Prompting GPT3 [2]

#### 🙋‍♀️ Ask Questions using GPT3
This function will allow you to ask a question related to the article, and GPT3 returns an answer that is supposed to be related to the article. In case an irrelevant question is asked, the model answers by indicating the question is not relevant.
```python
>>> article.gpt_ask_question("What is Fuat Oktay? What did he say?")
>>> 'Fuat Oktay is Turkey's vice-president. He said that 3,419 people had been killed in the quake, with another 20,534 injured.'
```

```python
>>> article.gpt_ask_question("Who are the most affected by the earthquake?")
>>> 'The World Health Organization estimates that around 23 million people, including 1.4 million children, are likely to be affected by the earthquake.'
```

```python
>>>article.gpt_ask_question("Who is the fisheries minister of India ?")
>>>'Irrelevant to the article.'
```

#### 🧃 Summarise using GPT3
The extractive summarisation technique defined above is too simplistic, prone to noise inclusion and is not very effective when understanding is needed. We can make an abstractive summary using GPT3.
```python
article.gpt_summary()
```
Output:
```
'On Tuesday morning, the death toll from the 7.8-magnitude earthquake that struck southern Turkey and northern Syria rose to 5,021. Over 20,000 people have been injured and an estimated 23 million people are affected by the quake. The World Health Organization warned the number of fatalities could exceed 20,000. Turkey has deployed over 24,400 search and rescue personnel and 3,400 people have taken shelter in trains used as emergency accommodation. Syria has been accused of playing politics with aid.'
```

#### 👉 Generate Pointers using GPT3
This function returns a list of pointers which are crisp statements based on the article.
```python
points = article.gpt_pointers()
print(*points, sep="\n")
```
Output:
```
- 7.8-magnitude earthquake hit southern Turkey and northern Syria on Monday
- Death toll estimated to exceed 20,000
- Nearly 23 million people, including 1.4 million children, affected by the quake
- Turkey: 3,419 killed, 20,534 injured and 11,342 reports of collapsed buildings
- Syria: 1,602 killed
- Turkey deployed 24,400 search and rescue personnel to the quake area
- Syria accused of playing politics with aid
```







[1] You will need to configure [SERPApi](https://serpapi.com/) keys. It might demand a paid subscription.

[2] You will need to configure [OpenAI](https://openai.com/) keys . It might demand a paid subscription.









