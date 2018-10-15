from client import Client

cl1 = Client()
cl2 = Client()

cl1.log_in('user_1')
cl2.log_in('user_2')

cl1.create_game()
cl2.join_game()

cl1.ready()
cl2.ready()
