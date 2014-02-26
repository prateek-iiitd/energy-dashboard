__author__ = 'prateek'
import sys
from BeautifulSoup import BeautifulSoup
import re
import operator

args = sys.argv[1:]

if len(args) < 3:
    print "Usage: compare_scans new_scan_results.htm old_scan_results.htm"
    sys.exit(1)


new_scan_file_path = args[0]
old_scan_file_path = args[1]

new_scan_file = open(new_scan_file_path,'r').read()
old_scan_file = open(old_scan_file_path,'r').read()

new_soup = BeautifulSoup(new_scan_file)
old_soup = BeautifulSoup(old_scan_file)

new_points = {}
old_points = {}

new_streams = {}
changed_streams = {}

## Find parent div for all meter BACnet points in new scan file
li_tag = new_soup.find('li',text=re.compile(r'^device 4')).parent

## Iterate over all analog points
for li in li_tag.findAll('li',text=re.compile(r'^analog')):
    point_desc = li.parent.text
    split_desc = point_desc.split('  ')
    point_id = int(split_desc[0].split(' ')[1])
    point_stream = split_desc[1]
    new_points[point_stream] = point_id

## Find parent div for all meter BACnet points in old scan file
li_tag = old_soup.find('li',text=re.compile(r'^device 4')).parent

## Iterate over all analog points
for li in li_tag.findAll('li',text=re.compile(r'^analog')):
    point_desc = li.parent.text
    split_desc = point_desc.split('  ')
    point_id = int(split_desc[0].split(' ')[1])
    point_stream = split_desc[1]
    old_points[point_stream] = point_id

for key in new_points.keys():
    if key not in old_points:
        new_streams[key] = new_points[key]
    elif new_points[key]!= old_points[key]:
        changed_streams[key] = (old_points[key], new_points[key])

sorted_new_streams = sorted(new_streams.iteritems(), key=operator.itemgetter(1))
sorted_changed_streams = sorted(changed_streams.iteritems(), key=operator.itemgetter(1))

print
print "--------------New Streams-----------"
for x in sorted_new_streams:
    print "%s - %s" %(str(x[0]),str(x[1]))

print
print "-----------Changed Streams----------"
for x in sorted_changed_streams:
    print "%s - Old ID: %s, New ID: %s" %(str(x[0]),str(x[1][0]),str(x[1][1]))