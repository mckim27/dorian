#! /usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(order=False)
class PipelineContentsData:
    file_name: str
    contents: str