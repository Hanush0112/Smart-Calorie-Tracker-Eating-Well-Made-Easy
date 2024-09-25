import pandas as pd

class CalorieCounter:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.food_log = []
        self.food_database = pd.read_csv('food_database.csv')

    def add_food(self, food_item, quantity):
        if food_item in self.food_database['food_item'].values:
            calories_per_unit = self.food_database[self.food_database['food_item'] == food_item]['calories_per_unit'].values[0]
            calories = calories_per_unit * quantity
            self.food_log.append({'food_item': food_item, 'quantity': quantity, 'calories': calories})
        else:
            print("Food item not found in database")

    def total_calories(self):
        return sum(item['calories'] for item in self.food_log)

    def compare_intake_to_tdee(self):
        tdee = self.user_profile.calculate_tdee()
        intake = self.total_calories()
        return intake - tdee

    def get_food_log(self):
        return self.food_log
