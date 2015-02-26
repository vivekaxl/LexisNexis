#!/usr/bin/env python
from __future__ import division, print_function
import click
import subprocess

@click.command()
@click.option('--hw',
    prompt='Which assignment? (use {} to skip this dialogue)'.format('--hw'),
    help='assignment number', type=click.INT)
@click.option('-o', help='output file', default='witschey')
@click.option('-p', help='input pages per output page',
    default=2, type=click.IntRange(min=1, max=2, clamp=True))
@click.option('--landscape', is_flag=True)
@click.option('--to-ps', is_flag=False)
@click.option('--chars-per-line', help='characters per line')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def build_pdf(files, hw, o, p, landscape, to_ps, chars_per_line):
    click.echo(chars_per_line)
    if not files:
        click.echo('please give file arguments')
        click.exit()
    ps_name = o + '.ps' if to_ps else '/tmp/hwgen.ps'
    title = '--center-title="csc710sbse: hw{hw}: Witschey"'.format(hw=hw)
    a2ps_cmd = [
        'a2ps',
        '-MLetter', # paper size
        title, # title on each page; customize to your needs
        '-{p}'.format(p=p), # pages per sheet
        '-C', # number every 5th line
        '-Av', # allow multiple files per sheet
        '--highlight-level=none', # fixes silly treatment of comments
        # '-q', # you can make the command quiet if you want
    ]
    if chars_per_line:
        a2ps_cmd.append('-l {}'.format(chars_per_line)) # set characters per line
    if landscape:
        a2ps_cmd.append('--landscape') # set to landscape
    a2ps_cmd.extend(['-o', ps_name]) # set output file
    a2ps_cmd.extend(files)
    print('about to execute', a2ps_cmd)
    p1 = subprocess.call(a2ps_cmd)
    if p1 != 0:
        exit(p1)

    if not to_ps:

        outfile = o
        ps2pdf_cmd = [
            'ps2pdf',
            ps_name,
            outfile + '.pdf'
        ]
        print('about to execute', ps2pdf_cmd)
        p2 = subprocess.call(ps2pdf_cmd)


if __name__ == '__main__':
    build_pdf()

# dl listing.* ; a2ps --center-title="csc710sbse: hw1: Witschey" -2C -MLetter -o listing.ps *.py ; ps2pdf listing.ps listing.pdf

