#import important libraries
import os
import pickle
from flask import Flask, request, jsonify, render_template
#from flask_restful import Api, Resource
#import helper

app = Flask(__name__)
#api = Api(app)

#load the saved ML model from local
loaded_model = pickle.load(open('model.pickle', 'rb'))

#runs index.html as homepage for the website automatically
@app.route("/")
def home():
	return render_template("index.html")


@app.route('/classify', methods=['POST'])
def classify():
	#for rendering results on html page
	input = request.form['content']
	print(input, flush=True)
	test= dict([i, True] for i in input.split())
	print(test, flush=True)
	output = loaded_model.classify(test)
	return render_template('index.html', show_text='Sentiment : {}'.format(output))



@app.route('/classify_api', methods = ['POST'])
def inputModel():
	journie_input = request.getjson(force= True)
	#test= dict([i, True] for i in journie_input.split())
	result = loaded_model.classify(journie_input)
	#print(result)
	return jsonify(output)


#run the app in debug mode
if __name__ == '__main__':
	app.run(debug=True)