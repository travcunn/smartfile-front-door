from app.models import User


class LoginValidator(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    @property
    def is_valid(self):
        user = self.lookup_user
        if user is None:
            return False

        if not user.check_password(self.__password):
            return False

        return True

    @property
    def lookup_user(self):
        user = User.query.filter_by(username=self.__username).first()
        return user
