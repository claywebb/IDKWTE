# -*- coding: utf-8 -*-
""" simple fact sample app """
from __future__ import print_function

import recommend
import yelp

import json

SKILL_NAME = "I Don't Know Where To Eat"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "I Don't Know Where To Eat can help you find a nearby restaurant when you are indecisive! " \
               "Just say, Alexa, I don't know where to eat."
HELP_REPROMPT = "Just say, Alexa, I don't know where to eat."
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The I Don't Know Where To Eat skill can't help you with that.  " \
                   "It can help you find nearby restaurants and make suggestions. " \
                   "To invoke this skill, just say, Alexa, I Don't Know Where To Eat."
FALLBACK_REPROMPT = "Just say, Alexa, I don't know where to eat."

BEGIN_STATE = "START"
WAITING_STATE = "WAITING"
FAIL_STATE = "FAIL"

LOGGING = True;

# --------------- App entry point -----------------

def lambda_handler(event, context):
    """  App entry point  """

    #print(event)

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']

    # process the intents
    if intent_name == "GetRestaurantIntent":
        return get_restaurant_response(session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(session)
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response(session)
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response(session)
    elif intent_name == "AMAZON.YesIntent":
        return get_answer(session, True)
    elif intent_name == "AMAZON.NoIntent":
        return get_answer(session, False)
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response(session)
    else:
        print("invalid Intent reply with help")
        return get_help_response()


def get_restaurant_response(session):
    """ get and return a restaurant """

    # Array of dictionaries. All the restaurants.
    global restaurants

    if "attributes" in session and "restaurants" in session["attributes"]:
        restaurants = session["attributes"]["restaurants"]

        if "selected_restaurant" in session["attributes"]:
            selected = session["attributes"]["selected_restaurant"]
            restaurants.remove(selected)
    else:
        restaurants = yelp.getYelp(get_location())

    # Selected restaurant
    restaurant = recommend.get_next_restaurant(restaurants)

    attributes = {"STATE": WAITING_STATE,
                  "restaurants": restaurants,
                  "selected_restaurant": restaurant}

    speech_text = get_text_from_restaurant(restaurant)

    return response_with_attributes(speech_response_prompt(speech_text, False, speech_text), attributes)


def get_answer(session, affirmative):
    """ process user's response """

    if session["attributes"] and "STATE" in session["attributes"]:
        if session["attributes"]["STATE"] == WAITING_STATE:
            if affirmative:
                # Answered YES
                speech_text = get_detailed_text_from_restaurant(session["attributes"]["selected_restaurant"])
                card_content = get_detailed_card_from_restaurant(session["attributes"]["selected_restaurant"])
                card_link = get_maps_link_from_restaurant(session["attributes"]["selected_restaurant"])
                return response(speech_response_with_card("I Don't Know Where To Eat", card_content, card_link, speech_text, True))
            else:
                # Answered No
                return get_restaurant_response(session)
        else:
            return get_fallback_response(session)
    else:
        return get_fallback_response(session)


def get_help_response(session):
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message, False, speech_message))
def get_launch_response(session):
    """ get and return the help string  """

    return get_restaurant_response(session)

def get_stop_response(session):
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response(session):
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, True))

def on_session_started():
    """" called when the session starts  """
    if LOGGING:
        print("on_session_started")

def on_session_ended():
    """ called on session ends """
    if LOGGING:
        print("on_session_ended")

def on_launch(request, session):
    """ called on Launch, we reply with a launch message  """

    return get_launch_response(session)


# --------------- Speech response handlers -----------------

def get_text_from_restaurant(restaurant):
    speech_text = "How about " + restaurant["name"] + "? "

    if restaurant["categories"] and len(restaurant["categories"]) >= 2:
        speech_text += "It specializes in " + restaurant["categories"][0]["title"] + \
                        " and " + restaurant["categories"][1]["title"] + ". "
    elif restaurant["categories"] and len(restaurant["categories"]) >= 1:
        speech_text += "It specializes in " + restaurant["categories"][0]["title"] + ". "

    speech_text += "It has a rating of " + str(restaurant["rating"]) + " stars" \
                   " and is only " + get_distance_string(restaurant["distance"]) + " away!"

    return speech_text


def get_detailed_text_from_restaurant(restaurant):

    # TODO make this text more detailed
    speech_text = "Great! You selected " + restaurant["name"] + "! "

    if restaurant["categories"] and len(restaurant["categories"]) >= 2:
        speech_text += "It specializes in " + restaurant["categories"][0]["title"] + \
                        " and " + restaurant["categories"][1]["title"] + ". "
    elif restaurant["categories"] and len(restaurant["categories"]) >= 1:
        speech_text += "It specializes in " + restaurant["categories"][0]["title"] + ". "

    speech_text += "It has a rating of " + str(restaurant["rating"]) + " stars" \
                   " and is only " + get_distance_string(restaurant["distance"]) + " away!"

    return speech_text

def get_detailed_card_from_restaurant(restaurant):
    return restaurant["name"] + "\n" + restaurant["address1"] + "\n" "Click the link below for Google Maps:"

def get_maps_link_from_restaurant(restaurant):
    return ("https://google.com/maps/place/" + restaurant["address1"]).replace(" ", "+")

def get_distance_string(distance):

    # TODO make this better
    return str(int(distance)) + " meters"


def get_location():

    # TODO actually get location

    return "Amazon Spheres"


def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }


def dialog_response(endsession):
    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }


def speech_response_with_card(title, output, link, cardcontent, endsession):
    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent,
            'redirectionUrl': link
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }


def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }


def speech_response_prompt(output, endsession, reprompt_text):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }


def response_with_attributes(speech_message, attributes):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speech_message
    }


def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }