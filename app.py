from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, request, jsonify
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from textblob import TextBlob
from iso3166 import countries
from collections import deque
from random import randrange
from gtts import gTTS 

import nltk.sentiment.vader as Sentiment
import urllib.request
import requests
import random
import praw
import nltk
import os

# list facts, images, 

#------------------------------------------
User = ''
spell = SpellChecker()
analyser = SentimentIntensityAnalyzer()
reddit = praw.Reddit(user_agent='REDDIT_SCRAPE',client_id='0qN2W0aFaEKbfA', client_secret="YVVEJRUOHXffq0AOi4dDeJPMH6A",username='chinmayrane16', password='qwerty1234')
app = Flask(__name__)

#------------------------------------------

def create_mp3(reply, x):
    language = 'en'
    myobj = gTTS(text=reply, lang=language, slow=False) 
    myobj.save("C:\\Users\\Dell Pro\\Desktop\\BOT\\static\\img\\reply_" + str(x) + ".mp3")

#------------------------------------------

def print_sentiment_scores(sentence):
    snt = analyser.polarity_scores(sentence)
    return snt

#------------------------------------------

def get_cases(r):
    data = r.json()
    text = ''
    if r.status_code == 200:
        if User != "":
            text =  User + f', Covid-19 {data["country"]} Confirmed Cases : {data["cases"]}, Today Cases : {data["todayCases"]} , Deaths : {data["deaths"]}, Recovered : {data["recovered"]}'
        else:
            text = f'Covid-19 {data["country"]} Confirmed Cases : {data["cases"]}, Today Cases : {data["todayCases"]} , Deaths : {data["deaths"]}, Recovered : {data["recovered"]}' 
    else:
        if User != "":
            text = User +'I could not retrieve the results at this time, sorry.'
        else:
            text = 'I could not retrieve the results at this time, sorry.'
    return text

#------------------------------------------
globe_keys = ['whole world', 'whole', 'world', 'glode', 'earth']
globe_set = set(globe_keys)

def bot(incoming_msg):
    B = 'Please specify the country for Covid-19 updates.'
    h_set = set(incoming_msg.split(" "))
    print("----------------")
    tokenized = nltk.word_tokenize(incoming_msg)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')]
    print(nouns)
    if (globe_set & h_set):
        r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
        B = get_cases(r)
    else: 
        for country in countries:            
            if country.name.lower() in nouns:
                print(country.name.lower())
                vv = 'https://coronavirus-19-api.herokuapp.com/countries/' + str(country.name).lower()
                r = requests.get(vv)
                B = get_cases(r)
    return B

#------------------------------------------

def sentiment(query):    
    blob = TextBlob(query)
    compount2 = blob.sentiment.polarity
    return compount2

#------------------------------------------

def getJokes():    
    connection = requests.get('https://official-joke-api.appspot.com/random_joke')
    result = connection.json()	
    question = result["setup"]
    ans = 'The answer :'
    punchline = result["punchline"]
    return question, ans, punchline

#------------------------------------------

def getDomain(val):
    sub_reddit = []
    encoded_text = val.replace(" ", "%20")
    address = 'https://www.reddit.com/search/?q='+encoded_text
    connection = urllib.request.urlopen(address)
    data = str(connection.read()).split('<div class="')
    for line in data:
        if '_2torGbn_fNOMbGw3UAasPl' in line:
            y = str(line).replace('_2torGbn_fNOMbGw3UAasPl', '')
            xx = y.split('_3CUjJH8t2eFynKUAv1ER7C')
            if len(xx) == 1:
                cc = xx[0].replace('</div>', '').replace('">', '')
                ccc = cc.split('/')
                if ccc[0] == 'r':
                    sub_reddit.append(ccc[1])
    return sub_reddit

#------------------------------------------

def check_profanity(text_to_check):
    encoded_text = urllib.parse.quote(text_to_check, 'utf-8')
    address = "http://www.wdylike.appspot.com/?q="+encoded_text
    connection = urllib.request.urlopen(address)
    output = str(connection.read())
    if 'true' in output:  
        return True
    else:
        return False 

#------------------------------------------

def choose(comments_scores, comments_body, sentiments):
    max_index = sentiments.index(max(sentiments))
    val = str(comments_body[max_index])
    return val

