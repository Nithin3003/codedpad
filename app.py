from flask_pymongo import PyMongo
from flask import Flask,redirect,url_for,render_template,request,session
# from werkzeug.security import generate_password_hash, check_password_hash
import csv 
from secrets import token_urlsafe
app= Flask(__name__) 


app.config['MONGO_URI'] = "mongodb+srv://msnithin84:Nithin@cluster0.wob2cfi.mongodb.net/coded"
app.config['SECRET_KEY'] = token_urlsafe(32)

mongo = PyMongo(app)
coded = mongo.db.codedpad
fields = [ 'name' , 'email' , 'feedback']

def fb(mydict):
    with open('data.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(mydict)
# store_password= []

# store_csv('password1', 'hi')
def check_password(password):
    data = coded.find_one({'password' : password })
    return data if data else False

def check_newdata():
    data = coded.find_one({'password' : session['newpassword']})
    return data  if data else False


@app.route('/')
def home():
    return render_template("home2.html")


@app.route("/display", methods=['POST', 'GET'])
def display_data():
    if request.method == 'POST':
        session['newpassword']= request.form['password']
        result = check_password(session['newpassword'])

        if result:
            return render_template('data2.html', data=result['data'],passs= request.form['password'])
        else:
            # Handle invalid password case (e.g., display an error message)
            return  render_template('data2.html', data="" ,passs= request.form['password'] )

    return redirect('/')



@app.route('/final', methods=['POST', 'GET'] )
def display_newdata():
    if request.method =='POST':
        value = request.form['data']
        old_data  =check_newdata()
        if old_data and session['newpassword'] == old_data['password']:  # if old data with/without changes
            coded.find_one_and_update({'password' :session['newpassword']}, { '$set':{ 'data': value}}) #session['newpassword'] = None

            return render_template('final.html' ,change = True)
            # newdata = coded.insert_one({'password' :session['newpassword'],'data': value  } )

        else:#new data / password 
            coded.insert_one({'password' :session['newpassword'],'data': value  } )
            # store_password.clear
            # session['newpassword'] = None
            return render_template('final.html' ,change = False)


    return 'get <a href="/"><button> Go back </button></a>'

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method=='POST':
        # return request.form
        fb(request.form)
        return f"<h1> Feedback Saved <br> </h1> get <a href='/'><button> Go back </button></a>"
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)