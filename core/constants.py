import random

from backports.strenum import StrEnum


MAX_LENGTH_STANDARD = 124
MAX_LENGTH_PHONE = 12
MAX_LENGTH_ABOUT = 256
MAX_LENGTH_STATUS = 6

ALLOWED_HOSTS_VALIDATION = 'github.com'

PAGINATION_VALUE = 12
AUTOCOMPLETE_LIMIT = 10

STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'

AVATAR_SIZE = 200
AVATAR_FONT_RATIO = 0.7
TEXT_ANCHOR_COORDS = (0, 0)
TEXT_VERTICAL_OFFSET = 10
AVATAR_TEXT_COLOR = '#FFFFFF'


class AvatarColor(StrEnum):
    '''
    Используется StrEnum из backports для совместимости с Python 3.10.
    '''
    RED = '#FF6B6B'
    TEAL = '#4ECDC4'
    BLUE = '#45B7D1'
    GREEN = '#96CEB4'
    YELLOW = '#FFEAA7'
    PURPLE = '#DDA0DD'
    CYAN = '#98D8C8'
    GOLD = '#F7DC6F'
    AMETHYST = '#BB8FCE'
    SKY = '#85C1E2'
    PEACH = '#F8B88B'
    MINT = '#A8E6CF'
    SAND = '#FFD3B5'
    LAVENDER = '#C7CEE6'
    SALMON = '#FFB7B2'

    @classmethod
    def get_random(cls):
        return random.choice(list(cls))
