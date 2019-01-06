import bs4 as bs
import requests
import re
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec

web_data = requests.get(
    'https://en.wikipedia.org/wiki/Outline_of_industry').text

parsed_article = bs.BeautifulSoup(web_data, features="html5lib")

total_text = ""
# hard coding for now, will change later
link_list = ['Aerospace_maunfacturer', 'Agriculture', 'Fishing_industry', 'Wood_industry', 'Tobacco_industry',
             'Chemical_industry', 'Pharmaceutical_industry', 'Computer_industry', 'Software_industry',
             'Construction#Industry_characteristics', 'Arms_industry', 'Education','Energy_industry',
             'Electric_power_industry','Petroleum_industry','Show_business','Financial_services','Food_industry',
             'Insurance','Horticulture_industry','Healthcare_industry','Hospitality_industry',
             'Information_industry','Manufacturing', 'Automotive_industry','Electronics_industry',
             'Pulp_and_paper_industry','Steel#Steel_industry','Shipbuilding','Mass_media','Broadcasting',
             'Film_industry','Music_industry','News_media', 'Publishing', 'World_wide_web','Mining',
             'Telecommunications_industry', 'Internet','Transport','Water_industry']

link_list_reduce = ['Aerospace_maunfacturer', 'Computer_industry','Software_industry','Education' ,
'Electric_power_industry','Information_industry','Electronics_industry','World_wide_web','Internet']

def prepare_link(link):
    prepend = 'https://en.wikipedia.org/wiki/'
    return prepend+link

def is_valid_link(link):
    return re.match(r'<a href="/wiki', link)

def get_paragraphs(link):
    text= ''
    web_data = requests.get(link).text
    soup = bs.BeautifulSoup(web_data,'html5lib')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text+=p.text
    return text    


#GET ALL TEXT FROM EVERY PARAGRAPH OF LINK IN LINKLIST
def get_data(link_list):
    total_text= ''
    for link in link_list:
        good_link = prepare_link(link)
        p_text_data = get_paragraphs(good_link)
        total_text+=p_text_data
    return total_text

def clean_text(text):
    processed_article = text.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
    processed_article = re.sub(r'\s+', ' ', processed_article)

    # Preparing the dataset
    all_sentences = nltk.sent_tokenize(processed_article)

    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

    # Removing Stop Words
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
    return all_words

def make_model(word_list,default_word='computer'):
    word2vec = Word2Vec(word_list, min_count=2)
    #vocabulary = word2vec.wv.vocab
    #vector = word2vec.wv[default_word] 
    vector = word2vec.wv
    del(word2vec) #free ram????
    sim = vector.most_similar(default_word) #word2vec.wv.most_similar(default_word)
    print(sim)

#MAIN FUNCTION LMAO
def do_all(link_list, target_word):
    raw_words = get_data(link_list)
    final_word_list = clean_text(raw_words)
    make_model(final_word_list,target_word)

do_all(link_list_reduce, 'science')

# def prepare(tag):
#     print('lmao')
#     re.search(r'htref=\w{6,27}')


# def get_data(link):
#     print('about ot prepare link')
#     link = prepare_link(link)
#     print('link is now: ', link)
#     web_data = requests.get(link).text
#     parsed_article = bs.BeautifulSoup(web_data, feqtures='html5lib')
#     print(parsed_article.get_text)


# use regex to remove fucking everything that isn't the direct link
# then preprend wikipedia.com and boom we have an actual link
# {x, y} - Repeat at least x times but no more than y times.
#{6, 27}
#re.search(r'\d{9,10}', '0987654321').group()
# for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
# print link.get('href')

# for link in parsed_article.find_all('a', attrs={'href': re.compile("^https://en.wikipedia.org/")}):
#     print('Link is: \n', link)
#     a_tag = link.extract()
#     if (is_valid_link(str(a_tag))):
#         prepare(a_tag)
#         link_list.append(a_tag)
