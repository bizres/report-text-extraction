#!/usr/bin/python
# -*- coding:utf-8 -*-

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import io


def to_text(data):

    file = data
    
    if isinstance(file, io.BytesIO):
        file.seek(0)
    else:
        file = io.BytesIO(file.read())

    try:
        full_text = ''

        # Iterate over every page of document
        for page_layout in extract_pages(file):

            page_text = ''

            # Iterate over every container on page
            for element in page_layout:

                # Only consider containers which are marked as text containers (no headers, footers, tables or images)
                if isinstance(element, LTTextContainer):

                    section_text = ''

                    # Iterate over every line of text container
                    for text_line in element:
                        section_text += text_line.get_text().replace('\n', ' ')
                    
                    # Remove all whitespaces (except ' ') such as new lines or tabs
                    section_text = ' '.join(section_text.split())

                    page_text += section_text # Add section text to page text
                    page_text += '\n' # Separate sections with a new line

            full_text += page_text # Add page text to full text
            full_text += '\n' # Separate pages with a double new line

    except:
        full_text = None
        
    return full_text