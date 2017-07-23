import os
import requests
import operator
import re
import nltk
import hashlib,uuid
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet



application = Flask(__name__)
application.config.from_object("config.DevelopmentConfig")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


@application.route('/', methods=['GET', 'POST'])
def index():
	from models import Result
	errors = []
	sorted_results = {}
	top_hundred_results = []
	results=[]
	if request.method == "POST":
	    # get the url entered
	    try:
	        url = request.form['url']
	        r = requests.get(url)
	    except:
	        errors.append(
	            "The URL have entered is not valid."
	        )
	        return render_template('index.html', errors=errors)
	    if r:
	        # text processing
	        raw = BeautifulSoup(r.text, 'html.parser').get_text()
	        nltk.data.path.append('./nltk_data/')  # set the path
	        tokens = nltk.word_tokenize(raw)
	        text = nltk.Text(tokens)
	        # remove punctuation, count raw words
	        nonPunct = re.compile('.*[A-Za-z].*')
	        raw_words = [w for w in text if nonPunct.match(w)]
	        raw_word_count = Counter(raw_words)
	        # stop words
	        no_stop_words = [w for w in raw_words if w.lower() not in stops]
	        no_stop_words_count = Counter(no_stop_words)

	        # sort the results
	        sorted_results = sorted(
	            no_stop_words_count.items(),
	            key=operator.itemgetter(1),
	            reverse=True
	        )

	        # Strip the list of words to the top 100 words
	        if len(sorted_results) >= 100:
	        	top_hundred_results = sorted_results[:100]
	        else:
	        	top_hundred_results = sorted_results
	        print (type(top_hundred_results))
	        # Salting the word and creating asymmetric encryption
	        for k,v in top_hundred_results:
	        	salt = uuid.uuid4().hex    # Adding the salt
	        	hashed_word = hashlib.sha256(k.encode('utf-8')+salt.encode('utf-8')).hexdigest() # hashing

	        	# Use the python encryption module to encrypt and decrypt if needed
	        	key = Fernet.generate_key()
	        	cipher_suite = Fernet(key)
	        	encrypted_word = cipher_suite.encrypt(k.encode('utf-8'))
	        	#plain_text = cipher_suite.decrypt(cipher_text)
	        	
	        	# populate the results object which is a list of turple containing the encrypted word in string and its frequency
	        	results.append((encrypted_word.decode('utf-8'),v))
	        	#print (k, hashed_word,encrypted_word,v)
	        	# Try/except block to try and save the information to our database.
	        	try:
	        		result = Result(hashed_word=hashed_word,encrypted_word=encrypted_word,frequency=v,url=url)
	        		db.session.add(result)
	        		db.session.commit()
	        	except:
	        		errors.append("Unable to add item to database.")
	            
	return render_template('index.html', errors=errors, results=results)



if __name__ == '__main__':
    application.run()
