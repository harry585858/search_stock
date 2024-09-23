from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    nameOfStock = 'none'
    nameOfStock = request.form['nameOfStock']
    return render_template('search.html',nameOfStock=nameOfStock)
    
if __name__=='__main__':
    app.debug=True
    app.run()