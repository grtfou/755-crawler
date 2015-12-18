#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing get talk id and name
"""
from talk_id import get_talk_id


def test_talk_id():
    urls = (
        "http://7gogo.jp/talks/YtykfykuJfMT",
        "http://7gogo.jp/akimoto-manatsu",
        "http://7gogo.jp/talks/Na5Tkpl12wmu",
        "http://7gogo.jp/hori-miona",
        "http://7gogo.jp/magic-prince",
        "http://7gogo.jp/furuhata-nao",
        "http://7gogo.jp/kumazawa-serina"
    )

    for url in urls:
        result = get_talk_id(url)
        print(result)
        assert result != (None, None)
        if result:
            assert result[0][::-1][:2] == '=='
            assert result[1] != ''


def test_error_talk_id():
    url = "http://7gogo.jp/talks/error"

    result = get_talk_id(url)
    assert result == (None, None)
