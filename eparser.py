import email
import sys


try:
    f = open("./data/email.eml", "r", encoding="utf8")

except OSError:
    print("Could not open file...bye")
    sys.exit()

with f:
    msg = email.message_from_file(f)
    print(msg["From"])
    print(msg["To"])
