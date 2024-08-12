import sqlite3
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from models import db, Student, Management, meal
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/student_signin', methods=['GET', 'POST'])
def student_signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = Student.query.filter_by(email=email, password=password).first()
            if user:
                return redirect(url_for('dashboard'))  # Redirect to dashboard route
        return render_template('student_signin.html', error="Invalid email or password")
    return render_template('student_signin.html')

@app.route('/management_signin', methods=['GET', 'POST'])
def management_signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = Management.query.filter_by(email=email, password=password).first()
            if user:
                return redirect(url_for('mess_stats'))  # Redirect to dashboard route
        return render_template('management_signin.html', error="Invalid email or password")
    return render_template('management_signin.html')

@app.route('/mess_stats',methods=['GET','POST'])
def mess_stats():
      #session = Session()
      try:
           breakfast_count = db.session.query(meal.Number_of_meals).filter(meal.meal_type == 'Breakfast').scalar()
           lunch_count = db.session.query(meal.Number_of_meals).filter(meal.meal_type == 'Lunch').scalar()
           dinner_count = db.session.query(meal.Number_of_meals).filter(meal.meal_type == 'Dinner').scalar()
           print(breakfast_count,lunch_count,dinner_count)
      except Exception as e:
          print("Error:", e)
      finally:
          db.session.close()
      return render_template('messtats.html',breakfast=breakfast_count, lunch=lunch_count, dinner=dinner_count)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']  # Get user type from form

        if user_type == 'student':
            new_user = Student(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('student_signin'))
        elif user_type == 'management':
            new_user = Management(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('management_signin'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    breakfast = "Oatmeal"
    lunch = "Grilled Chicken Salad"
    dinner = "Spaghetti Bolognese"
    user_role = 'student'  # Mock user role for demonstration
    return render_template('dashboard.html', breakfast=breakfast, lunch=lunch, dinner=dinner, user_role=user_role)

@app.route('/cancel_meal', methods=['POST','GET'])
def cancel_meal():
    print('Hi')
    if request.method=='GET':
        meal_type=request.args.get('meal')
        print(meal_type)
        if(meal_type=='breakfast'):
            print('I work in breakfast')
            #sess.query(User).filter(User.age == 25).\
            #update({User.age: User.age - 10}, synchronize_session=False)
            db.session.query(meal).filter(meal.meal_type == 'Breakfast').update({meal.Number_of_meals : meal.Number_of_meals-1})
            db.session.commit()
            #db.session.query(meal).filter_by(meal_type='Breakfast').update({"Number_of_meals":})
            return jsonify({'message': 'Meal cancelled successfully'})
        if(meal_type=='lunch'):
            print('I work in breakfast')
            db.session.query(meal).filter(meal.meal_type == 'Lunch').update({meal.Number_of_meals : meal.Number_of_meals-1})
            db.session.commit()
            return jsonify({'message': 'Meal cancelled successfully'})
        if(meal_type=='dinner'):
            print('I work in dinner')
            db.session.query(meal).filter(meal.meal_type == 'Dinner').update({meal.Number_of_meals : meal.Number_of_meals-1})
            db.session.commit()
            return jsonify({'message': 'Meal cancelled successfully'})
        

      
    


if __name__ == '__main__':
    app.run(debug=True)
