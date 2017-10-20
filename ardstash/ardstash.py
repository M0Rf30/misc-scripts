#!/bin/python2
import serial
import oauth2 as oauth
import json
import urllib
from threading import Timer
import configparser
import os, sys
from daemon import runner


class ArdStash():
    def __init__(self):
        self.stdin_path = '/dev/tty'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/ardstash.pid'
        self.pidfile_timeout = 5
    
    def get_arduino_ip(self):
        arduino_ip = str(urllib.urlopen('http://icanhazip.com').read()).rstrip('\n')
        return arduino_ip
    
    def get_settings(self):
        config = configparser.ConfigParser()
        if not os.path.isfile("/etc/ardstash.conf"):
            print("Config file not found. Please check if /etc/ardstash.conf exists")
            exit()
    
        config.read("/etc/ardstash.conf")
 
        server = "http://" + config.get('stashboard', 'server')
        port = config.get('stashboard', 'port')
        device = config.get('arduino', 'device')
        baud = config.get('arduino', 'baud')
        return (server, port , device, baud)

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    def serialCom(self, device, baud):
        try:
            ser = serial.Serial(self.device, self.baud)
            status = ser.readline().rstrip('\n').rstrip('\r')
            print(status)
        except:
            print("Communication problem with arduino")
        

    def connectToStash(self, arduino_ip, server, port):

# These keys can be found at /admin/credentials
        consumer_key = 'anonymous'
        consumer_secret = 'anonymous'
        oauth_key = 'ACCESS_TOKEN'
        oauth_secret = 'ACCESS_SECRET'

# Create your consumer with the proper key/secret.
# If you register your application with google, these values won't be
# anonymous and anonymous.

        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth.Token(oauth_key, oauth_secret)

# Create our client.
        client = oauth.Client(consumer, token=token)

# Base url for all rest requests
        base_url = server + ":" + port + "/admin/api/v1"

# CREATE a new service
        data = urllib.urlencode({
                "name": arduino_ip,
                "description": "Stato del cestino",
        })
        try:
            resp, content = client.request(base_url + "/services","POST", body=data)
            data = json.loads(content)
        except:
            print("Communication problem with stashboard")
    
    
    #def writeConfig():
    
    #def readConfig():   
     
    
    #def pushToStash():
    def run(self):
        ip = self.get_arduino_ip()
        server, port, device, baud = self.get_settings()
        print(ip)
        print(server)
        print(port)
        print(device)
        print(baud)
        #t = Timer(1, self.serialCom(device, baud))
        #t.start()
        #self.connectToStash(ip, server, port)

ardstash = ArdStash()
daemon = runner.DaemonRunner(ardstash)
daemon.do_action()

