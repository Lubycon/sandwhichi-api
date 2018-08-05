from enum import Enum, EnumMeta

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class ProjectMemberRoles(ChoiceEnum):
    # 오너
    # 어드민
    # 멤버
    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'


class RequestStatus(ChoiceEnum):
    # 요청됨
    # 승인됨
    # 거부됨
    REQUESTED = 'Requested'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    CANCELED = 'Canceled'


