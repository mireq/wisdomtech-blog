#!/bin/bash
inkscape favicon.svg --export-filename=favicon-0.png -d 96
inkscape favicon.svg --export-filename=favicon-1.png -d 144
inkscape favicon.svg --export-filename=favicon-2.png -d 192
pngquant --nofs -f --quality 5 --ext .png favicon-0.png
pngquant --nofs -f --quality 5 --ext .png favicon-1.png
pngquant --nofs -f --quality 5 --ext .png favicon-2.png
icotool -c favicon-0.png favicon-1.png favicon-2.png -o favicon.ico
