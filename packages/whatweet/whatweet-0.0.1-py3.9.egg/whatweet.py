from pytwitterscraper import TwitterScraper
import re
import sys
import MeCab
import matplotlib.pyplot as plt
import csv
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk

class main():
    def main(self,username, days, language):
        username = str(username)
        #print(username)
        days = int(days)
        tw = TwitterScraper()
        profile = tw.get_profile(name=username)

        tweets = tw.get_tweets(profile.id, count=days)
        tweet_list = []
        for tweet in tweets.contents:
            tmp = tweet['text']
            # Preprocessing
            tmp = tmp.strip('RT')
            tmp = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', tmp)
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
            tmp = tmp.translate(non_bmp_map)
            tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', tmp)
            tmp = re.sub(r'\d+', '0', tmp)
            tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', tmp)
            tmp = re.sub(u'[■-♯]', ' ', tmp)
            #print(tmp)
            tweet_list.append(tmp)
        #print(tweet_list)
        fname = 'tweet_text'

        with open(fname, 'w',encoding='utf-8') as f:
            f.writelines(tweet_list)
        if language == 'Japanese':

            mecab = MeCab.Tagger('-Ochasen')
            words=[]
            with open(fname, 'r',encoding='utf-8') as f:
                reader = f.readline()
                while reader:
                    node = mecab.parseToNode(reader)
                    while node:
                        word_type = node.feature.split(',')[0]
                        if word_type in ['形名詞', '動詞','名詞','副詞']:
                            words.append(node.surface)
                        node = node.next       
                    reader = f.readline()

            text_tweet = ' '.join(words)
            fpath = "/Library/Fonts/ヒラギノ明朝 ProN.ttc"
            stop_words = ["私","わたし","僕","あなた","みんな","ただ","ほか","それ", "もの", "これ", "ところ","ため","うち","ここ","そう","どこ", "つもり", "いつ","あと","もん","はず","こと","そこ","あれ","なに","傍点","まま","事","人","方","何","時","する","なり","おる","いた","おる","ある","さん","いる","笑","一","二","三","四","五","六","七","八","九","十",'あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん']
            wordcloud = WordCloud(background_color = "black", font_path = fpath ,width = 800, height = 600, stopwords = stop_words).generate(text_tweet)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()

        else:
            text_tweet = open(fname, encoding='utf-8').read()
            nltk.download('stopwords')
            stop_words = stopwords.words('english')
            stop_words.extend(('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'))
            wordcloud = WordCloud(background_color = 'black', width = 800, height = 600).generate(text_tweet)
            plt.imshow(wordcloud)
            plt.axis('off')
            plt.show()
            
username= ''
days = 100
language = ''

if len(sys.argv) != 4:
    print('Please fill in the three arguments')
    sys.exit()
else:
    if int(sys.argv[2]) > 500:
        print('Please use smaller days')
        sys.exit()
    else:
        days = int(sys.argv[2])
        if str(sys.argv[3]) == 'Japanese' or str(sys.argv[3]) == 'English':
            country = str(sys.argv[3])
        else:
            print('Please correct language name')
            sys.exit()

m = main() 
m.main(username=sys.argv[1],days=sys.argv[2],language=sys.argv[3])