import random
from dataclasses import dataclass, field
from itertools import cycle


class Users:
    def __init__(self):
        self._users = []


    @property
    def all_users(self):
        return self._users
    
    @property
    def users_count(self):
        return len(self._users)

    @property
    def users_circle(self):
        return cycle(self._users)
    

    def __repr__(self):
        return self._users.__repr__()

    def __str__(self):
        return self._users.__repr__()

    def __iter__(self):
        return (user for user in self._users)

    def __getitem__(self, index):
        return self._users[index]


    def user_exist(self, login):
        for user in self._users:
            if user.login == login:
                return True

        return False

    def add_user(self, user):
        if self.user_exist(user.login):
            raise LoginException('Login already exist')

        self._users.append(user)

    def get_user(self,login):
        if not self.user_exist(login):
            return None
    
        for user in self._users:
            if user.login == login:            
                return user

    def get_prev_user(self, user):
        while True:
            prev_user = next(self.users_circle)
            iter_user = next(self.users_circle)
            if iter_user == user:
                return prev_user


@dataclass
class User:
    login   : str
    cards   : list  = field(default_factory=list)
    money   : int   = 1000
    bet     : int   = 0
    position: int   = None
    actions : list  = field(default_factory=list)
    action  : str   = None
    ready   : bool  = False
    role    : str   = None

    def __eq__(self, user):
        if self.login == user.login:
            return True
        else:
            return False


@dataclass
class Game:
    users           : Users = Users()
    blind           : int  = 50 
    turn_number     : int  = 0
    active_player   : int  = 0
    actual_bet      : int  = 0
    bank            : int  = 0
    cards           : list = field(default_factory=lambda : [i for i in range(54)])
    cards_availble  : list = field(default_factory=list)
    game_status     : str  = 'wait'
    
    def user_joined(self, login):
        return self.users.user_exist(login)

    def join_user(self, user):
        if self.game_status == 'ON':
            raise Exception('game already started')

        if len(self.users.all_users) != 0:
            max_pos = self.users.all_users[-1].position
            if max_pos == 6:
                raise Exception('game is full')
        else:
            max_pos = 0

        user.position = max_pos + 1
        self.users.add_user(user)

    def all_users_ready(self):
        for user in self.users:
            if not user.ready:
                return False

        return True

    def start_turn(self):
        self.turn_number += 1
        self.game_status = 'ON'
        
        if self.turn_number == 1:
            self.__deal_cards()
        elif self.turn_number == 2:
            self.__deal_flop()

        self.__switch_blinds()

    def next_player(self):
        if self.__check_bets():
            self.__get_bets()
            self.start_turn()

        if self.active_player == self.users.users_count:
            self.active_player = 1
        else:
            self.active_player += 1

    def __switch_blinds(self):
        if self.turn_number == 1:
            self.users[0].role = 'small blind'
            self.users[0].bet  = self.blind
            self.users[1].role = 'big blind'
            self.users[1].bet  = self.blind * 2
            self.actual_bet = self.blind * 2
        else:
            for user in self.users.users_circle:
                if user.role == 'big blind':
                    user.role = 'small blind'
                    user.bet = self.blind
                    user = next(self.users.users_circle)
                    user.role = 'big blind'
                    user.bet = self.blind * 2
                    self.actual_bet = self.blind * 2
                    break
        self.__set_active_player()

    def __deal_cards(self):
        for user in self.users:
            for i in range(2):
                random_card_num = random.randrange(len(self.cards))
                random_card = self.cards.pop(random_card_num)
                user.cards.append(random_card)

    def __deal_flop(self):
        random_card_num = random.randrange(len(self.cards))
        self.cards.pop(random_card_num)
        for i in range(3):
            random_card_num = random.randrange(len(self.cards))
            random_card = self.cards.pop(random_card_num)
            self.cards_availble.append(random_card)

    def __set_active_player(self):
        for user in self.users.users_circle:
            if user.role == 'big blind':
                user = next(self.users.users_circle)
                self.active_player = user.position
                break

    def __check_bets(self):
        for user in self.users:
            if user.bet != self.actual_bet:
                return False

        return True

    def __get_bets(self):
        for user in self.users:
            self.bank += user.bet
            user.money -= user.bet
            user.bet = 0


class LoginException(Exception):
    def __init__(self, message):
        super().__init__(message)

        self.message = message
        