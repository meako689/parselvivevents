import requests
import json
import csv
from dateutil import parser as dateparser #different parser!
from datetime import datetime
from BeautifulSoup import BeautifulSoup

from db import session, Event, Tag

def parseevents():
    counter = 4320
    parent_url = 'http://morepodiy.lviv.ua/api/v1/events/'
    baseurl = 'http://morepodiy.lviv.ua/events/'

    while counter < 15050:
        print counter,
        counter+=1
        try:
            url = parent_url+str(counter)
            res = requests.get(url)
            if res.status_code == 200:
                evt = json.loads(res.content)['event']
                web_url=baseurl+str(evt['id'])
                exists = session.query(Event).filter_by(url = web_url).first()
                if not exists:
                    event_instance = Event(title=evt['title'],
                              description=BeautifulSoup(evt['description']).text,
                              start_date=dateparser.parse(evt['start_date']) if evt['start_date'] else None,
                              end_date=dateparser.parse(evt['end_date']) if evt['end_date'] else None,
                              url=web_url,
                              location=evt['location'],
                              source='morepodiy',
                              image_link=evt['poster']
                        )
                    tags = evt['tags'] + [evt['category_name']]
                    for tag_text in tags:
                        tag_text = tag_text.lower().strip()
                        tag_instance = session.query(Tag).filter_by(title=tag_text).first()
                        if not tag_instance:
                            tag_instance = Tag(title=tag_text)
                        if not tag_instance in event_instance.tags:
                            event_instance.tags.append(tag_instance)
                    session.add(event_instance)
                    print event_instance.title
        except Exception, e:
            print "FAILED", e

    session.commit()
