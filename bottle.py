#!/usr/bin/env python
# Created by: Chris Cox
# Project 2
# ECE 4564
# Description: Created a server on the raspberrypiII that is connected to a breadboard via gpio pins
# when a client connects it can light up LEDs on the breadboard based on the message it receives through RabbitMQ.
# Commented out code is from example code.  I left it so i can follow what is happening in the examples.
import socket
import time
from threading import Thread
import RPi.GPIO as GPIO
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='bottle_queue')

# def fib(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n-1) + fib(n-2)

# GPIO pin number of LED according to spec; GPIO pin 18 Phys Pin 12
LED = 12 # Physical pin = 12. GPIO pin = 18
LED = 13 # Physical pin = 13. GPIO pin = 27
LED = 15 # Physical pin = 15. GPIO pin = 22
LED = 16 # Physical pin = 16. GPIO pin = 23

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

FLASH_DELAY = 1 # flash delay in seconds

# This function will be run in the thread.
def flash(is_active):
	c = 0
	while True:
		c = 1-c
		if len(is_active) == 0: # empty list means exit, for our purposes
			GPIO.output(LED,GPIO.LOW) # Turn off LED
			break # jump out of this infinite while loop and exit this thread
		if is_active[0]:
			if c:
				GPIO.output(LED,GPIO.HIGH) # Turn on LED
			else:
				GPIO.output(LED,GPIO.LOW) # Turn off LED
		time.sleep(FLASH_DELAY)


def on_request(ch, method, props, body):
    n = int(body)

    # print " [.] fib(%s)"  % (n,)
    # response = fib(n)
    print '[*] Waiting for messages. To exit press CTRL+C'


    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_request, queue='bottle_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()