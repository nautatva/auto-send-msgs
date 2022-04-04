def merge_iterables(iter1, iter2):
    # TODO: make a function with *args instead of fixed args
    final_list = []
    if iter1 is None:
        return iter2
    if iter2 is None:
        return iter1
    for e in iter1:
        final_list.append(e)
    for e in iter2:
        final_list.append(e)

    return final_list


def is_json_key_present(json:dict, key:str) -> bool:
    # TODO: Add in common_utils PyPi
    try:
        json[key]
    except KeyError:
        return False

    return True
