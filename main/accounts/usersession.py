from django.conf import settings
from .models import UserProfile

class UserSession(object):

    def __init__(self, request):
        self.session = request.session
        usersession = self.session.get(settings.USER_SESSION_ID)
        if not usersession:
            # save an empty cart in the session
            usersession = self.session[settings.USER_SESSION_ID] = {}
        self.usersession = usersession


    def add(self, userprofile):
        userprofile_id = str(userprofile.id)
        if userprofile_id not in self.usersession:
            self.usersession[userprofile_id]
        else:
            self.usersession[userprofile_id]

        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.USER_SESSION_ID] = self.usersession
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True


    

