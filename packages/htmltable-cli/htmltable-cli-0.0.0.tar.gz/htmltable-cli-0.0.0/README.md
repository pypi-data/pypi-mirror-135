# htmltable cli

Command line tool to convert lists to html tables with embedded audios and images.

![example output](images/example_output_1.png)
## Usage

    $ python htmltable.py --help
    usage: 

    Command line tool to convert lists to html tables with embedded audios and images.

    Separate columns with ,
    The easiest way to use it is to put each column in a folder and then pass it using a wildcard *

        [-h] [-b] [-x] [-a] data [data ...]

    positional arguments:
    data                 input table data. Format: columnname1 item1 item2 item3
                        , columname2 item1 item2 item3 ...

    optional arguments:
    -h, --help           show this help message and exit
    -b, --base64
    -x, --index          add an index column
    -a, --infer_columns  (A)uto infer columnnames from parent directories

Assuming filestructure:

```
.
├── col1
│   ├── audio.wav
|   ├ ...
│   └── image.png
├── col2
│   ├── audio.wav
|   ├ ...
│   └── image.jpg
└── col3
    ├── audio.wav
    ├ ...
    └── image.png
```


- Separate columns with `,`
- The easiest way to use it is to put each column in a folder and then pass it using a wildcard `*`

### Examples

specifying file paths explicitly

```sh
python htmltable.py col1 col1/1.wav col1/2.wav col1/3.wav , \
                    col2 col2/1.wav col2/2.wav col2/3.wav , \
                    col3 col3/1.wav col3/2.wav col3/3.wav --base64 --index > output.html
```

Specifying file paths implicitly using *

```sh
python htmltable.py col1 col1/*.wav , \
                    col2 col2/*.wav , \
                    col3 col3/*.wav --base64 --index > output.html
```

(A)uto infer columnnames from parent directories (`-a` or `--infer_columns`).


```sh
python htmltable.py col1/*.wav , \
                    col2/*.wav , \
                    col3/*.wav --infer_columns --base64 --index > output.html
```

(you don't actually have to organize your arguments in new lines :p)

## TODO

- [ ] add support for videos
