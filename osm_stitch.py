#! /usr/bin/env python

import math
import httplib
import sys
from PIL import Image

if not len(sys.argv) > 6:
    raise SystemExit("Usage: upper_lat upper_lon lower_lat lower_lon zoom output_file")

upper_lat = float(sys.argv[1])
upper_lon = float(sys.argv[2])
lower_lat = float(sys.argv[3])
lower_lon = float(sys.argv[4])
zoom = int(sys.argv[5])
output = sys.argv[6]
#upper_lat = 30.690502
#upper_lon = -84.418142
#lower_lat = 30.099011
#lower_lon = -84.003676
sub = ''

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def writetile(x, y, zoom):
    global sub
    if sub == 'a':
      sub = 'b'
    elif sub == 'b':
      sub = 'c'
    else:
      sub = 'a'
    file_name = str(x) + '_' + str(y) + '.png'
    conn = httplib.HTTPConnection(sub + '.tile.openstreetmap.org')
    print('Retrieving /' + str(zoom) + '/' + str(x) + '/' + str(y) + '.png')
    conn.request('GET', '/' + str(zoom) + '/' + str(x) + '/' + str(y) + '.png')
    response = conn.getresponse()
    conn.close()

    if response.status == 200 and response.reason == 'OK':
        print('/' + str(zoom) + '/' + str(x) + '/' + str(y) + '.png retrieved')
        f = open('/tmp/' + file_name, 'w')
        f.write(response.read())
        f.close()
    else:
        print('/' + str(zoom) + '/' + str(x) + '/' + str(y) + '.png failed')
        print(str(response.status) + ' ' + response.reason)
    return file_name

top_left = deg2num(upper_lat, upper_lon, zoom)
bottom_right = deg2num(lower_lat, lower_lon, zoom)

height = (bottom_right[1] - top_left[1]) * 256
width = (bottom_right[0] - top_left[0]) * 256
osm_map = Image.new("RGBA", (width, height))

for x in range(top_left[0], bottom_right[0]):
    for y in range(top_left[1], bottom_right[1]):
        foo = Image.open('/tmp/' + writetile(x, y, zoom))
        osm_map.paste(foo, (256 * (x - top_left[0]), 256 * (y - top_left[1])))

print('Saving map')
osm_map.save(output + '/map.png')
