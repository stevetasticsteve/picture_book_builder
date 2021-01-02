#! /usr/bin/python3

### Chronological picture book builder ###
#
# Creator: stephen_stanley@ntmpng.org, GPL v3
#
# This script will take a selection of Foundation Matters chronological
# pictures that you define and build them into an A4, A5 or A6 book.
#
# Installation:
# - Python must be installed on your computer https://www.python.org/
# - Certain Python libraries must be installed:
#   - Open a command line prompt in the script's parent folder
#   - Run this command:   pip3 install PyPdF2 img2pdf PIL reportlab
#
# Options:
# All options are included in the options section at the top of the script
# Change them to the desired state and then save the script and run it.
# Front matter can also be tweaked if desired.
# The most important option is that you can change which pictures go into
# your book by editing the selection list.
#
# Running the script:
# Run from the command line using python
#
# Assumptions:
# The script isn't designed to be rock solid, it relies on the following:
# - Script is located in the same folder as the foundation matters pics
# - The pictures are .jpg files
# - Pictures are named like this: 001 Prophet.jpg
#      The script uses the 3 digit number at the start of the filename
# - No other files in the folder have a 3 digit number in their name
#
#
### Options ###
paper_size = 'A4'  # Choose 'A4', 'A5' or 'A6' paper
quality = 'H'  # Choose 'H' (300dpi), 'M' 150dpi) or 'L' (75dpi) quality
front_matter = True # choose False if you don't want front matter
selection = [
    '001',
    '004',
    '008',
    '011',
    '012',
    '015',
    '019',
    '020',
    '029',
    '033',
    '036',
    '039',
    '043',
    '046',
    '049',
    '053',
    '055',
    '059',
    '060',
    '063',
    '066',
    '069',
    '079',
    '080',
    '084',
    '089',
    '090',
    '092',
    '095',
    '097',
    '098',
    '104',
    '109',
    '107',
    '111',
    '112',
    '113',
    '114',
    '117',
    '118',
    '119',
    '120',
    '121',
    '122',
    '123',
    '124',
    '125',
    '126',
    '129',
    '128',
    '130',
    '133',
    '134',
    '136',
    '138',
    '140',
    '144',
    '147',
    '148',
    '151',
    '154',
    '156',
    '158',
    '159',
    '160',
    '162',
    '164',
    '166',
    '169',
    '165',
    '170',
    '171',
    '174',
    '176',
    '178',
    '179',
    '180',
    '181',
    '183',
    '184',
    '186',
    '190',
    '194',
    '195'
]
###

### Front matter ###
font = 'Helvetica'  # Helvetica, Times-Roman or Courier are allowed

title = 'Baibel piksa long kos 1'

subtitle = """
{n} piksa long strongim wok 
bilong autim Tok bilong God
""".format(n=len(selection))

title_page_image = '186 Crucifixion.jpg'

ntm_address = """
New Tribes Mission
P.O. Box 1079, Goroka E.H.P 441
Papua New Guinea    
"""

_copyright = """
This book was written and published by New Tribes Mission.
Please do not copy or reproduce in part or in whole
without written consent.

Copyright © 2021 New Tribes Mission"""

preface = """
Preface
This picture book is designed to support the teaching of
the 'God I Wokim Strongpela Haus' Bible curriculum with a
selection of the materials produced by Foundation Matters.
Pictures are used by permission and are intended to be
used with the Kos 1 and Kos 2 book series with more
information being available by contacting New Tribes 
Mission's printing department: central-trc@ntmpng.org.
"""

tpi_preface = """
Tok i go pas
As bilong dispela buk em strongim ol tisa i yusim 'God i
wokim strongpela haus' Baibel kos. Mipela i makim sampela
piksa ol lain long Foundation Matters i wokim. Dispela
lain i givim tok orait long mipela yusim ol piksa olsem.
Ol piksa long dispela buk em inap long strongim ol tisa i
skul long Kos 1 na Kos 2. Sapos yu laikim save moa long ol
dispela samting yu mas salim pas long New Tribes Mission:
central-trc@ntmpng.org
"""
###

### Program begins ###

import io
import os
import tempfile

import img2pdf
from PIL import Image
from PyPDF2 import PdfFileMerger
from reportlab.pdfgen.canvas import Canvas

print('### Chron Pictures Book builder ###')
# ensure the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
output_file_name = 'Chronological picture selection.pdf'
# build a list of file names we're interested in
image_paths = sorted([p for p in os.listdir() for s in selection if s in p])
print('Set to create {s} book at {q} quality\n'.format(
    s=paper_size, q=quality))

# Hardcoded recommended pixel sizes for target dpi's
pixel_quality = {
    'A6H': (1240, 1748),
    'A6M': (620, 874),
    'A6L': (310, 437),
    'A5H': (1748, 2480),
    'A5M': (874, 1240),
    'A5L': (437, 620),
    'A4H': (2480, 3508),
    'A4M': (1240, 1754),
    'A4L': (620, 877)
}

