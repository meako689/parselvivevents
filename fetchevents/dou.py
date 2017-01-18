# -*- coding: utf-8 -*-
import dateparser
from pyquery import PyQuery as pq
from BeautifulSoup import BeautifulSoup
from db import Event, Tag, session


def transformdate(datestr):
    """input may be like 3 — 5 червня 2016"""
    parts = datestr.split(u'—')
    if len(parts) > 1:
        start_date = dateparser.parse(parts[0] + parts[1][3:])
        end_date = dateparser.parse(parts[1])
    else:
        start_date = dateparser.parse(datestr)
        end_date = None
    return (start_date, end_date)


def parseevents():
    parent_url = "http://dou.ua/calendar/archive/%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2/"

    counter = 1
    maxcounter = 35 #10
    typeopts = {'date': [u'Пройдет', u'Відбудеться', u'Date'],
                'location': [u'Place', u'Место', u'Місце']}

    while counter < maxcounter:
        print counter,
        try:
            parent_doc = pq(url=parent_url + str(counter))
            p_urls = parent_doc("article.b-postcard h2.title>a")
            for el in p_urls:
                url = el.attrib['href']
                exists = session.query(Event).filter_by(url = url).first()
                if not exists:
                    doc = pq(url=url)
                    info = {key: '' for key in typeopts.keys()}
                    info['title'] = doc("div.page-head h1").text()
                    info['description'] = BeautifulSoup(doc("article.b-typo").text()).text
                    info['url'] = url
                    inforows = doc(".event-info-row")
                    for inforow in inforows:
                        for typeopt in typeopts.keys():
                            if any(filter(lambda key: key in inforow.text_content(), typeopts[typeopt])):
                                info[typeopt] = inforow.find_class('dd')[0].text

                    start_date, end_date = transformdate(info['date'])
                    event_instance = Event(title=info['title'],
                        description=info['description'],
                        url=info['url'],
                        location=info['location'],
                        start_date=start_date,
                        end_date=end_date,
                        source='dou',
                        image_link=doc(".event-info-logo").attr('src')
                    )
                    for el in doc('.b-post-tags a'):
                        tag_text = el.text
                        tag_instance = session.query(Tag).filter_by(title=tag_text).first()
                        if not tag_instance:
                            tag_instance = Tag(title=tag_text)
                        event_instance.tags.append(tag_instance)
                    session.add(event_instance)
                    print event_instance.title
        except Exception, e:
            print "FAILED", e

        counter += 1
    session.commit()
