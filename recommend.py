from math import log
import random

max_radius = 1600
prob_selec = max(random.triangular(0,.1,.9),random.triangular(0,.1,.4))

def set_radius(radius):
    global max_radius
    max_radius = radius

def set_selectionmult(mult):
    global selection_multiplier
    selection_multiplier = mult

def decision(probability):
    return random.random() < probability

def select_num(totRest):
    global prob_selec
    for n in range(1,totRest+1):
        selected = decision(prob_selec)
        if selected:
            break
        prob_selec = prob_selec * .92
    if (n == totRest):
        return random.randint(0,totRest)
    else:
        return n

def get_goodness(distance, rating):
    goodness = log(rating) + (((max_radius/1600) - (distance/1600)) / 5)
    return goodness

def get_next_restaurant(restaurants):
    totRest = len(restaurants)
    nextInt = select_num(totRest)
    return restaurants[nextInt]

def eliminate_below_rating(restaurants, min_rating):
    for restaurant in restaurants:
        if restaurant["rating"] < min_rating:
            eliminate_restaurant(restaurants, restaurant)

def eliminate_restaurant(restaurants, restaurant):
    restaurants.remove(restaurant)
    return restaurants

def init_recomendations(restaurants):
    recommendations = []
    for i in range(0, 10):
        restaurant = get_next_restaurant(restaurants)
        recommendations.append(restaurant)
        restaurants = eliminate_restaurant(restaurants, restaurant)
    return recommendations