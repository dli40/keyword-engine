import bs4 as bs
import requests
import re
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec


# NEW PLAN ----------------------------------------------
# take "important" words from class entered and look them up in wikipedia. And then hope???
# should work ok for common classes
# MAIN ISSUE:::: returning the right thing...mabe have a filter of words we want, and only chooose
# probably words from there to display. vocab generated is ok overall, but many are useless, can this be
# improved???
my_stop_words = ['intro', 'introduction', 'beginning', 'intermediate', 'advanced',
                 'AP', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# assuming the data is a single string, separtaed by whitespace
# regex or tokenize it into multiple strings of one word size
# UNLESS IT IS A COMMON FHRASE???????????


# hard coding for now, will change later
link_list = ['Engineering','Artificial_intelligence']


def prepare_link(link):
    prepend = 'https://en.wikipedia.org/wiki/'
    return prepend+link


def get_paragraphs(link):
    text = ''
    web_data = requests.get(link).text
    soup = bs.BeautifulSoup(web_data, 'html5lib')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text += p.text
    return text


# GET ALL TEXT FROM EVERY PARAGRAPH OF LINK IN LINKLIST
def get_data(link_list):
    total_text = ''
    for link in link_list:
        good_link = prepare_link(link)
        p_text_data = get_paragraphs(good_link)
        total_text += p_text_data
    return total_text


def clean_text(text):
    processed_article = text.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article)
    processed_article = re.sub(r'\s+', ' ', processed_article)

    # Preparing the dataset
    all_sentences = nltk.sent_tokenize(processed_article)

    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

    # Removing Stop Words
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i]
                        if w not in stopwords.words('english')]
    return all_words


def make_model(word_list, default_word='computer'):
    word2vec = Word2Vec(word_list, min_count=2)
    #vocabulary = word2vec.wv.vocab
    #vector = word2vec.wv[default_word]
    vector = word2vec.wv
    print('VECTOR IS --------------------------------------\n')
    print(vector['artificial'])
    del(word2vec)  # free ram????
    sim = ['empty boi']
    try:
        # word2vec.wv.most_similar(default_word)
        sim = vector.most_similar(default_word, topn=20)
    except KeyError as e:
        print('oof, there was a key error looking for the word: ', default_word)

    print(sim)

# MAIN FUNCTION LMAO


def do_all(link_list, target_word):
    raw_words = get_data(link_list)
    final_word_list = clean_text(raw_words)
    make_model(final_word_list, target_word)


do_all(link_list, 'engineering')
