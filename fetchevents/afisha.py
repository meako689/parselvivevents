import dateparser
from pyquery import PyQuery as pq
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup
from db import Event, Tag, session


def parseevents():
    parent_url = "http://afishalviv.net/events/"
    urls = []
    dt = datetime(2016, 1, 1)
    end_dt = datetime(2017, 1, 1)

    while dt < end_dt:
        print dt, 
        try:
            parent_doc = pq(url=parent_url + dt.strftime("%Y-%m-%d"))
            p_urls = parent_doc("#tribe-events-content a.af-event:first")
            url_categories = parent_doc("#tribe-events-content div.af-location--type")
            for i in xrange(len(p_urls)):
                url = p_urls[i].attrib['href']
                exists = session.query(Event).filter_by(url = url).first()
                if url not in urls and not exists:
                    urls.append(url)
                    doc = pq(url=url)
                    date_attr = doc("div.af-single-events-data.-date").text().split('-')
                    tag_text = url_categories[i].findall('a')[1].text
                    event_instance = Event(url=url,
                        title=doc("h2.af-single-title").text(),
                        start_date=dateparser.parse(date_attr[0]),
                        end_date=dateparser.parse(date_attr[1]) if len(date_attr) > 1 else None,
                        description=BeautifulSoup(doc("div.af-page-block.-fourth").text()).text,
                        location=doc("div.af-single-events-data.-address").text(),
                        source='afisha',
                        image_link=doc(".wp-post-image").attr('src')
                    )
                    tag_instance = session.query(Tag).filter_by(title=tag_text).first()
                    if not tag_instance:
                        tag_instance = Tag(title=tag_text)
                    event_instance.tags.append(tag_instance)
                    session.add(event_instance)
                    print event_instance.title

        except Exception as e:
            print "FAILED", e
        dt += timedelta(1)
    session.commit()