#------------------------------------------

def spelling(val):
    list = val.split(" ")
    misspelled = spell.unknown(list)
    if len(misspelled) == 0:
        return False
    else:
        return True

#------------------------------------------

topics = ["insomia", "suicide", "depression", "diamentia", "adhd", "add", "stress", "borderline disorder", "anxiety", "eating disorder", "personality disorder", "bipolar disorder", "mood disorder", "post traumatic stress disorder", "substance related abuse"]
subreddits_ = ["insomia", "SuicideWatch", "Anxiety Help", "Anxiety Disorders", "ADHD", "ADD", "mentalhealth", "relationships", "Anxiety"]
subreddits = ["anxiety"]
subreddits_set = set(subreddits)

#------------------------------------------
def get_common(Title, Human, val):    
    list = []
    for t in Title:
        for h in Human:
            if h == t:
                list.append(h)

    if len(list)> val:
        return True
    else:
	    return False
#------------------------------------------

def ask_reddit(Human, domain):    
    comments_scores = []
    comments_body = []
    sentiments = []
    Human_list = Human.split(" ")
    Human_set = set(Human_list)
    
    if len(domain) == 0:
        if 'what is' in Human:
            domain.append('AskReddit')
        elif subreddits_set & Human_set:
            for h_v in Human_list:
                for s_v in subreddits:
                    if s_v == h_v:
                        domain.append(s_v)
    print(domain)
    val = 'nothing'
    for sub in domain:
        print(sub)
        for submission in reddit.subreddit(sub).search(Human):
            title_list = str(submission.title.lower()).split(" ")
            if get_common(title_list, Human_list, 2):
                comments = submission.comments        
                for comment in comments:
                    try:
                        bodyy = str(comment.body)
                        if (len(bodyy) < 500) and (bodyy != '[deleted]') and ('i am a bot' not in bodyy.lower()) and ('i\'m' not in bodyy.lower()) and ('i\'m' not in bodyy.lower()) and ('i am' not in bodyy.lower()) and ('reddit' not in bodyy.lower()) and ('my' not in bodyy.lower()) and ('me' not in bodyy.lower()):
                            
                            pf = check_profanity(bodyy)
                            if pf == False:
                                spel = spelling(bodyy)
                                if spel == False:
                                    compount2 = sentiment(bodyy)                    
                                    if (compount2 >= 0.1):#Positive replies only
                                        print("TITLE : ", submission.title.lower())
                                        print('Sentiment : ', compount2)
                                        comments_scores.append(int(comment.score))
                                        comments_body.append(bodyy)
                                        sentiments.append(compount2)
                                        print(bodyy)
                                        print("------------------------------------------------")
                    except AttributeError:
                        pass
    if len(comments_scores) > 0:
        val = choose(comments_scores, comments_body, sentiments)
    return val

#------------------------------------------

@app.route('/')
def index():
    print('Hellii there')
    return render_template('index.html')

#------------------------------------------


@app.route('/support_group/')
def support_group():
    # show the form, it wasn't submitted
    return render_template('support_group.html')

#------------------------------------------

@app.route('/contact/')
def contact():
    # show the form, it wasn't submitted
    return render_template('contact.html')

#------------------------------------------
'''
def facts():
    ans = []
    ans.append('1: Clean your hands often. Use soap and water, or an alcohol-based hand rub.')
    ans.append('2: Maintain a safe distance from anyone who is coughing or sneezing.')
    ans.append('3: Don’t touch your eyes, nose or mouth.')
    ans.append('4: Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.')
    ans.append('5: Stay home if you feel unwell.')
    ans.append('6: If you have a fever, a cough, and difficulty breathing, seek medical attention. Call in advance.')
    ans.append('7: Follow the directions of your local health authority.')
    return ans
 
#------------------------------------------

def symptoms():
    return 'Covid 19 common-symptoms are : fever, tiredness, dry cough. Additional Symptoms are : aches and pains, nasal congestion, runny nose, sore throat, diarrhoea'
#------------------------------------------
'''
#------------------------------------------

