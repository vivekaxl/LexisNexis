# github-social-graph

This program helps to build simple social graphs for GitHub using it's
API and [graphviz](http://www.graphviz.org/).

## Installation

Installation via pip 1.5+:

```bash
$ pip install --process-dependency-links https://github.com/Kagami/github-social-graph/archive/master.zip
```

Installation via pip &lt;1.5:

```bash
$ pip install https://github.com/Kagami/github-social-graph/archive/master.zip
```

## Usage

Show help:
```bash
$ github-social-graph -h  # or gsg -h
```

Usage examples:

```bash
# Draw graph for vim-jp organization members (without authorization):
$ github-social-graph --orgs vim-jp -o 1.png

# Draw graph for organization and users (with authorization by password):
$ github-social-graph -u Kagami -p --orgs vim-jp --users Shougo -o 1.png

# Only fetch data for future use and analysis:
$ github-social-graph --orgs vim-jp -o jp.json

# Use pre-fetched data to draw graph:
$ github-social-graph -i jp.json -o jp.png
```

## Examples

This graph demonstrates some curious relationships between
Japanese/Vim/Haskell users (click for fullsize image):

[![](http://dump.bitcheese.net/files/ysilytu/jp-shrink-min.png)](http://dump.bitcheese.net/files/izunyjy/jp-min.png)

(Produced by `github-social-graph --token --orgs vim-jp akechi golang-samples vimjolts neovim --users bos tibbe donsbot kazu-yamamoto spl MarcWeber ZyX-I -o jp.png`)

Much simpler graph:

![](http://dump.bitcheese.net/files/itanida/kagami.png)

(Produced by `github-social-graph --full-graph --users Kagami -o kagami.png`)

## TODO

* Proper error handling
* Info about current rate limits
* Deep crawling
* Merge several JSON inputs
* Additional graph modes and options

## License

github-social-graph - Build simple social graphs for GitHub

Written in 2014 by Kagami Hiiragi <kagami@genshiken.org>

To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.