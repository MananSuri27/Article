# Article 🗞️
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
