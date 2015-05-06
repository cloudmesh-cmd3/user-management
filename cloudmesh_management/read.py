from pprint import pprint

from mongoengine import *

from user import SubUser, Users
from cloudmesh_management.user import read_user


FILENAME = "/tmp/user.yaml"

connect('user', port=27777)

users = Users()

# Reads user information from file


def main():
    #    user = random_user()
    #    with open(FILENAME, "w") as f:
    #        f.write(user.yaml())


    print 70 * "="
    user = SubUser()
    user = read_user(FILENAME)

    print 70 * "="
    pprint(user.json())
    user.save()

    user.update(**{"set__username": "Hallo"})
    user.save()
    print SubUser.objects(username="Hallo")


if __name__ == "__main__":
    main()
