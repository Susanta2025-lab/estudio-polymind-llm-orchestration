"""Tiny synthetic PDFs generated with the existing pypdf dependency."""

from io import BytesIO
import pytest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject, NumberObject


@pytest.fixture
def pdf_bytes():
    def build(kinds=("text", "blank", "text"), encrypted=False, labels=False):
        writer = PdfWriter()
        for index, kind in enumerate(kinds):
            page = writer.add_blank_page(width=300, height=400)
            if kind in ("text", "columns"):
                font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                         NameObject('/Subtype'): NameObject('/Type1'),
                                         NameObject('/BaseFont'): NameObject('/Helvetica')})
                page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
                stream = DecodedStreamObject()
                text = f'BT /F1 12 Tf 20 350 Td (Page {index+1} alpha) Tj ET'
                if kind == 'columns':
                    text += ' BT /F1 12 Tf 170 350 Td (Column beta) Tj ET'
                stream.set_data(text.encode('ascii'))
                page[NameObject('/Contents')] = writer._add_object(stream)
            elif kind == 'image':
                image = DecodedStreamObject()
                image.set_data(b'\xff\x00\x00')
                image.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Image'),
                              NameObject('/Width'): NumberObject(1), NameObject('/Height'): NumberObject(1),
                              NameObject('/ColorSpace'): NameObject('/DeviceRGB'), NameObject('/BitsPerComponent'): NumberObject(8)})
                page[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): DictionaryObject({NameObject('/Im0'): writer._add_object(image)})})
                stream = DecodedStreamObject(); stream.set_data(b'q 100 0 0 100 0 0 cm /Im0 Do Q')
                page[NameObject('/Contents')] = writer._add_object(stream)
            elif kind == 'graphics':
                stream = DecodedStreamObject(); stream.set_data(b'0 0 100 100 re f')
                page[NameObject('/Contents')] = writer._add_object(stream)
        if labels:
            writer.set_page_label(0, len(kinds) - 1, prefix='Appendix')
        if encrypted:
            writer.encrypt('synthetic-password')
        output = BytesIO(); writer.write(output)
        return output.getvalue()
    return build
