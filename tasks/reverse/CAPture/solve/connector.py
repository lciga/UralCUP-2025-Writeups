import re
import base64

def formatstring(inputtext):
    lines = [line.strip() for line in inputtext.strip().splitlines() if line.strip()]

    combined = []
    buffer = ""
    inconcat = False

    for line in lines:
        if not line.endswith('+'):
            stripped = line.strip()
            match_newstr = re.fullmatch(r"new string\('(.?)',\s*(\d+)\),?", stripped)
            if match_newstr:
                char, count = match_newstr.groups()
                part = char * int(count)
                if inconcat:
                    buffer += part
                    combined.append(buffer)
                    buffer = ""
                    inconcat = False
                else:
                    combined.append(part)
                continue

            part = stripped.strip('",')
            if inconcat:
                buffer += part
                combined.append(buffer)
                buffer = ""
                inconcat = False
                continue

            combined.append(part)
            continue

        stripped = line.rstrip('+').strip()
        stripped = stripped.strip('"')
        if inconcat:
            buffer += stripped
        else:
            buffer = stripped
            inconcat = True

    if buffer:
        combined.append(buffer)

    return "".join(combined)


code = '''
"Wk2QAAMAAAAEAAAA//8AALgAAAAAAAAAQ",
        new string('A', 47),
        "sAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAAC9D8va+W6liflupYn5bqWJd3G2if1upYkFTreJ+G6liVJpY2j5bqWJ",
        new string('A', 10),
        "BQRQAATAEEAP5/z2g",
        new string('A', 10),
        "OAADwELAQUMAAIAAAAGAAAAAAAAAEAAAAAQAAAAIAAAAABAAAAQAAAAAgAAB",
        new string('A', 10),
        "E",
        new string('A', 10),
        "BQAAAABAAAAAAAAAIAAAAAABAAABAAAAAAEAAAEAAAAAAAAB",
        new string('A', 10),
        "AAAAAAggAAAo",
        new string('A', 68),
        new string('A', 44),
        "IAAAC",
        new string('A', 31),
        "AAAAAC50ZXh0AAAABgAAAAAQAAAAAgAAAAQ",
        new string('A', 18),
        "CAAAGAucmRhdGEAAFIAAAAAIAAAAAIAAAAG",
        new string('A', 18),
        "BAAABAREFUQQAAAADvAAAAADAAAAACAAAAC",
        new string('A', 19),
        "QAAAwENPREUAAAAAFAAAAABAAAAAAgAAAAo",
        new string('A', 18),
        "EAAAM",
        new string('A', 22),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        "AAAAAP8lACB",
        new string('A', 69),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 48),
        "OCAAAAAAAAAwI",
        new string('A', 13),
        "BGIAAAAC",
        new string('A', 30),
        "OCAAAAAAAACxAU1lc3NhZ2VCb3hBAHVzZXIzMi5kbGwAAAAA",
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 10),
        "BGaW5hbCBTdGFnZQBXZWxjb21lIHRvIHRoZSBGaW5hbCBTdGFnZSEAFjMxGDYmIzYRci8pKxEAVT0VcDMjK0QcOiAcHCdgBhhHGENhUHR1cmVNZQBDYVB0VXJlTWUAQ2FQdHVyRU1lAKMbXH0+Kv8QZwARIjNEVWZ3iJkAQ0FQdHVyZU1lAExBVVRdKzx/agChssPU5fYXKDkAQ2FwdHVyZU1lAP/spyJdEytNb3wAVYvsg+wQagxoEAAAkJCQzMyLRQyJRQQAuAQAAADNIZCQAGNhcHR1cmVtZQBDQVBUVVJFTUUAQ0FQdHVyZW1l",
        new string('A', 72),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 53),
        "GoAaAAwQABoDDBAAGoA6O3P///D",
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 80),
        new string('A', 16)
'''

output = formatstring(code)
