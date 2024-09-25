from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from calorie_counter import CalorieCounter
from user_profile import UserProfile

app = Flask(__name__)

profiles = {}
current_profile = None
calorie_counter = None

@app.route('/')
def home():
    global current_profile
    return render_template('index.html', profiles=profiles, current_profile=current_profile)

@app.route('/create_profile', methods=['POST'])
def create_profile():
    global current_profile, calorie_counter
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    activity_level = request.form['activity_level']
    profile = UserProfile(name, age, gender, weight, height, activity_level)
    profiles[name] = profile
    current_profile = profile
    calorie_counter = CalorieCounter(current_profile)
    print(f"Created profile for {name}")
    return redirect(url_for('home'))

@app.route('/select_profile', methods=['POST'])
def select_profile():
    global current_profile, calorie_counter
    name = request.form['name']
    if name in profiles:
        current_profile = profiles[name]
        calorie_counter = CalorieCounter(current_profile)
        print(f"Selected profile: {name}")
    else:
        print(f"Profile not found: {name}")
    return redirect(url_for('home'))

@app.route('/add_food', methods=['POST'])
def add_food():
    food_item = request.form['food_item']
    quantity = float(request.form['quantity'])
    calorie_counter.add_food(food_item, quantity)
    print(f"Added food: {food_item}, Quantity: {quantity}")
    return redirect(url_for('home'))

@app.route('/total_calories')
def total_calories():
    total = calorie_counter.total_calories()
    print(f"Total calories: {total}")
    return f"Total calories consumed: {total}"

@app.route('/caloric_balance')
def caloric_balance():
    balance = calorie_counter.compare_intake_to_tdee()
    print(f"Caloric balance: {balance}")
    return f"Caloric balance (intake - TDEE): {balance}"

@app.route('/food_log')
def food_log():
    log = calorie_counter.get_food_log()
    return render_template('food_log.html', log=log)

@app.route('/calories_chart')
def calories_chart():
    log = calorie_counter.get_food_log()
    food_items = [entry['food_item'] for entry in log]
    calories = [entry['calories'] for entry in log]
    
    fig, ax = plt.subplots()
    ax.bar(food_items, calories)
    plt.xlabel('Food Item')
    plt.ylabel('Calories')
    plt.title('Calories Consumed Per Food Item')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('calories_chart.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
