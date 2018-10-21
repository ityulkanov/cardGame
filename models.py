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
    cards           : list = field(default_factory=list)
    cards_availble  : list = field(default_factory=list)
    game_status     : str  = 'wait'
    
    @property
    def active_player_count(self):
        count = 0
        for user in self.users:
            if user.action != 'fold':
                count += 1
        return count

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
        self.actual_bet = 0
        self.__reload_user_actions()

        if self.turn_number == 1:
            self.cards_availble = []
            self.__reload_cards()
            self.__deal_cards()
            self.__switch_blinds()
        elif self.turn_number == 2:
            self.__deal_flop()
        elif self.turn_number == 3:
            self.__deal_kicker()
        elif self.turn_number == 4:
            self.__deal_river()

    def next_player(self):
        users_circle = self.users.users_circle
        #в первом цикле ищем активного игрока
        for user in users_circle:
            if user.position == self.active_player:
                #когда его нашли, продолжаем искать по кругу игрока который не фолданул
                for next_user in users_circle:
                    if next_user.action != 'fold':
                        self.active_player = next_user.position
                        break
                break

        if self.__check_bets():
            self.__get_bets()
            if self.active_player_count > 1:
                self.start_turn()
            else:
                self.turn_number = 0
                self.actual_bet = 0
                user = self.users[self.active_player - 1]
                user.money += self.bank
                self.bank = 0
                self.start_turn()

    def __switch_blinds(self):
        if self.game_status == 'wait':
            self.game_status = 'on'
            self.users[0].role = 'small blind'
            self.users[0].bet  = self.blind
            self.users[0].action = 'bet done'
            self.users[1].role = 'big blind'
            self.users[1].bet  = self.blind * 2
            self.users[1].action = 'bet done'
            self.actual_bet = self.blind * 2
            try:
                self.users[2]
                self.active_player = 3
            except IndexError:
                self.active_player = 1
        else:
            users_circle = self.users.users_circle
            for user in users_circle:
                if user.role == 'big blind':
                    user.role = 'small blind'
                    user.bet = self.blind
                    user.action = 'bet done'
                    print(user)
                    user = next(users_circle)
                    user.role = 'big blind'
                    user.bet = self.blind * 2
                    user.action = 'bet done'
                    self.actual_bet = self.blind * 2
                    print(user)
                    user = next(users_circle)
                    print(user)
                    self.active_player = user.position
                    break

    def __reload_cards(self):
        self.cards = [i for i in range(52)]
        random.shuffle(self.cards)
        for user in self.users:
            user.cards = []

    def __deal_cards(self):
        for user in self.users:
            for i in range(2):
                user.cards.append(self.cards.pop())

    def __deal_flop(self):
        #верхнюю карту просто сбрасывают
        self.cards.pop()
        for i in range(3):
            self.cards_availble.append(self.cards.pop())

    def __deal_kicker(self):
        #верхнюю карту просто сбрасывают
        self.cards.pop()
        self.cards_availble.append(self.cards.pop())

    def __deal_river(self):
        #верхнюю карту просто сбрасывают
        self.cards.pop()
        self.cards_availble.append(self.cards.pop())

    def __reload_user_actions(self):
        for user in self.users:
            user.action = 'waiting'

    def __check_bets(self):
        for user in self.users:
            if (user.bet != self.actual_bet and user.action != 'fold') or \
               user.action == 'waiting':
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
        