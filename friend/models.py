from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class FriendShip(models.Model):
    from_friend=models.ForeignKey(get_user_model(), related_name="friend_set")
    to_friend=models.ForeignKey(get_user_model(), related_name="to_friend_set")

    def __str__(self):
        return "%s, %s" % (self.from_friend.username, self.to_friend.username)

    class Meta:
        unique_together=(("to_friend", "from_friend"), )