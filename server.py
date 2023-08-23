import json
from flask import Flask,request
from flask_cors import CORS
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]','',text)
        text = re.sub("\\W"," ",text)
        text = re.sub('https?://S+|www\.\S+','',text)
        text = re.sub('<.*?>+','',text)
        text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
        text = re.sub('\n','',text)
        text = re.sub('\w*\d\w*','',text)
        return text
def output_label(n):
    if n== 0:
        return "Fake News"
    elif n==1:
        return "Not a Fake News"

def algo(news):
    data_fake = pd.read_csv('D:/fakeNews/flask-server/DataSets/Fake.csv')
    data_true = pd.read_csv('D:/fakeNews/flask-server/DataSets/True.csv')
    # data_fake.head()
    # data_true.head()
    data_fake['class'] = 0
    data_true['class'] = 1
    # data_fake.shape, data_true.shape
    # data_fake.shape, data_true.shape
    # data_fake_manual_testing['class']=0
    # data_true_manual_testing['class']=1
    data_merge = pd.concat([data_fake,data_true],axis=0)
    # data_merge.head(10)
    data_merge.columns
    data = data_merge.drop(['title','subject','date'],axis=1)
    data.isnull().sum()
    data = data.sample(frac=1)
    # data.head()
    data.reset_index(inplace = True)
    data.drop(['index'],axis=1,inplace =True)
    # data.columns
    # data.head()
    data['text'] = data['text'].apply(wordopt)
    x = data['text']
    y = data['class']
    x_train, x_test, y_train, y_test =  train_test_split(x,y,test_size=0.25)  
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)
    LR = LogisticRegression()
    LR.fit(xv_train,y_train)
    pred_lr = LR.predict(xv_test)
    LR.score(xv_test,y_test)
    #print(classification_report(y_test,pred_lr))
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    return ("Result: {}".format(output_label(pred_LR[0])))
    


app = Flask(__name__)


CORS(app)

@app.route('/data',methods=["POST"])
def predict():
    tagsArray = request.get_json()
    tagsArray = tagsArray["arg"]
    print(tagsArray)
    
    domains=algo(tagsArray)
    print(domains)
    
    return json.dumps(domains)
    

if __name__ == '__main__':
    app.run(debug=True)


    