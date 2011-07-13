# -*- coding: utf-8 -*-

"""
A simple implementation of a key-insensitive dictionary (implemented by using the pattern decorator).

@authors: U{Ivan Herman<http://www.ivan-herman.net>}, U{Sergio Fernández<http://www.wikier.org>}, U{Carlos Tejo Alonso<http://www.dayures.net>}
@organization: U{World Wide Web Consortium<http://www.w3.org>} and U{Foundation CTIC<http://www.fundacionctic.org/>}.
@license: U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/copyright-software">}
"""

class KeyInsensitiveDict:
    """
    A simple implementation of a key-insensitive dictionary (implemented by using the pattern decorator).
    """

    def __init__(self, d={}):
        self.__dict__["d"] = {}
        for k, v in d.items(): self[k] = v

    def __getattr__(self, attr):
        return getattr(self.__dict__["d"], attr)

    def __setattr__(self, attr, value):
        setattr(self.__dict__["d"], attr, value)

    def __setitem__(self, key, value):
        if (hasattr(key, "lower")):
            key = key.lower()
        self.__dict__["d"][key] = value

    def __getitem__(self, key):
        if (hasattr(key, "lower")):
            key = key.lower()
        return self.__dict__["d"][key]

