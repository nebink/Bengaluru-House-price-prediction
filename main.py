from flask import Flask, render_template, request
import pandas as pd
app=Flask(__name__)

data=pd.read_csv("Cleaned_data.csv")

@app.route('/')
def index():

    locations=sorted(data['location'].unique())

    return render_template('index2.html',locations=locations)

if __name__=="__main__":
    app.run(debug=True, port=5001)