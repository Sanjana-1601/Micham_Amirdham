from flask import Flask, render_template,request
import pymongo
 

app = Flask('test', template_folder= 'templates')

 
 

#index
@app.route('/')
def index():
 
    # return render_template("index.html",user_image=pic1)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)   