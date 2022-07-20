def leftPad(length, num):
    return '0' * (length - len(str(num))) + str(num)


def checkSuccessfulLogin(registration_number, server_response):
    # Convert all letters in registration number to uppercase
    registration_number = registration_number.capitalize()
    if server_response.text[3424] == registration_number[0]:
        return True
    else:
        return False
