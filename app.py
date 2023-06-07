from flask import Flask, render_template, request
from client import cluster
import random

#This is the connection to the MongoDB server.
cluster = cluster

#This is the main cluster.
db = cluster["Marvin_Chat"]
#This is the collection Responses
responses = db["Responses"]
#This is the collection Keywords
keywords = db["Keywords"]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index2.html")


@app.route("/get")
#This is the main function for the whole website. It gets an input from the html and
#returns a response based on keywords in that input.
def get_bot_response():
    #This is the user input that is sent via the html
    user_text = request.args.get('msg')
    intent = 0
    #find() is the same as a SQL select statement and the .distinct() is specifing
    #which column you want to select. Here it is SELECT Keyword FROM Keywords.
    for key in keywords.find().distinct("Keyword"):
        #Then it checks to see if any words in the user input match any of the keywords
        #in the Keywords collection. It also puts in lowercase and removes questionmarks.
        if key in user_text.replace("?", "").lower().split():
            #Here it uses a select statement with a "where". So in SQL this is
            #SELECT Intent_ID FROM Keywords WHERE Keywords = key.
            #So it checks all the keywords and sets the intent to the intent of that
            #keyword.
            for i in keywords.find({"Keyword": key}).distinct("Intent_ID"):
                intent = i
    if intent == 0:
        intent = 7
    responses_list = []
    #Here it is in SQL SELECT Response_Name FROM Responses WHERE Intent_ID = intent.
    #It then adds all the responses wit that intent_ID to a list and returns a
    #random response from that list.
    for response in responses.distinct("Response_Name", {"Intent_ID": intent}):
        responses_list.append(response)
    return responses_list[random.randint(0, (len(responses_list)) - 1)]


if __name__ == '__main__':
    app.run()
