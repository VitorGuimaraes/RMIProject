# -*-coding: utf-8-*-

from threading import Thread
import time
import Pyro4

@Pyro4.expose
# "single" indica que o objeto será compartilhado entre todos os clientes
@Pyro4.behavior(instance_mode = "single") 
class GameServer(object):
	def __init__(self):
		self.players = None
		self.boards = [None] * 2
		self.msg = [None] * 2

	# Define se o jogador vai ser o player1 ou player2
	def you_are_player(self):
		if self.players == None:
			self.players = True
			return 1
		else:
			return 2

	# Recebe e armazena as mensagens enviadas por cada jogador
	def send(self, player, msg):
		print(msg)
		if player == 1:
			if len(msg) == 32:
				self.boards[0] = msg
			else:
				self.msg[0] = msg 
		
		elif player == 2:
			if len(msg) == 32:
				self.boards[1] = msg
			else:
				self.msg[1] = msg  
	
	# Os jogadores vão invocar esse método para adquirir as mensagens do servidor
	def request(self, player, msg):
		if player == 1:
			if msg == "msg":
				return self.msg[1] 

			elif msg == "board":
				return self.boards[1] 

		elif player == 2:
			if msg == "msg":
				return self.msg[0]
			
			elif msg == "board":
				return self.boards[0] 

	# Os jogadores vão invocar esse método para resetar o array que armazenas as mensagens
	def reset_msg_controller(self, player):
		if player == 1:
			self.msg[1] = None 
		
		elif player == 2:
			self.msg[0] = None

def main():
    Pyro4.Daemon.serveSimple(
            {
                GameServer: "ponghau.gameserver"
            },
            ns = True) # True: This tells Pyro to use a name server to register the objects in

if __name__=="__main__":
    main()