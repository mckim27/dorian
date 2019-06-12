#! /usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(order=False)
class PipelineContentsData:
    contents: str
    file_name: str