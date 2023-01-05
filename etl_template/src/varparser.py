import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append("..")


def vars_parse_last_modified(string_process, last_modified=None):
    if last_modified is not None:
        return string_process.replace("$modified_last", last_modified)
    else:
        return string_process


def vars_parse_batch_size(string_process):
    return string_process.replace("$batch_size", str(os.environ.get("BATCH_SIZE")))


def vers_parse_list_id(string_process, list_id=None):
    if list_id is not None:
        if len(list_id) > 0:
            list_id_str = ",".join(f"'{str(x)}'" for x in list_id)
        else:
            list_id_str = "'00000000-0000-0000-0000-000000000000'"
        return string_process.replace("$list_id", list_id_str)
    else:
        return string_process
