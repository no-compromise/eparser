import email, email.parser, sys, os, string, random, zipfile
from prettytable import PrettyTable


outfile = "out.html"
style = "<style>td {font-size: small; border-bottom: 1px solid;} th {border-bottom: 2px solid}</style>\n"


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):  # type: ignore
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr


def randfilename(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size)) + ".eml"


count = 1
t = PrettyTable(["#", "FILE", "OD", "PRE", "PREDMET", "DÁTUM"])

print(f'Vidím tu celkovo: {len(os.listdir(os.getcwd() + "/data"))} súbory')
if not input("Je to OK? (A/N): ") == "A":
    print("Končím...")
    sys.exit()

z = zipfile.ZipFile("./complet/archive.zip", "w")

for filename in os.listdir(os.getcwd() + "/data"):
    print(f"Spracovávam súbor: {filename}", end=" ")
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
        filen = randfilename(8)
        t.add_row([count, filen, frm, to, sbj, date])
        count += 1
        print(" OK!")
    z.write(os.path.join(os.getcwd(), "data/", filename), arcname=filen)
z.close()
print("Emaily uložené do ZIP archivu")


try:
    print(f"Ukladám zoznam do {outfile}")
    out = open(os.path.join(os.getcwd(), "complet/", outfile), "w")
except OSError:
    print("Could not create out file!")
    sys.exit()

with out:
    outtext = style + t.get_html_string(format=True)
    out.write(outtext)
