def sort_vers(vers):
    """Sorts versions
    ARGS:
        vers: List of versions
    RETURNS:
        Sorted list"""
    return [k[-1] for k in
            sorted([([int(j) for j in i.split(".")], i) for i in vers])]
