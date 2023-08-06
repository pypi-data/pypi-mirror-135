# htmltable cli

Command line tool to convert lists to html tables with embedded audios and images.

![example output](https://raw.githubusercontent.com/FarisHijazi/htmltable-cli/master/images/example_output_1.png)

## Installation

### From pypi

```sh
pip install htmltable-cli
```

### From source

```sh
pip install git+https://github.com/FarisHijazi/htmltable-cli
```

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
htmltable col1 col1/1.wav col1/2.wav col1/3.wav , \
          col2 col2/1.wav col2/2.wav col2/3.wav , \
          col3 col3/1.wav col3/2.wav col3/3.wav --base64 --index > output.html
```

Specifying file paths implicitly using `*`

```sh
htmltable col1 col1/*.wav , \
          col2 col2/*.wav , \
          col3 col3/*.wav --base64 --index > output.html
```

(A)uto infer columnnames from parent directories (`-a` or `--infer_columns`).


```sh
htmltable col1/*.wav , \
          col2/*.wav , \
          col3/*.wav --infer_columns --base64 --index > output.html
```

(you don't actually have to organize your arguments in new lines :p)

## Known issues

- Outputting files is only supported in the `.` dir. i.e `htmltable .... > some/other/path/output.html` has issues when not using `--base64`
- `ERROR: Cannot uninstall 'llvmlite'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.`

    run `pip install llvmlite==0.36.0 --ignore-installed`
