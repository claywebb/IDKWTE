from math import log
import random

max_radius = 1600
prob_selec = max(random.triangular(0, .1, .9), random.triangular(0, .1, .4))


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
    last = totRest
    for n in range(0, totRest):
        selected = decision(prob_selec)
        if selected:
            last = n
            break
        prob_selec = prob_selec * .92
    if (last == totRest):
        return random.randint(0, totRest - 1)
    else:
        return last


def get_goodness(distance, rating):
    goodness = log(rating) + (((max_radius / 1600) - (distance / 1600)) / 5)
    return goodness


def compare(rest1, rest2):
    if get_goodness(rest1["distance"], rest1["rating"]) > get_goodness(rest2["distance"], rest2["rating"]):
        return True
    else:
        return False


def sort_restaurants(restaurants):
    restaurants.sort(compare)
    return restaurants

def get_next_restaurant(restaurants):
    totRest = len(restaurants)
    nextInt = select_num(totRest)
    return restaurants[nextInt]


def eliminate_below_rating(restaurants, min_rating):
    new_list = []
    for restaurant in restaurants:
        if restaurant["rating"] >= min_rating:
            new_list.append(restaurant)
    return new_list


def eliminate_restaurant(restaurants, restaurant):
    restaurants.remove(restaurant)
    return restaurants


def init_recomendations(restaurants):
    restaurants = sort_restaurants(restaurants)
    recommendations = []
    for i in range(0, 10):
        restaurant = get_next_restaurant(restaurants)
        recommendations.append(restaurant)
        restaurants = eliminate_restaurant(restaurants, restaurant)
    return recommendations
