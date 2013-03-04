#Shoverbot

## Description
Shoverbot is a quick web servlet using cherrypy that is meant ot be the target of Rackspace Cloud Monitorings webhook alert type. Shoverbot takes the data from the alert and sends it to Prowl to provide push notifications of your Cloud Monitoring Alerts. 

## Requiremetns
Python Module: cherrypy
Python Module: prowlpy
Python Module: json

## Configuration
Complete the config file shoverbot.conf with your resolveable host name, your desired port. It will also ned your prowl api key. The other options are unused at this time.

## Usage
$ ./shoverbot.py 

## ToDo
Build in Verification of the Cloud Monitoring webhook token so shoverbot isnt fooled into sending you unwanted messages. 
