from enum import Enum, EnumMeta

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

class RequestStatus(ChoiceEnum):
    # 요청됨
    # 승인됨
    # 거부됨
    REQUESTED = 'Requested'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    CANCELED = 'Canceled'


