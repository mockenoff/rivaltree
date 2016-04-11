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

import copy
import simplejson as json

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from django.conf import settings
from apps.bracketr import models

def get_diff(old_bracket, new_bracket):
	""" Find updated games in a new bracket compared to an old bracket

	:param old_bracket: Old bracket
	:type old_bracket: dict
	:param new_bracket: New bracket
	:type new_bracket: dict
	:returns: list

	"""
	games = []
	old_games = {}
	new_games = {}

	if not isinstance(old_bracket, dict):
		old_bracket = {}
	else:
		old_bracket = copy.deepcopy(old_bracket)

	if not isinstance(new_bracket, dict):
		new_bracket = {}
	else:
		new_bracket = copy.deepcopy(new_bracket)

	for key in ('round_robin', 'winners', 'losers', 'winner_loser'):
		if key in old_bracket:
			for row in old_bracket[key]:
				for game in row:
					game['type'] = key
					old_games[game['id']] = game

		if key in new_bracket:
			for row in new_bracket[key]:
				for game in row:
					game['type'] = key
					new_games[game['id']] = game

	for game_id in new_games:
		if game_id not in old_games or new_games[game_id] != old_games[game_id]:
			games.append(new_games[game_id])

	return games

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
		""" Callback for whenever the server gets a message

		SUB message - {'type': 'SUB', 'bracket_id': 'bracket_id'}
		PUB message - {'type': 'PUB', 'bracket_id': 'bracket_id', 'bracket': {...}}

		"""
		if is_binary:
			print('Binary message received: {} bytes'.format(len(payload)), self.http_request_path)
		else:
			print('Text message received: {}'.format(payload.decode('utf8')), self.http_request_path)
			data = json.loads(payload.decode('utf8'))

			if data['type'] == 'SUB':
				print('SUB', data['bracket_id'])
				self.factory.subscribe(data['bracket_id'], self)
				self.sendMessage(json.dumps({
					'type': 'SUB',
					'did_subscribe': True,
					'bracket_id': data['bracket_id'],
				}).encode('utf8'), False)

			elif data['type'] == 'PUB':
				print('PUB', data['bracket_id'])

				# TODO: Figure out the diff between last_updates[bracket_id] and data[bracket]
				games = get_diff(
					self.factory.last_updates[data['bracket_id']]
					if data['bracket_id'] in self.factory.last_updates
					else None,
					data['bracket'])
				self.factory.last_updates[data['bracket_id']] = data['bracket']

				self.factory.broadcast(json.dumps({
					'type': 'PUB',
					'games': games,
					'bracket_id': data['bracket_id'],
				}), data['bracket_id'])

				self.sendMessage(json.dumps({
					'type': 'PUB',
					'did_publish': True,
					'bracket_id': data['bracket_id'],
				}).encode('utf8'), False)

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
		self.last_updates = {}

	def register(self, client):
		print('registered client {}'.format(client.peer))
		if client not in self.clients:
			self.clients.append(client)

	def unregister(self, client):
		print('unregistered client {}'.format(client.peer))
		try:
			client_index = self.clients.index(client)
			del self.clients[client_index]
			for bracket_id in self.brackets:
				self.brackets[bracket_id].remove(client_index)
				if not self.brackets[bracket_id] and bracket_id in self.last_updates:
					del self.last_updates[bracket_id]
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

	def broadcast(self, message, bracket_id=None):
		""" Sends a message to multiple clients

		:param message: The message to broadcast
		:type message: str
		:param bracket_id: If supplied, will only broadcast to clients subscribed to that bracket
		:type bracket_id: str

		"""
		if not bracket_id:
			print('broadcasting message \'{}\' ..'.format(message))
			for client in self.clients:
				client.sendMessage(message.encode('utf8'))
				print('message sent to {}'.format(client.peer))
		elif bracket_id in self.brackets:
			print('publishing message \'{}\' ..'.format(message))
			for client_index in self.brackets[bracket_id]:
				try:
					self.clients[client_index].sendMessage(message.encode('utf8'))
					print('message sent to {}'.format(self.clients[client_index].peer))
				except IndexError:
					print('client_index {} not found in clients'.format(client_index))


if __name__ == '__main__':
	factory = ServerFactory(u'ws://127.0.0.1:%s' % settings.WS_PORT)
	factory.protocol = ServerProtocol

	print('Starting WebSocket server at ws://127.0.0.1:%s' % settings.WS_PORT)
	print('Quit the server with CONTROL-C.')

	reactor.listenTCP(9000, factory)
	reactor.run()
