#!/usr/bin/python

import time
from calendar import timegm
from datetime import datetime
from launchpadlib.launchpad import Launchpad

# For what we need anonymous access should be sufficient
cachedir = './cache'
launchpad = Launchpad.login_anonymously('bug report', 'production', cachedir, version='devel')

# set the project to openstack-ansible
project = launchpad.projects('openstack/openstack-ansible')

# must have UTC time
start_date = 'Aug-01-2017Z'
end_date = 'Sep-01-2017Z'
start_timestamp = timegm( time.strptime(
    start_date.replace('Z', 'UTC'), '%b-%d-%Y%Z'))
end_timestamp = timegm( time.strptime(
    end_date.replace('Z', 'UTC'), '%b-%d-%Y%Z'))

# get the bug list
bugs = project.searchTasks(status=["New", "Confirmed", "Triaged",
                                          "Opinion", "Invalid", "In Progress",
                                          "Won't Fix", "Expired",
                                          "Fix Committed", "Fix Released"],
                                          created_since=datetime.utcfromtimestamp(start_timestamp).isoformat(),
                                          created_before=datetime.utcfromtimestamp(end_timestamp).isoformat())

# break up by importance
counts = { 'unknown':0, 'undecided':0, 'critical':0, 'high':0,
           'medium':0, 'low':0, 'wishlist':0 }
bug_details = {}
for bug in bugs:
    if bug.importance == 'Unknown':
        counts['unknown'] += 1
    if bug.importance == 'Undecided':
        counts['undecided'] += 1
    if bug.importance == 'Critical':
        counts['critical'] += 1
    if bug.importance == 'High':
        counts['high'] += 1
    if bug.importance == 'Medium':
        counts['medium'] += 1
    if bug.importance == 'Low':
        counts['low'] += 1
    if bug.importance == 'Wishlist':
        counts['wishlist'] += 1
    bug_details[bug.title] = bug.status

# Report total
print "Number of upstream (OSA) bugs created since %s: %d" % (start_date, len(bugs))
print "Breakdown by importance: %s" % (counts)
print "Overview of upstream issues:\n"
for bug_info in bug_details.iteritems():
    print str(bug_info)
