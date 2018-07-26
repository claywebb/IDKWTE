from math import log
import random

max_radius = 1.0;
selection_multiplier = .2;

def set_radius(radius):
    global max_radius
    max_radius = radius

def set_selectionmult(mult):
    global selection_multiplier
    selection_multiplier = mult

def decision(probability):
    return random.random() < probability

def get_goodness(distance, rating):
    goodness = log(rating) + ((max_radius - distance) / 5)
    return goodness

def get_next_restaurant(restaurant):


def eliminate_below_rating(restaurants, min_rating):
    for restaurant in restaurants:
        if restaurant["rating"] < min_rating:
            eliminate_restaurant(restaurant)

def eliminate_restaurant(restaurants, restaurant):
    restaurants.remove(restaurant)
    return restaurants