from db import session, Event, Tag
import dou
import afisha
import morepodiy

print "parsing afisha"
# afisha.parseevents()
print "parsing morepodiy"
morepodiy.parseevents()
print "parsing DOU"
# dou.parseevents()

print "DONE"
print "Parsed {} events".format(session.query(Event).count())
