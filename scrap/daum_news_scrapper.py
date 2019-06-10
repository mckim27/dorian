#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from bs4 import BeautifulSoup


def ex_scrap(raw_html):
    result_text = ''

    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        news_view = soup.find('div', class_='news_view')
        # log.debug(news_view)

        # TODO summary_view 있는 경우 있음.

        text_container = news_view.find('div', id='harmonyContainer')
        # text = text_container.find_all('section')
        re = text_container.find_all("p", attrs={"dmcf-ptype": True})

        for text_block in re:
            #log.debug(text_block.get_text())

            if result_text != '':
                result_text = result_text.strip() + '\n'

            result_text += text_block.get_text().strip() + '\n'

    except Exception as e:
        log.error(e)

    finally:
        return result_text