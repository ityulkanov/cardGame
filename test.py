# Arseny: when you write tests the good practice is
# Arseny: using the `pytest` lib or the `unittest` lib
import unittest
from typing import Any, Tuple

from server import index, login, create_game, join_game
from models import User, Users, Game

