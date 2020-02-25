from facial_authentication import isAuthenticated
from email_automation import sendAlertMail
from drowsiness_detection import drowsyCheck

def checkAuthorization():
    name, authValue = isAuthenticated()
    if authValue:
        print(f'Hi {name}, Welcome aboard...!')
    else:
        print("Anonymous User")
        sendAlertMail()

if __name__ == "__main__":
    checkAuthorization()
    drowsyCheck()