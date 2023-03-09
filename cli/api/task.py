from typing import Union
import requests
from config import get_config
import utils.auth as auth_utils
cfg = get_config()

def create_task(task_data: dict):
    resp = requests.post(
        cfg.base_url + "/tasks",
        json=task_data,
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp


def get_tasks(
    cats: list,
    start_date: Union[str, None],
    end_date: Union[str, None],
    min_pri: Union[int, None],
    max_pri: Union[int, None],
    tag: str
):
    query_str_obj = {
        "category": cats,
        "start_date": start_date,
        "end_date": end_date,
        "min_pri": min_pri,
        "max_pri": max_pri,
        "tag": tag
    }
    
    resp = requests.get(
        cfg.base_url + "/tasks",
        headers=auth_utils.build_jwt_header(cfg.config_path),
        params=query_str_obj
    )
    return resp
    

def get_tags():
    resp = requests.get(
        cfg.base_url + "/tasks/tags",
        headers=auth_utils.build_jwt_header(cfg.config_path)
    )
    return resp
    