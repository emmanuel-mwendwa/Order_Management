from datetime import datetime
from flask import Flask, request
import requests
import africastalking
import random
import base64


app = Flask(__name__)

africastalking.initialize("sandbox",  "40120c6927fd58cbcebc5c01045e55b923505ec2be15369eb3c1036811536968")
sms = africastalking.SMS

@app.route('/')
def hello_world():

    return "Hello world"

def confirmation_message(order_number, food_items, amount):
    order_number = random.randrange(0, 100000)
    return f"""
        Your order has been received.\n
        Order number: {order_number},\n
        Order: {food_items}\n
        Amount: Ksh. {amount}\n
        Pay via: Buy Goods: 423424\n
        """


def confirmation_reservation(order_number, people, amount):
  order_number = random.randrange(0, 100000)
  return f"""
      Your reservation has been received.\n
      Reservation number: {order_number},\n
    for {people} people\n
      Amount: Ksh. {amount}\n
      Pay via: Buy Goods: 423424\n
      """



@app.route("/ussd", methods=['POST', 'GET'])
def ussd():
  # Read the variables sent via POST from our API
  session_id = request.values.get("sessionId", None)
  serviceCode = request.values.get("serviceCode", None)
  phone_number = request.values.get("phoneNumber", None)
  text = request.values.get("text", "default")

  if text == '':
    # This is the first request. Note how we start the response with CON
    response = "CON What would you want to do \n"
    response += "1. Make Order \n"
    response += "2. Make Reservation "

  elif text == '1':
    # Business logic for first level response
    response = "CON Choose Meal \n"
    response += "1. Breakfast \n"
    response += "2. Lunch \n"
    response += "3. Supper "

  elif text == '2':
    response = "CON Choose   Reservation type \n"
    response += "1. Seat/Table \n"
    response += "2. Event \n"

  elif text == '2*1':
    response = "CON Input Range of people \n"

  elif text == '2*2':
    response = "CON Input Event's Range of people \n"

  elif text.startswith('2*1*'):
    # Extract the input after '2*1*'
    user_input_range = text.split('*')[-1]

    # Now you can use the user_input_range as a number and process it as needed
    # For example, you can save it to a database or perform further actions

    # Provide a response to the user
    response = f"END {phone_number} Table Reservation for {user_input_range} people confirmed."
    response_message = confirmation_reservation(phone_number, int(user_input_range),
                                      (int(user_input_range) * 50))
    response_to_sms(phone_number, response_message)
  elif text.startswith('2*2*'):
    # Extract the input after '2*1*'
    user_input_range = text.split('*')[-1]

    # Now you can use the user_input_range as a number and process it as needed
    # For example, you can save it to a database or perform further actions

    # Provide a response to the user
    response = f"END {phone_number} Event Reservation for {user_input_range} people confirmed."
    response_message = confirmation_reservation(phone_number, int(user_input_range), "50,000")
    response_to_sms(phone_number, response_message)
    
  elif text == '1*1':
    response = f"CON Choose Breakfast meal \n"
    response += "1.Tea & chapati \n"
    response += "2.Tea & Mandazi \n"
    response += "3.Tea & pancakes"
  elif text == '1*2':
    response = " CON Choose Lunch meal\n"
    response += "1.Rice & beef \n"
    response += "2.Ugali & beef \n"
    response += "3.Chapati & beef"
  elif text == '1*2':
    response = " CON Choose Supper meal\n"
    response += "1.Rice & beef \n"
    response += "2.Ugali & beef \n"
    response += "3.Chapati & beef"

  elif text == '1*2*1':
    option = "Rice & beef"
    response = f" END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "250")
    response_to_sms(phone_number, response_message)
  elif text == '1*2*2':
    option = "Ugali & beef"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "450")
    response_to_sms(phone_number, response_message)
  elif text == '1*2*3':
    option = "Chapati & beef"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "350")
    response_to_sms(phone_number, response_message)
  elif text == '1*1*1':
    option = "Tea & Chapati"
    response = f" END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "60")
    response_to_sms(phone_number, response_message)
  elif text == '1*1*2':
    option = "Tea & Mandazi"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "50")
    response_to_sms(phone_number, response_message)
  elif text == '1*1*3':
    option = "Tea & Pancakes"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "70")
    response_to_sms(phone_number, response_message)
  elif text == '1*3*1':
    option = "Rice & beef"
    response = f" END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "250")
    response_to_sms(phone_number, response_message)
  elif text == '1*3*2':
    option = "Ugali & beef"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "450")
    response_to_sms(phone_number, response_message)
  elif text == '1*3*3':
    option = "Chapati & beef"
    response = f"END  {phone_number} Your order{option} is confirmed. A confirmation message will be sent to your number"
    response_message = confirmation_message("", option, "350")
    response_to_sms(phone_number, response_message)
  else:
    response = "END Invalid choice you made "

  # Send message

  # Send the response back to the API
  return response

@app.route('/sms_callback', methods=['POST'])
def sms_callback():
    print(request.method)
    print(request.form)
    print(request.form["from"])
    # print("Hello")

    message = "Thank you"
    response_to_sms(request.form["from"], message)
    print(response_to_sms(request.form["from"], message))
    return "Success", 201


SANDBOX_API_KEY = "40120c6927fd58cbcebc5c01045e55b923505ec2be15369eb3c1036811536968"

def response_to_sms(recipient_phone_number, message):
    recipients = [recipient_phone_number]
    message = message
    sender ='3943'

    try:
        # Thats it, hit send and we'll take care of the rest.
        response = sms.send(message, recipients, sender)
        print (response)
    except Exception as e:
        print ('Encountered an error while sending: %s' % str(e))



if __name__ == '__main__':
    app.run(debug=True)