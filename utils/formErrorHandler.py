import re


def formErrorHandler(message):
    """ if message.author == self.user:
            return """
    if len(message) > 255:
        return [False, "Please do not use more than 255 characters"]

    if re.match('^[-\w\s.]*$', message) is None:
        return [False, "Please do not use special characters"]

    """ if m.channel != message.channel:
        return [False, "We have no idea what is happening"] """

    return [True, message]


def checkIfError(message):

    if len(message) > 255:
        return False
    if re.match('^[-\w\s.]*$', message) is None:
        return False

    return True