covid_list = ['cases in', 'corona', 'coronavirus', 'covid', 'covid-19', 'covid19',  '2019-ncov', 'sars-coronavirus 2', 'sars-cov-2', '2019 novel coronavirus']
greetings = ["who are you?", "hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"]
native_greetings = ['ongiini', 'ongapi', 'omwalalaponawa', 'moro', 'matisa', 'morokeni', 'mire', 'hoe gaan dit', 'mwavuka']
native_replies = ['onawa', 'onawa', 'onda lalapo nawa', 'emoro', 'nxaire', 'morokeni', 'nxasmamire', 'dit gaan goed met my', 'hande']
name_statements = ['my', 'name', 'is', 'friends', 'call', 'me']

Choices = ['What is your name?', 'Do you want to hear a joke?']
Trigger = []

@app.route('/pass_val/',methods=['POST'])
def pass_val():
    H1 = request.get_json()
    Original = str(H1['human'])
    H = Original.lower()
    profanity = check_profanity(H)
    x = randrange(100000)
    Reponses = []
    print(H)

    if profanity == True:
        A = "I am a family friendly chatbot"
        B = "Please keep your language clean"
        Reponses.append(A)
        Reponses.append(B)
        Full = A + ' ' + B
        create_mp3(Full, x)
        return jsonify({'reply':Reponses, 'play':x, 'sentiment':-3})
    elif profanity == False:        
        if any(w in H for w in covid_list):
            A = bot(H)
            B = 'Covid'#facts()#C = 'Covid Symptoms'#symptoms()
            Reponses.append(A)
            Reponses.append(B)
            Full = A + ' ' + B
            create_mp3(Full, x)
            return jsonify({'reply':Reponses, 'play':x})
        elif (H in greetings):                 
            A = 'Hello 🙋🏽‍'
            B = 'I am is Counselling Artificial Intelligence chatting robot developed by Fideria Ndapopile and Norah Mamane please ask me anything that is troubling you.' 
            C = random.choice(Choices)
            Reponses.append(A)
            Reponses.append(B)
            Reponses.append(C)
            Full = 'Hello, I am a Counselling Artificial Intelligence chatting robot developed by Fideria Ndapopile and Norah Mamane please ask me anything that is troubling you. ' + C
            create_mp3(Full, x)
            return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
        elif (H in native_greetings):
            A = ''
            for native in native_greetings:
                if native == H:
                    native_index = native_greetings.index(native)
                    A = native_replies[native_index]
            Reponses.append(A)
            create_mp3(A, x)
            return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
        elif get_common(name_statements, H.split(' '), 1):               
            tokenized = nltk.word_tokenize(Original)
            nouns = nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos == 'NNP')]#cause lowercase
            print('----------> ',nouns)
            if len(nouns) == 1:
                User = nouns[0].title()
                A = 'Nice to meet you ' + User
                Reponses.append(A)
                create_mp3(A, x)
                return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
            else:
                User = nouns.pop().title()
                A = 'Nice to meet you ' + User
                Reponses.append(A)
                create_mp3(A, x)
                return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
        elif ('yes' == H):
            A, B, C = getJokes()
            Reponses.append(A)
            Reponses.append(B)
            Reponses.append(C)
            Full = A + ' ' + B + ' ' + C
            create_mp3(Full, x)
            return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
        elif ('no' == H):
            A = ""
            if User != "":
                A = User + ', Feel free to ask me anything'
            else:
                A = 'Feel free to ask me anything'
            B = 'Especially on Mental Health Issues'
            C = 'And I will do my best to respond'
            Reponses.append(A)
            Reponses.append(B)
            Reponses.append(C)
            Full = A + ' ' + B + ' ' + C
            create_mp3(Full, x)
            return jsonify({'reply':Reponses, 'play':x, 'sentiment':3})
        else:
            compount2 = sentiment(H)
            sub_reddit = getDomain(H)
            A = ask_reddit(H, sub_reddit)
            Reponses.append(A)
            create_mp3(A, x)
            return jsonify({'reply':Reponses, 'play':x, 'sentiment':compount2})
    else:
        A = "An error occurred!"
        Reponses.append(A)
        create_mp3(A, x)
        return jsonify({'reply':Reponses, 'play':x, 'sentiment':-3})

#--------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
    app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access
    #app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access

#--------------------------------------------
