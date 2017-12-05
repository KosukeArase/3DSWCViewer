"""
toroid 領域中のコンパートメントが集中している部分の中心を楕球状にくり抜く

Usage:
$ python troid.py

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


def process():
    with open('swc/'+file, 'r') as f:
        line = f.readline()
        while line[0] == '#':
            line = f.readline()

        lines = f.readlines()
        assert len(lines) == N

        coordinates = np.zeros([5, N]) # x, y, z, excluded?, toroid?
        for i in range(N):
            toroid_flag, x, y, z = list(map(float, lines[i].split()[1:5]))
            coordinates[:3, i] = x, y, z
            if (x-cx)**2 * ax**2 + (y-cy)**2 * ay**2  + (z-cz)**2 * az**2  < r**2:
                coordinates[3,i] = 1
            if toroid_flag == 7.:
                coordinates[4,i] = 1


    toroid = np.where((coordinates[3]-1)*coordinates[4]!=0)# toroid and not center
    without_synapse = np.where(coordinates[3]*coordinates[4]==1) # toroid and center
    other_region = np.where(coordinates[4]==0) # not toroid
    with open(file.split('.')[0]+'_toroid.txt', 'w') as f:
        for syn in toroid[0]:
            f.write(str(syn+1)+'\n')

    _trace1 = get_trace(coordinates[0][toroid], coordinates[1][toroid], coordinates[2][toroid], 'rgb(255, 0, 0)') #toroid
    _trace2 = get_trace(coordinates[0][without_synapse], coordinates[1][without_synapse], coordinates[2][without_synapse], 'rgb(0, 0, 255)')# center of toroid
    _trace3 = get_trace(coordinates[0][other_region], coordinates[1][other_region], coordinates[2][other_region], color)
    return _trace1, _trace2, _trace3


files = [('200.swc', 1214, 'rgb(0,0,0)'), ('300.swc', 22928, 'rgb(0, 0,0)'), ('301.swc', 12525, 'rgb(0, 0, 0)')]

cx, cy, cz = 85, 135, 90 
ax, ay, az = 1, 1, 2
r = 20

# file, N = files[int(sys.argv[1])]
data = []
for file, N, color in files:
    trace1, trace2, trace3 = process()
    data.append(trace1)
    data.append(trace2)
    data.append(trace3)

# data = [trace1, trace2]
layout=dict(height=1000, width=1000, title='toroid')
fig=dict(data=data, layout=layout)
offline.plot(fig, filename=file.split('.')[0]+'_toroid_result')

