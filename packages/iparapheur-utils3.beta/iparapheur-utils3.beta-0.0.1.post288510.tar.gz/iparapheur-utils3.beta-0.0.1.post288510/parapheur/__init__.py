#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce module est un simple client parapheur
"""
__version__ = "0.0.1-288510"


def getrestclient():
    # We have to define it here, because we use it everywhere in scripts
    from . import parapheur
    return parapheur.getrestclient()


def getsoapclient(user=None, password=None):
    from . import parapheur
    return parapheur.getsoapclient(user, password)