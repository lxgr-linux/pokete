def liner(text, width, pre=""):
    """Wraps a string after a certain length and respects word endings
    ARGS:
        text: The text that should be lined
        width: The max width
        pre: Prefix that will be added in the next line
    RETURNS:
        The lined string"""
    lens = 0
    out = ""
    for name in text.split(" "):
        if "\n" in name:
            lens = len(pre)
            out += name + pre
        elif lens + len(name) + 1 <= width:
            out += name + " "
            lens += len(name) + 1
        else:
            lens = len(name) + 1 + len(pre)
            out += "\n" + pre + name + " "
    return out


def hard_liner(l_len, name):
    """Wraps a string after a certain length
    ARGS:
        name: The String
        l_len: The max length
    RETURNS:
        The lined string"""
    ret = ""
    for i in range(int(len(name) / l_len) + 1):
        ret += name[i * l_len:(i + 1) * l_len] + ("\n"
                                                  if i != int(len(name) / l_len)
                                                  else "")
    return ret
