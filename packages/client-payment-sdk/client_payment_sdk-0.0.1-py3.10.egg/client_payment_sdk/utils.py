from jwcrypto import jws, jwk
from jwcrypto.common import json_encode, json_decode


def dict_to_str(data_dict):
    data_str = ''

    for key in data_dict:
        data_str += f'"{key}":{dict_to_str(data_dict[key])},' if isinstance(data_dict[key], dict) else f'"{key}":"{data_dict[key]}",'

    return '{' + data_str[0:len(data_str)-1] + '}'
