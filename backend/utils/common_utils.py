
def is_json_key_present(json:dict, key:str) -> bool:
    # TODO: Add in common_utils PyPi
    try:
        json[key]
    except KeyError:
        return False

    return True
