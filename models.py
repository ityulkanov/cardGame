from dataclasses import dataclass, field


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


@dataclass
class Game:
    users           : list = field(default_factory=list)
    turn_number     : int  = 0
    active_player   : int  = 0
    bank            : int  = 0
    cards           : list = field(default_factory=lambda : [i for i in range(54)])
    cards_availble  : list = field(default_factory=list)
    game_status     : str  = 'wait'

    def user_joined(self, login):
        for user in self.users:
            if user.login == login:
                return True

        return False

    def join_user(self, user):
        self.users.append(user)


class Users:
    def __init__(self):
        # Arseny: Why you use double '_' symbol in name of object attr?
        # Arseny: If you want to create "private" attribute
        # Arseny: You should use `_users`
        # Arseny: `__users` mean that it's a class attribute
        # Arseny: But it's not
        self._users = []

    def __repr__(self):
        return self._users.__repr__()

    def __str__(self):
        return self._users.__repr__()

    def user_exist(self, login):
        for user in self._users:
            if user.login == login:
                return True

        return False

    def add_user(self,login):
        if self.user_exist(login):
            raise LoginException('Login already exist')

        user = User(login=login)
        self._users.append(user)

    def get_user(self,login):
        if not self.user_exist(login):
            return None
        
        for user in self._users:
            if user.login == login:            
                return user




class LoginException(Exception):
    def __init__(self, message):
        super().__init__(message)

        self.message = message
        