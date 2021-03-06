import pickle
import os
from sklearn import model_selection
import joblib
import nltk
import re, string
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import classify
from nltk import NaiveBayesClassifier


#downloading the dataset
from nltk.corpus import twitter_samples
#twitter_samples.fileids()

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

#import os
#from sklearn import model_selection
#import joblib
#download important modules for pre-processing of data
#import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

#Data Pre-processing
#from nltk.tag import pos_tag
#from nltk.stem.wordnet import WordNetLemmatizer

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

#import re, string

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

nltk.download('stopwords')

#removing stopwords

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

#print("\n This is how the first tweet looks after noise removal: \n",remove_noise(tweet_tokens[0], stop_words))

positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


# collecting the cleaned tokens together

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

all_pos_words = get_all_words(positive_cleaned_tokens_list)

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)


import random

positive_dataset = [(tweet_dict, "Positive")
                     for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                     for tweet_dict in negative_tokens_for_model]

# merging the two files into a larger miscellaneously labelled dataset
dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

# splitting the data ito the 70:30 ratio =>training : testing

train_data = dataset[:7000]
test_data = dataset[7000:]



#from nltk import classify
#from nltk import NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(train_data)

#print("Accuracy is:", classify.accuracy(classifier, test_data))

from nltk.tokenize import word_tokenize
    
input_text= "I am happy"
input_text = remove_noise(word_tokenize(input_text))
input_token = dict([token, True] for token in input_text)

#print("\n\tText : ", input_token)

print("\n\n\tSentiment: ", classifier.classify(input_token))

#import pickle 
pickle.dump(classifier, open('model.pickle', 'wb'))