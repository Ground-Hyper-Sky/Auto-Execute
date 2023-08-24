from mcdreforged.api.utils.serializer import Serializable
from typing import Dict, List


class Path_config:
    config_path: str = './config/AutoExecute.json'
    script_path: str = './Auto_execute_script'


class Default_total_config(Serializable):
    turn_off_auto_execute: bool = False
    auto_execute_list: Dict[str, str] = []
    minimum_permission_level: Dict[str, int] = {
        'create': 2,
        'add': 2,
        'del': 2,
        'remove': 2,
        'look': 2,
        'set': 2,
        'auto_list': 0,
        'list': 0,
        'run': 1,
        'auto': 2,
        'des': 2,
        'permission': 2,
        'kill': 2,
        'insert': 2,
        "re": 2,
        "reload": 2
    }


class Default_script_config(Serializable):
    description: str = ''
    single_permission: int = -1
    command: List[str] = []
