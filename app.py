from flask import Flask, render_template, request, url_for, redirect,flash,session,jsonify
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask import send_file
import json

app = Flask(__name__)
app.secret_key="parsheela"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2004'
app.config['MYSQL_DB'] = 'chronicdisease'
mysql = MySQL(app)

##form validation

class user:
    def __init__(self,Id,Username,Password):
        self.Id=Id
        self.Username=Username
        self.Password=Password
 
class signupform(FlaskForm):
    Id=IntegerField('Id')  
    Username=StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
    Password=PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
    MailID=StringField('MailID',validators=[InputRequired(),Length(min=10,max=30)])
    PhoneNumber=StringField('PhoneNumber',validators=[InputRequired(),Length(min=10,max=10)])
    Place=StringField('Place',validators=[InputRequired(),Length(min=5,max=15)])   
    Submit=SubmitField('Signup')


class loginform(FlaskForm):
    Username=StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
    Password=PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
    Submit=SubmitField('Login')

def passwordstrength(Password):
    strength = 0
    criteria = {
        "length": len(Password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", Password)),
        "lowercase": bool(re.search(r"[a-z]", Password)),
        "digit": bool(re.search(r"\d", Password)),
        "special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", Password))
    }
    strength = sum(criteria.values())
    if strength == 5:
        return "Very Strong"
    elif strength == 4:
        return "Strong"
    elif strength == 3:
        return "Moderate"
    elif strength == 2:
        return "Weak"
    else:
        return "Very Weak"
    
#signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = signupform()
    if form.validate_on_submit():
        Username = form.Username.data
        Password = form.Password.data
        MailID=form.MailID.data
        PhoneNumber=form.PhoneNumber.data
        Place=form.Place.data
        if not passwordstrength(Password) :
            flash('Re-enter the password,it must contain uppercase,lowercase,digit and special characters','danger')
            return redirect(url_for('signup'))
        Hashed_password=generate_password_hash(Password)
        cur=mysql.connection.cursor()
        cur.execute("SELECT Id FROM signup WHERE Username = %s", (Username,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template("signup.html", form=form)
        cur.execute("INSERT INTO signup (Username, Password, MailID, PhoneNumber, Place) VALUES (%s, %s, %s, %s, %s)",(Username, Hashed_password, MailID, PhoneNumber, Place))
        mysql.connection.commit()
        session['Username'] = Username
        session['Email'] = MailID
        session['Mobile'] = PhoneNumber
        session['Place'] = Place
        cur.close()
        flash('Signup successful', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

#login
@app.route("/login", methods=['GET','POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        Username = form.Username.data
        Password = form.Password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT Id, Username, Password, MailID, PhoneNumber, Place FROM signup WHERE Username = %s", (Username,))
        data = cur.fetchone() 
        cur.close()
        if data and check_password_hash(data[2], Password): 
            session['Username'] = data[1] 
            session['Email'] = data[3]  
            session['Mobile'] = data[4] 
            session['Place'] = data[5] 
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Username or Password!', 'danger')
            return(redirect(url_for("create")))
    return render_template("login.html", form=form)


#logout
@app.route("/logout")
def logout():
    session.clear()  
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


#profile
@app.route('/myprofile')
def profile():
    if 'Username' not in session:
        flash("Please Sign up or log in to access your profile.", "warning")
        return redirect(url_for('login'))
    user = {
    "username": session.get("Username", "Guest"),
    "email": session.get("Email", "Guest"),
    "mobile": session.get("Mobile", "Guest"),
    "place": session.get("Place", "Guest"),
}
    return render_template("profile.html", user=user)

#home page
@app.route("/")
def home():
    return render_template("home.html")

# Display table data
@app.route("/table")
def display():
    if 'Username' not in session:
        flash("Please log in first", "danger")
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM chronic")
    data = cur.fetchall()
    cur.close()
    return render_template("table.html", data=data)


# Create new entry
@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == 'POST':
        pName = request.form.get("Name")
        pAge = request.form.get("Age")
        pSex = request.form.get("Sex")
        pHighChol = request.form.get("HighChol")
        pCholCheck = request.form.get("CholCheck")
        pBMI = request.form.get("BMI")
        pSmoker = request.form.get("Smoker")
        pHeartDiseaseorAttack = request.form.get("HeartDiseaseorAttack")
        pPhysActivity = request.form.get("PhysActivity")
        pFruits = request.form.get("Fruits")
        pVeggies = request.form.get("Veggies")
        pHvyAlcoholConsump = request.form.get("HvyAlcoholConsump")
        pGenHlth = request.form.get("GenHlth")
        pMentHlth = request.form.get("MentHlth")
        pPhysHlth = request.form.get("PhysHlth")
        pDiffWalk = request.form.get("DiffWalk")
        # pStroke = request.form.get("Stroke")
        # pHighBP = request.form.get("HighBP")
        # pDiabetes = request.form.get("Diabetes")

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO chronic (Name, Age, Sex, HighChol, CholCheck, BMI, Smoker, 
            HeartDiseaseorAttack, PhysActivity, Fruits, Veggies, HvyAlcoholConsump, 
            GenHlth, MentHlth, PhysHlth, DiffWalks)  
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pName, pAge, pSex, pHighChol, pCholCheck, pBMI, pSmoker, 
              pHeartDiseaseorAttack, pPhysActivity, pFruits, pVeggies, pHvyAlcoholConsump, 
              pGenHlth, pMentHlth, pPhysHlth, pDiffWalk))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("display"))
    return render_template("index.html")

#Edit entry
@app.route("/edit/<string:Id>", methods=["POST", "GET"])
def edit(Id):
    if request.method == 'POST':
        pName = request.form.get("Name")
        pAge = request.form.get("Age")
        pSex = request.form.get("Sex")
        pHighChol = request.form.get("HighChol")
        pCholCheck = request.form.get("CholCheck")
        pBMI = request.form.get("BMI")
        pSmoker = request.form.get("Smoker")
        pHeartDiseaseorAttack = request.form.get("HeartDiseaseorAttack")
        pPhysActivity = request.form.get("PhysActivity")
        pFruits = request.form.get("Fruits")
        pVeggies = request.form.get("Veggies")
        pHvyAlcoholConsump = request.form.get("HvyAlcoholConsump")
        pGenHlth = request.form.get("GenHlth")
        pMentHlth = request.form.get("MentHlth")
        pPhysHlth = request.form.get("PhysHlth")
        pDiffWalk = request.form.get("DiffWalk")
        # pStroke = request.form.get("Stroke")
        # pHighBP = request.form.get("HighBP")
        # pDiabetes = request.form.get("Diabetes")
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE chronic 
            SET Name=%s, Age=%s, Sex=%s, HighChol=%s, CholCheck=%s, BMI=%s, Smoker=%s, 
                HeartDiseaseorAttack=%s, PhysActivity=%s, Fruits=%s, Veggies=%s, 
                HvyAlcoholConsump=%s, GenHlth=%s, MentHlth=%s, PhysHlth=%s, DiffWalk=%s
            WHERE Id=%s
        """, (pName, pAge, pSex, pHighChol, pCholCheck, pBMI, pSmoker, 
              pHeartDiseaseorAttack, pPhysActivity, pFruits, pVeggies, pHvyAlcoholConsump, 
              pGenHlth, pMentHlth, pPhysHlth, pDiffWalk, Id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("display"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM chronic WHERE Id=%s", (Id,))
    data = cur.fetchone()
    cur.close()
    return render_template("edit.html", data=data)

# Delete entry
@app.route("/delete/<string:Id>", methods=['GET'])
def delete(Id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM chronic WHERE Id=%s", (Id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("display"))


import pandas as pd
# Load trained models
import pickle
models = {}
diseases = ['Diabetes', 'Stroke', 'HighBP']
for disease in diseases:
    with open(f'{disease.lower()}_model.pkl', 'rb') as file:
        model, feature_columns = pickle.load(file)
        models[disease] = (model, feature_columns)

# predict
@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = {
            'Age': int(request.form['Age']),
            'Sex': int(request.form['Sex']),
            'HighChol': int(request.form['HighChol']),
            'CholCheck': int(request.form['CholCheck']),
            'BMI': float(request.form['BMI']),
            'Smoker': int(request.form['Smoker']),
            'HeartDiseaseorAttack': int(request.form.get('HeartDiseaseorAttack', 0)),
            'PhysActivity': int(request.form['PhysActivity']),
            'Fruits': int(request.form['Fruits']),
            'Veggies': int(request.form['Veggies']),
            'HvyAlcoholConsump': int(request.form['HvyAlcoholConsump']),
            'GenHlth': int(request.form['GenHlth']),
            'MentHlth': int(request.form['MentHlth']),
            'PhysHlth': int(request.form['PhysHlth']),
            'DiffWalk': int(request.form['DiffWalk'])
        }
        

        input_df = pd.DataFrame([form_data])
        results = {}

        for disease, (model, feature_cols) in models.items():
            aligned_input = input_df.reindex(columns=feature_cols, fill_value=0)
            prediction = model.predict(aligned_input)[0]
            results[disease] = "High Risk" if prediction == 1 else "Low Risk"

        # Convert results to a DataFrame
        results_df = pd.DataFrame(list(results.items()), columns=['Disease', 'Risk'])
        
        # Save the results to a CSV file
        file_path = 'prediction_results.csv'
        results_df.to_csv(file_path, index=False)
        # json format
        results_json = json.dumps(results)

        return render_template('result.html', prediction=results, download_url=url_for('download_file', filename='prediction_results.csv'))

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Provide the file for download
        return send_file(f'./{filename}', as_attachment=True)
    except Exception as e:
        return f"❌ Error: {str(e)}"



if __name__ == "__main__":
    app.run(debug=True)





