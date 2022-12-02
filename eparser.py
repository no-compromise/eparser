import email, email.parser, sys, os
from prettytable import PrettyTable


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):  # type: ignore
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr


count = 1
t = PrettyTable(["C", "OD", "PRE", "PREDMET", "DÁTUM"])

for filename in os.listdir(os.getcwd() + "/data"):

    try:
        f = open(os.path.join(os.getcwd(), "data/", filename), "r", encoding="utf8")

    except OSError:
        print("Could not open file...bye")
        sys.exit()

    with f:
        msg = email.message_from_file(f)

        frm = header_decode(msg["From"])
        to = header_decode(msg["To"])
        sbj = header_decode(msg["Subject"])
        date = header_decode(msg["Date"])
        t.add_row([count, frm, to, sbj, date])
        count += 1

print(t.get_html_string())

try:
    out = open(os.path.join(os.getcwd(), "out.html"), "w")
except OSError:
    print("Could not create out file!")
    sys.exit()

with out:
    out.write(t.get_html_string(format=True))
