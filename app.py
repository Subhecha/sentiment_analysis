#import important libraries
import json
import os
import pickle
from flask import Flask, request, jsonify, render_template
#from flask_restful import Api, Resource
#import helper

app = Flask(__name__)
#api = Api(app)

#load the saved ML model from local
loaded_model = pickle.load(open('model.pickle', 'rb'))

#checkkey
def checkKey(dict, key):
	if key in dict.keys():
		return True
	else:
		return False

#declaring string


#runs index.html as homepage for the website automatically
@app.route("/")
def home():
	return render_template("index.html")	




#print(input, flush=True)
#test= dict([i, True] for i in input.split())
#print(test, flush=True)
#output = loaded_model.classify(test)
#print(type(output), flush=True)
#return render_template('index.html', show_text='Sentiment : {}'.format(output))


@app.route('/classify', methods=['POST'])
def classify():
    journal_data = request.get_json(force=True)
    solution= ""
    for i in range(len(journal_data["blocks"])):
        if(checkKey(journal_data["blocks"][i]["data"], "style")):
            i=i+1
        else:
            solution=solution+journal_data["blocks"][i]["data"]["text"]
    sentimentAnalysis = dict([i,True] for i in solution.split())
    SAmodel = loaded_model.classify(sentimentAnalysis)
    return jsonify(SAmodel)

@app.route('/classify_api', methods = ['POST'])
def inputModel():
	journie_input = request.get_json(force= True)
	test= dict([i, True] for i in journie_input.split())
	result = loaded_model.classify(journie_input)
	print(result)
	return jsonify(result)


#run the app in debug mode
if __name__ == '__main__':
	app.run(debug=True)
