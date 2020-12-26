from node import Node
from constants import Metakey

import yaml

def read_file(filename):
    with open(filename) as f:
        return parse_yaml(
            yaml.load(
                f,
                Loader=yaml.FullLoader
            )
        )

def parse_yaml(data):
    if type(data) is dict:
        return _parse_dict_node(None, data)
    else:
        return Node(subnodes=_parse_yaml_list(data))

def _parse_yaml_list(data):
    return [
        Node(metadata={
            Metakey.name: d,
            Metakey.index: n
        })
        for n, d in enumerate(data)
    ]

def _parse_dict_node(name, data):
    metadata = {}
    if name is not None:
        metadata[Metakey.name] = name

    subnodes = list()

    for key, value in data.items():
        if type(value) is list:
            subnodes = _parse_yaml_list(value)
        elif type(value) is dict:
            subnodes.append(_parse_dict_node(key, value))
        else:
            metadata[key] = value

    return Node(metadata, subnodes)
