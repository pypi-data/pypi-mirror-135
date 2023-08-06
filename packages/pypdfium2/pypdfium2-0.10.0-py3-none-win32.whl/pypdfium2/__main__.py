# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

import os
import sys
import ast
import argparse
import pypdfium2 as pdfium
from pypdfium2 import _version
from os.path import (
    join,
    abspath,
    basename,
    splitext,
)


def rotation_type(string):
    rotation = int(string)
    if rotation not in (0, 90, 180, 270):
        raise ValueError("Invalid rotation value {}".format(rotation))
    return rotation

def colour_type(string):
    if string.lower() == 'none':
        return None
    else:
        evaluated = ast.literal_eval(string)
        if not isinstance(evaluated, (int, tuple, list)):
            raise ValueError("Invalid colour value {}".format(evaluated))
        return evaluated

def optimise_mode_type(string):
    return pdfium.OptimiseMode[string.lower()]


def pagetext_type(value):
    
    if not value:
        return
    
    page_indices = []
    splitted = value.split(',')
    
    for page_or_range in splitted:
        
        if '-' in page_or_range:
            
            start, end = page_or_range.split('-')
            start = int(start) - 1
            end = int(end) - 1
            
            if start < end:
                pages = [i for i in range(start, end+1)]
            else:
                pages = [i for i in range(start, end-1, -1)]
            
            page_indices.extend(pages)
        
        else:
            
            page_indices.append(int(page_or_range) - 1)
    
    return page_indices


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description = "Rasterise PDFs with PyPDFium2",
        formatter_class = argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--input', '-i',
        dest = 'pdffile',
        required = True,
        help = "Path to the PDF document to render.",
    )
    parser.add_argument(
        '--output', '-o',
        help = "Output directory where to place the serially numbered images.",
    )
    parser.add_argument(
        '--prefix', '-p',
        default = None,
        help = "Prefix for each image filename.",
    )
    parser.add_argument(
        '--password',
        default = None,
        help = "A password to unlock the document, if encrypted.",
    )
    parser.add_argument(
        '--pages',
        default = None,
        type = pagetext_type,
        help = "Numbers of the pages to render. Defaults to all.",
    )
    parser.add_argument(
        '--scale',
        default = 1,
        type = float,
        help = ("Define the resolution of the output images. By default, one PDF point (1/72in) "
                "is rendered to 1x1 pixel. This factor scales the number of pixels that represent "
                "one point."),
    )
    parser.add_argument(
        '--rotation',
        default = 0,
        type = rotation_type,
        help = "Rotate pages by 90, 180 or 270 degrees.",
    )
    parser.add_argument(
        '--colour',
        default = 0xFFFFFFFF,
        type = colour_type,
        help = ("Page background colour as 32-bit ARGB hex string, or as tuple of "
                "integers from 0 to 255. Use None for alpha background."),
    )
    parser.add_argument(
        '--no-annotations',
        action = 'store_true',
        help = "Do not render PDF annotations.",
    )
    parser.add_argument(
        '--optimise-mode',
        default = 'none',
        type = optimise_mode_type,
        help = "Select a rendering optimisation mode (none, lcd_display, printing)",
    )
    parser.add_argument(
        '--greyscale',
        action = 'store_true',
        help = "Whether to render in greyscale mode (no colours)",
    )
    parser.add_argument(
        '--processes',
        default = os.cpu_count(),
        type = int,
        help = "The number of processes to use for rendering. Defaults to the number of CPU cores."
    )
    parser.add_argument(
        '--show-toc',
        action = 'store_true',
        help = "Print the table of contents of a PDF document."
    )
    parser.add_argument(
        '--version', '-v',
        action = 'version',
        version = "PyPDFium2 {}\nPDFium {}".format(_version.V_PYPDFIUM2, _version.V_LIBPDFIUM)
    )
    return parser.parse_args(args)



def main():
    
    args = parse_args()
    
    if args.show_toc:
        with pdfium.PdfContext(abspath(args.pdffile)) as pdf:
            toc = pdfium.get_toc(pdf)
            pdfium.print_toc(toc)
        sys.exit()
    
    if args.prefix is None:
        prefix = splitext(basename(args.pdffile))[0] + '_'
    else:
        prefix = args.prefix
    
    output_base = join(abspath(args.output), prefix)
    
    renderer = pdfium.render_pdf(
        args.pdffile,
        args.pages,
        password = args.password,
        scale = args.scale,
        rotation = args.rotation,
        colour = args.colour,
        annotations = not args.no_annotations,
        greyscale = args.greyscale,
        optimise_mode = args.optimise_mode,
        n_processes = args.processes,
    )
    
    for image, suffix in renderer:
        filename = output_base + suffix + '.png'
        image.save(filename)
        image.close()


if __name__ == '__main__':
    main()
