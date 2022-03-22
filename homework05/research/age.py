import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    time = dt.date.today()
    age_of_people = []
    list_of_friends = get_friends(user_id, fields=["bdate"]).items
    for friend in list_of_friends:
        try:
            bdate = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")  # type: ignore
        except:
            continue
        age_of_people.append(
            time.year
            - bdate.year
            - (time.month < bdate.month or (time.month == bdate.month and time.day < bdate.day))
        )

    if age_of_people:
        return statistics.median(age_of_people)
    else:
        return None
