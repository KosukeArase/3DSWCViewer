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
            if x+y>thresh:
                coordinates[3,i] = 1
            # if toroid_flag == 7.:
            #     coordinates[4,i] = 1


    og = np.where(coordinates[3]==1) # OG
    mgc = np.where(coordinates[3]==0) # MGC
    with open(file.split('.')[0]+'_og.txt', 'w') as f:
        for syn in og[0]:
            f.write(str(syn+1)+'\n')

    _trace1 = get_trace(coordinates[0][og], coordinates[1][og], coordinates[2][og], 'rgb(255, 0, 0)') #og
    _trace2 = get_trace(coordinates[0][mgc], coordinates[1][mgc], coordinates[2][mgc], 'rgb(0, 0, 255)')# mgc
    # _trace3 = get_trace(coordinates[0][other_region], coordinates[1][other_region], coordinates[2][other_region], color)
    return _trace1, _trace2#, _trace3


files = [('300.swc', 22928, 'rgb(0, 0,0)'), ('301.swc', 12525, 'rgb(0, 0, 0)')]

thresh = 275

# file, N = files[int(sys.argv[1])]
data = []
for file, N, color in files:
    trace1, trace2 = process()
    data.append(trace1)
    data.append(trace2)
    # data.append(trace3)

# data = [trace1, trace2]
print(data)
layout=dict(height=1000, width=1000, title='toroid')
fig=dict(data=data, layout=layout)
offline.plot(fig, filename=file.split('.')[0]+'_toroid_result_tmp')

