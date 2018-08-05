from enum import Enum, EnumMeta

def get_enum_to_tuple(enum_klass):
    if type(enum_klass) is EnumMeta:
        return [(el, el.value) for el in enum_klass]
    else:
        return []

class RequestStatus(Enum):
    # 요청됨
    # 승인됨
    # 거부됨
    REQUESTED = 'Requested'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'


