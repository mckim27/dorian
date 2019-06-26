#! /usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from form.base_obj import Module
from logzero import logger as log


class Scrapper(Module):

    def __init__(self, data):
        super(Scrapper, self).__init__(data)

    def scrap_daumnews_article_contents(self):
        result_text = ''

        soup = BeautifulSoup(self._data.contents, 'html.parser')
        news_view = soup.find('div', class_='news_view')

        if news_view is None:
            log.warn('target object not exist ...')
            log.warn('check below html')
            log.warn(self._data.contents)
            self._status = -1
            return self

        text_container = news_view.find('div', id='harmonyContainer')
        # text = text_container.find_all('section')
        re = text_container.find_all("p", attrs={"dmcf-ptype": True})

        for text_block in re:
            # log.debug(text_block.get_text())

            if result_text != '':
                result_text = result_text.strip() + '\n'

            result_text += text_block.get_text().strip() + '\n'

        log.debug("result scrap file_name : " + self._data.file_name)
        log.debug("result scrap text : " + result_text)

        if result_text.strip() == '':
            log.warn('result scrap text is empty ...')
            self._status = -1
            return self

        self._data.contents = result_text
        self._data.file_name = self._data.file_name

        log.info('scrap_daumnews_article_contents func end.')

        return self