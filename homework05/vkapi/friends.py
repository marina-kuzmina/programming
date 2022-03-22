import dataclasses
import math
import time
import typing as tp

from vkapi import config, session
from vkapi.exceptions import APIError

from vkapi.config import VK_CONFIG
from vkapi.session import Session

session = Session(VK_CONFIG["domain"])

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    session = Session(VK_CONFIG["domain"])
    response = session.get(
        "friends.get",
        params={
            "user_id": user_id,
            "count": count,
            "offset": offset,
            "fields": fields,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        },
    ).json()["response"]
    return FriendsResponse(count=response["count"], items=response["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    session = Session(VK_CONFIG["domain"])

    list_of_mutualfriends = []

    if target_uids:
        for t_u in range(((len(target_uids) - 1) // 100) + 1):
            try:
                mutual_friends = session.get(
                    "friends.getMutual",
                    params={
                        "access_token": access_token,
                        "v": v,
                        "source_uid": source_uid,
                        "target_uid": target_uid,
                        "target_uids": ",".join(list(map(str, target_uids))),
                        "order": order,
                        "count": 100,
                        "offset": t_u * 100,
                    },
                )
                for friend in mutual_friends.json()["response"]:
                    list_of_mutualfriends.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
            except:
                pass
            time.sleep(0.38)
        return list_of_mutualfriends

    try:
        parm = {
            "access_token": access_token,
            "v": v,
            "source_uid": source_uid,
            "target_uid": target_uid,
            "target_uids": target_uids,
            "order": order,
            "count": count,
            "offset": offset,
        }
        mutual_friends = session.get("friends.getMutual", params=parm)
        list_of_mutualfriends.extend(mutual_friends.json()["response"])

    except:
        pass
    return list_of_mutualfriends


if __name__ == "__main__":
    print(get_mutual(274205023, 289180780))
    print(get_mutual(274205023, target_uids=[133985865, 289180780, 145904017]))  # общие друзья
