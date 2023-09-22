import requests
from bs4 import BeautifulSoup, NavigableString
import re
from urllib.parse import urlparse

class Article:
  '''
  Class to parse news articles.
  '''
  def __init__(self, url):
    '''
    Function that initialises the Article object with the url.

    url: full url of the news article to be analysed
    '''
    self.url = url
    self.soup = self.parse(url)
    self.title = self.get_title()
    self.text = self.get_text()
    self.date = self.get_date()
    self.models = ["dt", "nb", "lr", "svm"]

  def __str__(self):
    '''
    Function that generates a formatted string representing the article.
    '''
    return f"Title: {self.title} \n Article:{self.text}"


  def parse(self, url, engine="html.parser"):
    '''
    Function that generates a parser, for parsing the DOM elements that constitute the webpage.

    url: full url of the news article to be analysed
    engine: parser to use to parse the html document. 
      Options:["html.parser","lxml", "html5.lib"] 
      Recommended: "html.parser"

    Returns:
    A beautiful soup parser of the HTML document.
    '''
    # GET the webpage from the URL
    res = requests.get(url)

    # Parse HTML document using beautiful soup.
    soup = BeautifulSoup(res.content, engine)

    # Remove script tags from the HTML
    [s.decompose() for s in soup('script')]


    return soup


  def get_text(self):
    '''
    Function to extract the texts from an article. 
    This includes using various heuristics to find the elements which contain the article body.

    Returns:
    A string which is the textual content of the article.
    '''

    # List to store individual text snippets from DOM nodes.
    texts = []


    #  regex pattern to match with case insensitive strings containing article followed by body
    pattern1 = re.compile(r'article.*body', re.IGNORECASE)

    #  regex pattern to match with case insensitive strings containing article 
    pattern2 = re.compile(r'article*', re.IGNORECASE)

    # Utility function to match attribute value with a given regex pattern, will be used in text extraction heuristic
    def attrs_match(attrs,pattern):
      for key, value in attrs.items():
          if pattern.search(value):
              return True
      return False

    # Utility function to recursively get texts from DOM nodes and their children.
    def get_text_from_element(element, texts=[]):
      try:
        texts.append(element.text)
      except:
        "no text"
      if not isinstance(element, NavigableString):
        for child in element.children:
            texts = get_text_from_element(child, texts)
      return texts

    # node represents list of candidate article nodes

    node = None
    #  Heuristic:
    #  1. Priority 1: article Tag
    #  2. Priority 2: itemProp="articleBody"
    #  3. Priority 3: 3a: class name contains article and body (pattern1)
    #                 3b: class name contains article (pattern2)
    #  4. Priority 4: 4a: has an attribute containing article and body (pattern1)
    #                 4b: has an attribute containing article (pattern2)
    
    if articles := self.soup.find_all('article'):
      node = articles
    elif itemProps := self.soup.find_all(attrs={"itemprop":"articleBody"}) :
      node = itemProps
    elif elements_ab := self.soup.find_all(class_=pattern1):
      node = elements_ab
    elif elements_a := self.soup.find_all(class_=pattern2):
      node = elements_a
    elif elements_ab_alt := self.soup.find_all(attrs= lambda x: attrs_match(x,pattern1)):
      node = elements_ab_alt 
    else:
      elements_a_alt = self.soup.find_all(attrs= lambda x: attrs_match(x,pattern2))
      node = elements_a_alt
      
    # iterate through nodes if node!=None, and extract text recursively
    if node:

      for n in node:
        get_text_from_element(n,texts)
      
    else:
      texts.append("Article could not be scraped.")

    # join texts with a " " in between them

    return (" ").join(texts).strip()
      

  def get_title(self):
    '''
    Function to get the title from an article.
    A heuristic inspired by newspaper3k is used here, to find the title of the article

    Returns:
    A string which is the title of the article.
    '''

    # get title tag options
    title_tag = self.soup.find('title')
    h1_tags = self.soup.find_all('h1')
    h1_tags.sort(reverse=True, key= lambda x: len(x.text) if x.text else 0)
    meta_tag = self.soup.find('meta',  property="og:title")

    # get text candidates


    meta_title_text = meta_tag["content"] if meta_tag and meta_tag["content"] else ''
    title_title_text = title_tag.text if title_tag.text else ''
    h1_title_text = h1_tags[0].text if h1_tags and h1_tags[0].text else ''

    # default title set to title tag
    title = title_title_text

    # Heuristic:
    # 1. Priority 1: If title tag's text is equal to the first h1's text, then it is the title
    # 2. Priority 2: If h1's title is equal to meta derived title, then it is the title.
    # 3. Priority 3: If meta derived title is the beginning of the title tag's title, then meta derived title is the title

    if title_title_text==h1_title_text:
      title = title_title_text
    elif h1_title_text == meta_title_text:
      title = h1_title_text
    elif title_title_text.startswith(meta_title_text):
      title = meta_title_text

    # Often, title exists in the form of title | publisher, therefore we split the derived title, and take the longer stringas the title

    title_splits = title.split('|')
    title_splits.sort(key=lambda x: len(x), reverse=True)
    title_final = title_splits[0]

    return title_final
  def get_date(self):

    '''
    Function to get the publishing date of the article.
    Inspired by newspaper3k, it iterates over a list of possible tags and returns the first matched tag it finds.

    Returns:
    Date string or None depending on if date is found.
    '''


    PUBLISH_DATE_TAGS = [
            {'attribute': 'property', 'value': 'rnews:datePublished',
             'content': 'content'},
            {'attribute': 'property', 'value': 'article:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'OriginalPublicationDate',
             'content': 'content'},
            {'attribute': 'itemprop', 'value': 'datePublished',
             'content': 'datetime'},
            {'attribute': 'property', 'value': 'og:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'article_date_original',
             'content': 'content'},
            {'attribute': 'name', 'value': 'publication_date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'sailthru.date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'PublishDate',
             'content': 'content'},
            {'attribute': 'pubdate', 'value': 'pubdate',
             'content': 'datetime'},
            {'attribute': 'name', 'value': 'publish_date',
             'content': 'content'},
        ]

    for known_meta_tag in PUBLISH_DATE_TAGS:
        meta_tags = self.soup.find_all( attrs={known_meta_tag['attribute']:known_meta_tag['value']})
        if meta_tags:
            date_str = meta_tags[0].get(known_meta_tag['content'])
            if date_str:
              return date_str
    return None
            
