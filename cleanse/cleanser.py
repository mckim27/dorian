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
        text = self._data.contents

        try:
            # 한글이 아닌 것, '.' 이 아닌 것, 's' 공백이 아닌 것 일단 삭제
            not_hangul = '[^\\n^\\.{1}^\\sㄱ-ㅣ가-힣]+'
            text = re.sub(not_hangul, '', text)

            # '. ' 인 것들 '.' + 개행 으로 변경.
            text = re.sub('\\. +', '.\n', text)

            # '..' 두개 이상 인것들 삭제.
            text = re.sub('\\.{2,}', '', text)

            # 공백 두개 이상인것 하나로 변경.
            text = re.sub(' {2,}', ' ', text)

            text = re.sub('\n ', '\n', text)

            # 개행 두개 이상인것 하나로 변경.
            text = re.sub('\n{2,}', '\n', text)

            log.debug('### after text : {}'.format(text))
        except Exception as e:
            log.error('check string : {}'.format(text))
            raise e

        return self

    @staticmethod
    def test_remove_special_ch(s):
        text = s

        log.debug('before : {}'.format(text))

        try:
            # 한글이 아닌 것, '.' 이 아닌 것, 's' 공백이 아닌 것 일단 삭제
            not_hangul = '[^\\n^\\.{1}^\\sㄱ-ㅣ가-힣]+'
            text = re.sub(not_hangul, '', text)

            # '. ' 인 것들 '.' + 개행 으로 변경.
            text = re.sub('\\. +', '.\n', text)

            # '..' 두개 이상 인것들 삭제.
            text = re.sub('\\.{2,}', '', text)

            # 공백 두개 이상인것 하나로 변경.
            text = re.sub(' {2,}', ' ', text)

            text = re.sub('\n ', '\n', text)

            # 개행 두개 이상인것 하나로 변경.
            text = re.sub('\n{2,}', '\n', text)

            log.debug('### after text : {}'.format(text))
        except Exception as e:
            log.error('check string : {}'.format(text))
            raise e

        return text

    def arrange_return(self):
        log.debug('remove special ch')
        return self


if __name__ == "__main__":
    s = None

    with open('../pfs/20190622010201003_entertain.txt', 'r') as f:
        s = f.read()

    out = Cleanser.test_remove_special_ch(s)

    log.debug('after : {}'.format(out))

    with open('test.txt', mode='wt', encoding='utf-8') as f:
        f.write(out)


