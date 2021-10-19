from flask import Flask, render_template,request
import pymongo
from pymongo import MongoClient
import os
import json
from bson import json_util

app = Flask('test', template_folder= 'templates')


cluster = pymongo.MongoClient('mongodb+srv://Sanjana:yes1234@cluster0.vvgoz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["project1"]
donarcol = db["food_dr"]
foodcol = db["donar"]
reccol = db["receiver"]

picfolder=os.path.join('pics')
app.config['UPLOAD_FOLDER']=picfolder


#index
@app.route('/')
def index():
    return render_template("index.html")

#donator login page
@app.route('/donator',methods=["POST","GET"])
def donator():
    return render_template("donator.html")    

#donator submit page
@app.route('/showd', methods=["POST","GET"])
def showd():
    name =request.form.get("name") 
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    phno = request.form.get('phno')
    result_1 = donarcol.find({"phno" : { "$eq" : phno} })
    lt= len(list(result_1))
    if (lt < 1):
        donarcol.insert({ "name": name, "email": email, "pwd" : pwd, "phno": phno }) 
    return render_template("donreg.html", value1 =name , value2=phno)

#receiver login page
@app.route('/receiver', methods=["POST","GET"])
def reclogin():
    return render_template("receiver.html")

#receiver submit page
@app.route('/receiversub', methods=["POST","GET"])
def recshow():
    rname = request.form.get("rname") 
    remail = request.form.get('remail')
    rpwd = request.form.get('rpwd')
    rphno = request.form.get('rphno')
    result_2 = reccol.find({"rphno" : { "$eq" : rphno} })
    bt= len(list(result_2))
    print(bt)
    for res in result_2:
        numb = res.get("numb")
        print(numb)
        print("***************************************")
    if (bt < 1):
        reccol.insert({ "rname": rname, "remail": remail, "rpwd" : rpwd, "rphno": rphno })

    available_result = foodcol.find({"flag" : { "$eq" : 0} })  
    ava_len= len(list(available_result))
    print("*******")
    print(ava_len)
    myname = "Sanjana"
    addi =  "Chennai"
    fmenu=  "idly"
    fed= 50
    num=9876543210
    food="Veg"
    if  (ava_len < 1) :
        return render_template("Notavailable.html")
    else :
        print ("am here88888888888888888888888")  
        for x in available_result:
            myname=x['firstname']
            num = x['numb']
            add = x['add'] 
            fed= x['fed']
            fmenu= x['menu']  
            food=x['food']
            print ("resultheeeeeeeeeeeeeeeeeeeeee")
            print (num)
        return render_template("available.html",fname =myname,num= num,addi=addi, fmenu =fmenu, fed=fed,food=food)

#fname = firstname , num =  , feed="fed" , addi="add", vornv="food" , fmenu="menu"

#donor registration
@app.route('/donreg', methods=["POST","GET"])
def donreg():
    firstname = request.form.get("firstname")
    numb = request.form.get('numb')
    fed = request.form.get('fed')
    add = request.form.get('add')
    food = request.form.get('food')
    menu = request.form.get('menu')
    flag = 0
    foodcol.insert({ "firstname": firstname, "numb": numb, "fed" : fed, "add": add , "food" : food, "menu": menu, "flag" : flag }) 
    return render_template("ThankYou.html" )
#, fname = firstname , num =numb , feed=fed , addi=add, vornv=food , fmenu=menu


#availabilities final page
@app.route('/available', methods=["POST","GET"])
def available():
    return render_template("available.html")

@app.route('/confirm', methods=["POST","GET"])
def confirm():
    value1 = request.form.get("numb")
    myquery = { "numb": value1}
    newvalues = { "$set": { "flag": 1 } }
    foodcol.update_one(myquery, newvalues)

    print (value1)
    return render_template("ThankYou.html")

 
if __name__ == '__main__':
    app.run(debug=True)        