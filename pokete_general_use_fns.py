"""General use functions for Pokete"""

def liner(text, width, pre=""):
    """Wraps a string after a certain length and respects word endings"""
    lens = 0
    out = ""
    for name in text.split(" "):
        if "\n" in name:
            lens = len(pre)
            out += name + pre
        elif lens+len(name) + 1 <= width:
            out += name + " "
            lens += len(name) + 1
        else:
            lens = len(name) + 1 + len(pre)
            out += "\n" + pre + name + " "
    return out


def hard_liner(l_len, name):
    """Wraps a string after a certain length"""
    ret = ""
    for i in range(int(len(name) / l_len) + 1):
        ret += name[i * l_len:(i + 1) * l_len] + ("\n"
                                                  if i != int(len(name) / l_len)
                                                  else "")
    return ret


def sort_vers(vers):
    """Sorts versions"""
    return [k[-1] for k in
            sorted([([int(j) for j in i.split(".")], i) for i in vers])]


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
