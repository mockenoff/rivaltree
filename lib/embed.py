"""
.. module:: embed
   :platform: Unix
   :synopsis: Web socket server via Autobahn

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

# Establish paths

import sys, os
sys.path.insert(0, '/Users/timothypoon/.pyenv/versions/rivaltree/bin/python')
sys.path.append('/mockenoff/rivaltree')
os.chdir('/mockenoff/rivaltree')
os.environ['DJANGO_SETTINGS_MODULE'] = 'deployment.settings'

# Let Djago do its thing

import django
django.setup()

# Now the non-meta code

import simplejson as json

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from django.conf import settings
from apps.bracketr import models

class ServerProtocol(WebSocketServerProtocol):
	def onConnect(self, request):
		print('Client connecting: {}'.format(request.peer))
		if settings.WS_BASE and not request.path.startswith(settings.WS_BASE):
			self.doClose = True
		else:
			self.doClose = False

	def onOpen(self):
		print('WebSocket connection open.')
		if self.doClose:
			self.sendMessage(json.dumps({
				'type': 'ERR',
				'data': 'Cannot connect to invalid path',
			}), False)
			self.sendClose()
		else:
			self.factory.register(self)

	def onMessage(self, payload, is_binary):
		# SUB message - {'type': 'SUB', 'bracket_id': 'bracket_id'}
		# PUB message - {'type': 'PUB', 'bracket_id': 'bracket_id', 'bracket': {...}}
		if is_binary:
			print('Binary message received: {} bytes'.format(len(payload)), self.http_request_path)
		else:
			print('Text message received: {}'.format(payload.decode('utf8')), self.http_request_path)
			# data = json.loads(payload.decode('utf8'))
			# if data['type'] == 'SUB':
				# self.factory.subscribe(data['bracket_id'], self)
				# self.sendMessage(json.dumps({...}), False)
			# elif data['type'] == 'PUB':
				# self.factory.broadcast(json.dumps({...}), data['bracket_id'])

	def connectionLost(self, reason):
		print('WebSocket connection lost: %s' % reason)
		WebSocketServerProtocol.connectionLost(self, reason)
		self.factory.unregister(self)

	def onClose(self, was_clean, code, reason):
		print('WebSocket connection closed: {}'.format(reason))


class ServerFactory(WebSocketServerFactory):
	def __init__(self, url):
		WebSocketServerFactory.__init__(self, url)
		self.clients = []
		self.brackets = {}

	def register(self, client):
		print('registered client {}'.format(client.peer))
		if client not in self.clients:
			self.clients.append(client)

	def unregister(self, client):
		print('unregistered client {}'.format(client.peer))
		try:
			client_index = self.clients.index(client)
			self.clients.remove(client)
			for bracket_id in self.brackets:
				self.brackets[bracket_id].remove(client_index)
		except ValueError:
			pass

	def subscribe(self, bracket_id, client):
		print('subscribe client %s to %s' % (client.peer, bracket_id))
		if client not in self.clients:
			self.register(client)
		if bracket_id not in self.brackets:
			self.brackets[bracket_id] = set()
		self.brackets[bracket_id].add(self.clients.index(client))

	def unsubscribe(self, bracket_id, client):
		print('unsubscribe client %s from %s' % (client.peer, bracket_id))
		try:
			self.brackets[bracket_id].remove(self.clients.index(client))
		except (ValueError, KeyError):
			pass

	def broadcast(self, msg, bracket_id=None):
		print('broadcasting message \'{}\' ..'.format(msg))
		if bracket_id and bracket_id in self.brackets:
			pass
		else:
			for client in self.clients:
				client.sendMessage(msg.encode('utf8'))
				print('message sent to {}'.format(client.peer))


if __name__ == '__main__':
	factory = ServerFactory(u'ws://127.0.0.1:%s' % settings.WS_PORT)
	factory.protocol = ServerProtocol

	print('Starting WebSocket server at ws://127.0.0.1:%s' % settings.WS_PORT)
	print('Quit the server with CONTROL-C.')

	reactor.listenTCP(9000, factory)
	reactor.run()
