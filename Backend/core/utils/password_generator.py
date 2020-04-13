import random
import string


class PasswordGenerator():

    @staticmethod
    def generate_password(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))
