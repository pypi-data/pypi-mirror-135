"""

Command line tool to convert lists to html tables with embedded audios and images.

Separate columns with ,
The easiest way to use it is to put each column in a folder and then pass it using a wildcard *


Examples:
  specifying cells explicitly
    $ python htmltable.py col1 col1/1.wav col1/2.wav col1/3.wav , col2 col2/1.wav col2/2.wav col2/3.wav , col3 col3/1.wav col3/2.wav col3/3.wav
  specifying cells implicitly using *
    $ python htmltable.py col1 col1/*.wav , col2 col2/*.wav > output.html

"""

import itertools
import argparse
from functools import partial
import base64
import io
import sys
import os

import numpy as np
import wavio
from scipy.io.wavfile import read
from pathlib import Path


def remove_silence(y, top_db=25):
    from librosa import effects
    loudls = effects.split(y, top_db=top_db)
    y = np.concatenate([y[el[0]:el[1]] for el in loudls], 0)
    return y


def trim_silence(y, top_db=60):
    import librosa
    yt, _ = librosa.effects.trim(y, top_db=top_db)
    return yt


def load_wav(wav_path):
    assert os.path.isfile(wav_path), f'file does not exist {wav_path}'
    try:
        sampling_rate, audio = read(wav_path)
        # audio = trim_silence(audio)
        return audio, sampling_rate
    except FileNotFoundError as fnfe:
        return None


def create_html(rowwise, titlestr=''):
    html = '<html>'
    html += """<head>
    <style>
        img {
            width: 200px;
        }
        /* first row */
        tr:nth-child(1) > td {
            text-align: center;
            font-weight: bold;
        }

        td:nth-child(5), td:nth-child(6) {
            background-color: #11ff0021;
        }

        td:nth-child(7), td:nth-child(8) {
            background-color: rgba(0 90 255, 0.1);
        }

        td:nth-child(9), td:nth-child(10) {
            background-color: #ff000021;
        }

        table {
            width: 100%;
        }

        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }

        th, td {
            padding: 15px;
            text-align: left;
        }

        tr:nth-child(even) {
            background-color: #eee;
        }

        tr:nth-child(odd) {
            background-color: #fff;
        }

        th {
            background-color: black;
            color: white;
            text-align: center;
        }

        audio {
            width: 200px;
        }
    </style>
</head>""" + f"""
<body>{titlestr}
<table>
    <tr>""" + ''.join([f'<th>{c}</th>\n' for c in rowwise[0]]) + """</tr>"""

    for row in rowwise[1:]:
        html += f'<tr>'
        for cell in row:
            html += f'<td> {cell} </td>'
        html += '</tr>'

    html += ''' </table></body></html>'''

    return html


def get_audio(fpath, ret_html=True, b64=True):
    wav, sampling_rate = load_wav(fpath)
    if b64:
        # Audio to base64
        file_in_memory = io.BytesIO()
        wavio.write(file_in_memory, wav, sampling_rate, sampwidth=3)
        file_in_memory.seek(0)
        encode_output = base64.b64encode(file_in_memory.read())
        fpath = 'data:audio/mpeg;base64,' + encode_output.decode('utf-8')

    if not ret_html:
        return fpath
    else:
        return f'<audio controls><source src="{fpath}" type="audio/wav"></audio>'


def get_img(fpath, ret_html=True, b64=True):
    from matplotlib import pyplot as plt

    img = plt.imread(fpath)
    if b64:
        # img plot to base64
        s = io.BytesIO()
        plt.imshow(img)
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        fpath = "data:image/png;base64," + base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

    if not ret_html:
        return fpath
    else:
        return f'<img align="left" src="{fpath}">'


def convert_mediapath(fpath, b64=False):
    if fpath.lower().endswith('.wav'):
        return get_audio(fpath, ret_html=True, b64=b64)
    elif fpath.lower().endswith('.png') or fpath.lower().endswith('.jpg') or fpath.lower().endswith('.jpeg'):
        return get_img(fpath, ret_html=True, b64=b64)
    else:
        return fpath


if __name__ == '__main__':
    real_print = print
    print = print if sys.stdout.isatty() else lambda *a, **k: None

    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data', type=str, nargs='+',
                        help='input table data. Format: columnname1 item1 item2 item3 , columname2 item1 item2 item3 ...')
    parser.add_argument('-b', '--base64', action='store_true')
    parser.add_argument('-x', '--index', action='store_true', help='add an index column')
    parser.add_argument('-a', '--infer_columns', action='store_true', help='(A)uto infer columnnames from parent directories')
    # parser.add_argument('--sort', action='store_true')
    # parser.add_argument('-ts', '--trim_silence', action='store_true')

    args = parser.parse_args()

    # lol: list of lists, iterates columns wise
    lol_raw = [list(y) for x, y in itertools.groupby(args.data, lambda z: z == ',') if not x]
    
    def get_parentname_fpaths(fpaths):
        parentnames = [Path(fpath).parent.name for fpath in fpaths]
        assert all(x == parentnames[0] for x in parentnames), f'inconsistent parent dir names: {parentnames}'
        return parentnames[0]

    if args.infer_columns:
        lol = [[get_parentname_fpaths(l)] + l for l in lol_raw]
    else:
        lol = lol_raw

    lol = [list(map(partial(convert_mediapath, b64=args.base64), l)) for l in lol]

    rowwise = np.array(lol).T

    if args.index:
        index = np.array(['index'] + list(range(len(rowwise) - 1)))[..., None]
        rowwise = np.hstack((index, rowwise))

    for l in lol:
        assert len(l) == len(lol[0]), f'inconsistent number of columns, expected {len(lol[0])}, got {len(l)}'

    c, r = len(lol), len(lol[0])

    html = create_html(rowwise)
    real_print(html)
