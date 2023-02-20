"""
 
This program creates a producer and multiple task queues (RabbitMQ).
It reads data from the smoker-temps.csv file for smart smokers.

Author: Mel Scott
February 12, 2023
Streaming Data- Module 05 Assignment

"""

import pika
import socket
import sys
import csv
import time
import webbrowser

#Defined my Variables
show_offer= False
sleep_time = 30
input_file_name = "/Users/mel/Documents/Streaming-Data/Module-5-Smart-Smoker-1/smoker-temps.csv"

#Trigger Rabit MQ admin page if True

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()
            
# define csv file and queues
input_file = open("smoker-temps.csv", "r")
queue1 = "01-smoker"
queue2 = "02-food-A"
queue3 = "02-food-B"

## define the messages to be sent to queues
def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.
    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a  server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # Enabling 3 different queues
        ch.queue_delete(queue1)
        ch.queue_delete(queue2)
        ch.queue_delete(queue3)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message} on {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# This allows us to import this module and use its functions without executing the code below.
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    if show_offer == True:
        offer_rabbitmq_admin_site()

# define csv reader and set up messages for queue
# use an enumerated type to set the address family to (IPV4) for internet
socket_family = socket.AF_INET 

# use an enumerated type to set the socket type to UDP (datagram)
socket_type = socket.SOCK_DGRAM 

# use the socket constructor to create a socket object we'll call sock
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# create a csv reader for our comma delimited data
reader = csv.reader(input_file, delimiter=",")

for row in reader:
    for row in reader:
    # read a row from the file
        Time, Channel1, Channel2, Channel3 = row

# send message to queue1 from Channel1
        try:

    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
            fstring_message = f"[{Time}, {Channel1}]"
    
    # prepare a binary (1s and 0s) message to stream
            message = fstring_message.encode()

    # use the socket sendto() method to send the message
            send_message("localhost","queue1",message)
            print (f"Sent: {message} on queue1")

        except ValueError:
            pass

 # send message to queue1 from Channel2
        try:

    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
            fstring_message = f"[{Time}, {Channel2}]"
    
    # prepare a binary (1s and 0s) message to stream
            message = fstring_message.encode()

    # use the socket sendto() method to send the message
            send_message("localhost","queue2",message)
            print (f"Sent: {message} on queue2")

        except ValueError:
            pass

# send message to queue1 from Channel3
        try:

    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
            fstring_message = f"[{Time}, {Channel3}]"
    
    # prepare a binary (1s and 0s) message to stream
            message = fstring_message.encode()

    # use the socket sendto() method to send the message
            send_message("localhost","queue3",message)
            print (f"Sent: {message} on queue3")

        except ValueError:
            pass

# sleep for a few seconds
        time.sleep(30)



# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    show_offer=True
    offer_rabbitmq_admin_site(show_offer)
    # get the message from the command line
    # if no arguments are provided, use the default message
    # use the join method to convert the list of arguments into a string
    # join by the space character inside the quotes
    message = " ".join(sys.argv[1:]) or "Smart Smoker BBQ Producer"
    # send the message to the queue
    send_message("localhost","queue1",message)
