from django.utils.text import slugify

def get_private_room_name(user1, user2):
    usernames = sorted([user1.lower(), user2.lower()])
    return f"dm_{slugify(usernames[0])}_{slugify(usernames[1])}"

