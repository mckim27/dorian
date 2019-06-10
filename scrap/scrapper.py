#! /usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Scrapper(ABC) :

    @abstractmethod
    def scrap(self):
        pass
