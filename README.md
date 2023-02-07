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
Turkey and Syria earthquake: what we know so far on day two](https://www.theguardian.com/world/2023/feb/07/earthquakes-in-turkey-and-syria-what-we-know-so-far) published in [The Guarian](https://www.theguardian.com/international).
!(https://cdn.discordapp.com/attachments/891317274936483871/1072575484690432094/image.png)[Snapchot of the article]

We use different heuristics to automatically find the article title and article text. You can view the article by simply printing the article object.
```python
print(art)
```
#### Truncated output:
```
Title: Turkey and Syria earthquake: what we know so far on day two 
Article:Turkey-Syria earthquake 2023Turkey and Syria earthquake: what we know so far on day twoUN says death toll could rise to more than 20,000 from one of the most powerful earthquakes to hit the region in at least a century

Turkey and Syria earthquake live updates: follow the latest news
Emergency personnel during a search and rescue operation at the site of a building that collapsed  in Iskenderun, Hatay, in the Turkey-Syria earthquake. Photograph: Erdem Şahin/EPAEmergency personnel during a search and rescue operation at the site of a building that collapsed  in Iskenderun, Hatay, in the Turkey-Syria earthquake. Photograph: Erdem Şahin/EPAHelen Sullivan and Martin BelamTue 7 Feb 2023 00.47 GMTLast modified on Tue 7 Feb 2023 14.27 GMT
Aftershocks, freezing temperatures and damaged roads are hampering efforts to reach and rescue those affected by Monday’s earthquake in southern Turkey and northern Syria, which has killed more than 5,000 people and destroyed ...
```

### Classic NLP Techniques


