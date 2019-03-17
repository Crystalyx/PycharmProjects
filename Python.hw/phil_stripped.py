#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote
from urllib.parse import unquote
from urllib.error import URLError, HTTPError
import re
import copy

"""
Функция возвращает содержимое вики-страницы name из русской Википедии.
В случае ошибки загрузки или отсутствия страницы возвращается None.
"""


def get_content(name):
    try:
        url = ("https://ru.wikipedia.org/wiki/" + quote(name))
        page = ''
        with urlopen(url) as site:
            for line in site:
                page += unquote(line.decode('utf-8'))[0:-1]
        return page
    except URLError and HTTPError:
        return None


def extract_content(page):
    start = 0
    end = 0
    re_start = \
        re.compile(r'<h1 id="firstHeading" '
                   r'class="firstHeading" lang="ru">.*</h1>')
    re_end = re.compile(r'<div class="visualClear"></div>')
    starts = re_start.search(page)
    ends = re_end.search(page)
    if starts.endpos > 0:
        start = starts.start(0)
    if ends.endpos > 0:
        end = ends.endpos

    return [start, end]


def extract_links(page, begin, end):
    page_content = page[begin:end]
    links = []
    re_link = \
        re.compile(r"<[aA]\s+?[hH]ref=[\"']/wiki/"
                   r"([A-Za-zА-Яа-я0-9_]*?)[\"'].*?>.*?</[aA]")
    occurences = re_link.findall(unquote(page_content))
    for occurence in occurences:
        links.append(occurence)
    return links


def get_links(page):
    content = get_content(page)
    begin_end = extract_content(content)
    return extract_links(content, begin_end[0], begin_end[1])


def find_chain(start, finish):
    link_path = {}
    links = [start]
    link_path[start] = ""

    for link in links:
        # print(link)
        if link == finish:
            path = [link]
            key = link
            while key in link_path:
                key = link_path[key]
                path.append(key)
            return link_path[link].split('/'), True
        dlinks = get_links(link)
        for dlink in dlinks:
            if dlink not in link_path and dlink != "Заглавная_страница":
                links.append(dlink)
                link_path[dlink] = link
    return None


"""
Функция принимает на вход название начальной и конечной статьи и возвращает
список переходов, позволяющий добраться из начальной статьи в конечную.
Первым элементом результата должен быть start, последним — finish.
Если построить переходы невозможно, возвращается None.
"""
pass


def main():
    # links = get_links('Бытие')
    links = find_chain('Самолет', 'Философия')
    print(links)


if __name__ == '__main__':
    main()
