#!/usr/bin/env python

#   Copyright 2013 Joshua Bell
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cherrypy
import ConfigParser
import logging
import json as simplejson
import sys
import prowlpy

Config=ConfigParser.ConfigParser()
Config.read("shoverbot.conf")

serverconfig = {'server.socket_host': Config.get('webserver', 'host'),
                'server.socket_port': Config.getint('webserver', 'port'),
                'log.screen': True
               }

with open('/tmp/shoverbot.out', 'a') as logfile:
    logfile.write('Starting Shoverbot Run\n')

class ShoverBot:

    prowl = prowlpy.Prowl(Config.get('keys', 'prowl_api_key'))

    def index(self):
        msg = 'ShoverBot Active!'
        cherrypy.log(msg, context='', severity=logging.DEBUG, traceback=False)
        token_sent = cherrypy.request.headers['X-RACKSPACE-WEBHOOK-TOKEN']
        cl = cherrypy.request.headers['CONTENT-LENGTH']
        rawbody = cherrypy.request.body.read(int(cl))
        body = simplejson.loads(rawbody)
        msg = 'request body:\n'
        cherrypy.log(msg, context='', severity=logging.DEBUG, traceback=False)
        if body.has_key('entity'):
            entity_msg = 'entity name: ' + body['entity']['label']
            cherrypy.log(entity_msg, context='', severity=logging.DEBUG, traceback=False)
            print('entity name: {0}').format(body['entity']['label'])
        else: 
            entity_msg = 'entity name: not found'
            cherrypy.log(entity_msg, context='', severity=logging.DEBUG, traceback=False)
            print('entity name: not fround')

        try:
            self.prowl.add('Cloud Monitoring ShoverBot','Server: ' + body['entity']['label'],'State: ' + body['details']['state'] + ' Status: ' + body['details']['status'], 1, None, "http://www.rackspace.com/cloud/public/monitoring/")
            print('Success - sent prowl message\n')
        except Exception,msg:
            print(msg)

        return "Updated %r." % (body,)

    index.exposed = True


cherrypy.config.update(serverconfig)

cherrypy.quickstart(ShoverBot())
