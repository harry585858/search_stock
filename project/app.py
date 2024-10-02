from flask import Flask, render_template, request
import numpy as np

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    nameOfStock = {'','','',''}
    nameOfStock = request.form.getlist('nameOfStock[]')
    return render_template('search.html',nameOfStock=nameOfStock)

if __name__=='__main__':
    app.run(debug=True)