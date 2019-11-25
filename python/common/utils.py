import datetime
import hashlib
import time
from flask import request
from pytz import timezone

from .code import CODE_MSG_MAP

from config import SERVER_ID, RELEASE, ENVIRONMENT


def pretty_result(code, msg=None, start_time=datetime.datetime.now(), data=None):
    if msg is None:
        msg = CODE_MSG_MAP.get(code)

    return {
        'auditData': {
            'requestHost': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            'serverId': SERVER_ID,
            'environment': ENVIRONMENT,
            'release': RELEASE,
            'processTime': time.time() - start_time,
            'timestamp': datetime.datetime.now().astimezone(timezone('UTC')).isoformat(),
        },
        'code': code,
        'msg': msg,
        'data': data
    }


def hash_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def get_zodiac(month, day):
    zodiac = (
        '摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座',
        '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座'
    )
    date = (
        (1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22),
        (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23)
    )
    return zodiac[len(list(filter(lambda x: x <= (month, day), date))) % 12]


def get_age(year, month, day):
    now = datetime.datetime.now()
    now_year, now_month, now_day = now.year, now.month, now.day

    if year >= now_year:
        return 0
    elif month > now_month or (month == now_month and day > now_day):
        return now_year - year - 1
    else:
        return now_year - year
