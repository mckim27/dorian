#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
from logzero import logger as log
from form.base_obj import Module


class Cleanser(Module):

    def __init__(self, data):
        super(Cleanser, self).__init__(data)

    def text_length_validation(self):
        contents_length = len(self._data.contents)

        if  contents_length < 40:
            log.debug('too short text... \ntext: {}'.format(self._data.contents))
            self._status = -1
        else:
            log.debug('contents_lengths : {}'.format(contents_length))

        return self

    def hangul_data_validation(self):
        log.debug('hangul_data_validqtion')
        return self

    def remove_special_ch(self):
        c_return = '[^\\n{1}^]'
        hangul = '[^\\n{1}^\\.{1}^\\n^\\sㄱ-ㅣ가-힣]+'
        self._data.contents = re.sub(hangul, '', self._data.contents)
        log.debug('text: {}'.format(self._data.contents))

        return self

    @staticmethod
    def remove_special_ch2(s):
        log.debug('before : {}'.format(s))

        hangul = '[^\\.{1}^\\sㄱ-ㅣ가-힣]+'
        s = re.sub(hangul, '', s)
        s = s.replace('. ', '.\n')

        c_return = '[\n\\s{1,}]'
        # s = re.sub(c_return, '\\n', s)

        return s

    def arrange_return(self):
        log.debug('remove special ch')
        return self


if __name__ == "__main__":
    s = ''

    with open('../pfs/20190622010201003_entertain.txt', 'r') as f:
        s = f.read()

    log.debug('after : {}'.format(Cleanser.remove_special_ch2(s)))
