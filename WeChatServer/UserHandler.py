# -*- coding: utf-8 -*-
# filename: UserHandler.py

class UserHandler(object):
    openID = {
        "oHBF6wUHaE4L2yUfhKMBqcrjoi0g": 1,
        "oHBF6wR4kUe4KUNtMMN4J0LKXsPE": 2,
        "oHBF6wTt-wD22eAwEJLVozjcQjxo": 3,
    }

    user_name = {
        "szwlove" : 1,
        "kaarinn" : 2,
    }

    def __init__(self):
        pass

    @staticmethod
    def verify_user(user):
        if UserHandler.openID.get(user, "NoUser") == "NoUSer":
            print("No Such User {0}".format(user))
            return -1
        else:
            return 0