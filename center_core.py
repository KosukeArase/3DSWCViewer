
"""
center core を楕球と見なした時の楕球のパラメータを求めるために描画するツール
Usage:
$ python ellipse.py n
n=0: 200.swc, n=1: 300.swc, n=2: 301.swc
"""

import sys
import plotly.offline as offline
import plotly.graph_objs as go
from sklearn import preprocessing
import numpy as np
offline.init_notebook_mode()


def get_trace(_x, _y, _z, _color='rgb(255, 0, 0)'):
    trace = go.Scatter3d(
        x=_x,
        y=_y,
        z=_z,
        mode='markers',
        marker=dict(
            sizemode='diameter',
            color = _color,
            colorscale = 'Portland',
            line=dict(color='rgb(255, 255, 255)'),
            opacity=0.9,
            size=1
        )
    )
    return trace


files = [('200.swc', 1214), ('300.swc', 22928), ('301.swc', 12525)]

# cx, cy, cz = 170, 200, 75
cx, cy, cz = 180, 210, 85 
ax, ay, az = 1, 1, 2
r = 50

file, N = files[int(sys.argv[1])]

with open('swc/'+file, 'r') as f:
    line = f.readline()
    while line[0] == '#':
        line = f.readline()

    lines = f.readlines()
    assert len(lines) == N

    coordinates = np.zeros([4, N]) # x, y, z, excluded?
    for i in range(N):
        x, y, z = list(map(float, lines[i].split()[2:5]))
        coordinates[:3, i] = x, y, z
        if (x-cx)**2 * ax**2 + (y-cy)**2 * ay**2  + (z-cz)**2 * az**2  < r**2:
            coordinates[3,i] = 1


without_synapse = np.where(coordinates[3]==1)
with_synapse = np.where(coordinates[3]==0)

with open(file.split('.')[0]+'_center_core.txt', 'w') as f:
    for syn in without_synapse[0]:
        f.write(str(syn+1)+'\n')

trace1 = get_trace(coordinates[0][without_synapse], coordinates[1][without_synapse], coordinates[2][without_synapse], 'rgb(255, 0, 0)')
trace2 = get_trace(coordinates[0][with_synapse], coordinates[1][with_synapse], coordinates[2][with_synapse], 'rgb(0, 0, 255)')


data = [trace1, trace2]
layout=dict(height=1000, width=1000, title='center_core')
fig=dict(data=data, layout=layout)
offline.plot(fig, filename=file.split('.')[0]+'_center_core_result')

