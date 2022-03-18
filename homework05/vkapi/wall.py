import math
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd  # type: ignore
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    code = f"""var i = 0;
    var offset = {offset};
    var response = [];
    while(i < 25) {{
        i = i + 1;
        offset = offset + 100;
        response.push(API.wall.get({{
            "owner_id": "{owner_id}",
            "domain": "{domain}",
            "offset": offset,
            "count": "{count}",
            "filter": "{filter}",
            "extended": "{extended}",
            "fields": "{fields}"
        }}));
    }}
    return response"""
    response = session.post(
        "execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        },
    )
    doc = response.json()
    if not response.ok or "error" in doc:
        raise APIError(doc["error"]["error_msg"])
    return doc["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    if progress is None:
        progress = lambda null: null
    response = pd.DataFrame()
    for pos in progress(range(math.ceil(count / 2500))):
        if pos % 4 == 3:
            time.sleep(1)
        response = response.append(
            json_normalize(
                get_posts_2500(owner_id, domain, offset, count, max_count, filter, extended, fields)
            )
        )
        time.sleep(1)
    return response
