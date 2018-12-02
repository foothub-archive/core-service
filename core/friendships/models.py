from generics.models import Invitation


class FriendshipInvitation(Invitation):
    def resolve(self, resolution):
        assert False


class Friendship:
    pass