# Set the paper size, font size and image quality
if paper_size == 'A6':
    paper_input = (img2pdf.mm_to_pt(105), img2pdf.mm_to_pt(148))
    font_scaling = 2  # used later to adjust font size relative to page
    if quality == 'L':
        pixels = pixel_quality['A6L']
    elif quality == 'M':
        pixels = pixel_quality['A6M']
    else:
        pixels = pixel_quality['A6H']
elif paper_size == 'A5':
    paper_input = (img2pdf.mm_to_pt(148), img2pdf.mm_to_pt(210))
    font_scaling = 1.5
    if quality == 'L':
        pixels = pixel_quality['A5L']
    elif quality == 'M':
        pixels = pixel_quality['A5M']
    else:
        pixels = pixel_quality['A5H']
else:
    # default to A4
    paper_input = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    font_scaling = 1
    paper_size = 'A4'
    if quality == 'L':
        pixels = pixel_quality['A4L']
    elif quality == 'M':
        pixels = pixel_quality['A4M']
    else:
        pixels = pixel_quality['A4H']
layout = img2pdf.get_layout_fun(paper_input)

# Adjust font size for different page sizes
text_size = {
    'S': 16 / font_scaling,
    'M': 24 / font_scaling,
    'L': 40 / font_scaling
}


# Some helper functions
def set_large_font(page, font_size=text_size['L']):
    try:
        page.setFont(font, font_size)
    except KeyError:
        print('{f} is not a valid font, defaulting to Helvetica'.format(f=font))
        page.setFont('Helvetica', font_size)


def set_medium_font(page):
    set_large_font(page, font_size=text_size['M'])


def draw_paragraph(page, text, y, font_size):
    txt = page.beginText()
    txt.setFont(font, text_size[font_size])
    txt.setTextOrigin(left_margin, paper_input[1] * y)
    txt.textLines(text)
    page.drawText(txt)
###


# Create a temporary directory to store converted images
# All pdf files in this folder will be joined into the final book
with tempfile.TemporaryDirectory() as temp_dir:
    print('Resizing images...')
    # Loop through and convert the images
    for i, image in enumerate(image_paths, 1):
        # Create a new temporary pdf file
        pdf_path = os.path.join(temp_dir, image.rstrip('jpg') + 'pdf')
        # image_file refers to the exported pdf
        with open(pdf_path, 'wb') as image_file:
            print(' {n} of {total}'.format(n=i, total=len(selection)))
            im = Image.open(image)  # im refers to the image object used by PIL
            o = io.BytesIO()  # write the resized image into memory
            im = im.resize(pixels)
            im = im.save(o, format='jpeg')
            o.seek(0)  # start at the beginning of the bytecode
            # convert jpg stored in memory into pdf and save in temporary folder
            image_file.write(img2pdf.convert(o, layout_fun=layout))

    if front_matter:
        # Create front matter
        print('\nCreating front matter...')
        left_margin = paper_input[0] * 0.15

        # Title page
        title_pdf = os.path.join(temp_dir, '0000_title.pdf')
        title_page = Canvas(title_pdf, pagesize=paper_input)
        # write the title
        set_large_font(title_page)
        title_page.drawCentredString(
            paper_input[0] / 2, paper_input[1] * 0.9, title)
        # write the subtitle
        set_medium_font(title_page)
        for i, t in enumerate(subtitle.splitlines()):
            title_page.drawCentredString(
                paper_input[0] / 2, paper_input[1] * 0.15 - (i * 25 / font_scaling), t)
        # add the title image
        title_image = Image.open(title_page_image)
        # crop image to 60% of the size of the page
        cropped_image_size = (int(paper_input[0] * 0.6), int(paper_input[1] * 0.6))
        title_image = title_image.resize(cropped_image_size)
        # Add picture x centered, bottom corner at 20% of page height
        x = paper_input[0] / 2 - cropped_image_size[0] / 2
        title_page.drawInlineImage(title_image, x, paper_input[1] * 0.2)
        title_page.save()

        # Copyright page
        copyright_pdf = os.path.join(temp_dir, '0001_copyright.pdf')
        copyright_page = Canvas(copyright_pdf, pagesize=paper_input)
        # Add the copyright info to the address
        draw_paragraph(copyright_page, _copyright +
                    '\n' * 3 + ntm_address, 0.9, 'S')
        copyright_page.save()

        preface_pdf = os.path.join(temp_dir, '0002_preface.pdf')
        preface_page = Canvas(preface_pdf, pagesize=paper_input)
        # write the English and Tok Pisin prefaces
        draw_paragraph(preface_page, preface +
                    '\n' * 3 + tpi_preface, 0.75, 'S')
        preface_page.save()

    # Merge temp files together
    print('Merging pdf pages...')
    pdf_merger = PdfFileMerger(strict=False)
    for pdf in sorted(os.listdir(temp_dir)):
        pdf_merger.append(os.path.join(temp_dir, pdf))
    pdf_merger.write(paper_size + '_' + output_file_name)
    pdf_merger.close()

print('Done!')
