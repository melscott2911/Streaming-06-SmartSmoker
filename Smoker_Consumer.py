#Mel Scott
#Module6
#Feb_19_2023


import pika
import sys
import os
import time
#import deque module
from collections import deque

#define deque requirement for smoker que
deque_queue1 = deque(maxlen=5)
#Create requirement for alert
queue1_alert = 15

#define variables
host = "localhost"
queue1 = "01-smoker"


def listen_for_tasks():
    
    
    # create a blocking connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # use the connection to create a communication channel
    ch = connection.channel()

    # define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}")
    #function used to sort out smoker deque
    #create string for body
    reading_string=body.decode()
    #Split temp from string
    
    try:
        temp=reading_string.split(",")[1]
        #Add to deque
        deque_queue1.append(float(temp))
        #check to see if the temp has increased by 15
        if deque_queue1 and max(deque_queue1)-min(deque_queue1)>=15:
            print("ALERT: smoker has decreased by 15 degrees or more")
        # acknowledge the message was received and processed 
        # (now it can be deleted from the queue)
    except ValueError:
            pass
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

# define a main function to run the program
def main(hn: str = "localhost", qn: str = "task_queue"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=queue1, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=queue1, on_message_callback=callback, auto_ack=False)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


... 
... 
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", "01-smoker")
