from reportlab.lib import colors
from reportlab.platypus import Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.contrib.staticfiles.finders import find
from my_project.settings import BASE_DIR


class CustomReportLabMethods:

    @staticmethod
    def get_logo(**kwargs):
        """
        Arguments:

        path - The relative path of the image inside the 'static' folder.
        width - Width of the image in inches.
        height - height of the image in inches.
        """
        logo_path = find(BASE_DIR.joinpath('static/' + kwargs.get('path')))
        logo = ImageReader(logo_path)
        logo_width, logo_height = logo.getSize()
        aspect_ratio = logo_height / logo_width
        image = Image(logo_path, width=kwargs.get('width') * inch, height=(kwargs.get('height') * inch) * aspect_ratio)
        return image

    def get_title_p(self, title: str, description: str, is_bold: bool = True):
        """
        Arguments:

        title.
        description.
        is_bold (True) - Whether text1 should be bold or not.
        """
        paragraph1 = self.get_p(title, is_bold=is_bold, textColor='#727cf5', )
        paragraph2 = self.get_p(description)
        address = [paragraph1, Spacer(0, 2), paragraph2]
        return address

    @staticmethod
    def get_p(text, **kwargs):
        """
        Arguments:

        style ('Normal') - 'Heading1', 'Heading6', 'Title', 'Code', 'Bullet', etc.
        leading (14) - Line height.
        fontSize (10).
        textColor ('#6c757d').
        alignment (0): left-0, center-1, right-2.
        is_bold (False).
        """
        styles = getSampleStyleSheet()
        style = styles[kwargs.get('style', 'Normal')]
        style.textColor = colors.HexColor(kwargs.get('textColor', '#6c757d'))
        style.alignment = kwargs.get('alignment', 0)

        if 'style' not in kwargs:
            style.leading = kwargs.get('leading', 14)
            style.fontSize = kwargs.get('fontSize', 10)

        return Paragraph(f'<b>{text}</b>' if kwargs.get('is_bold', False) else text, style)

    @staticmethod
    def get_table_styles(**kwargs):
        """
        Arguments:

        valign, align.
        text_color, bg_color, row_colors, column_colors.
        grid_weight, grid_color, box_weight, box_color, line_before_weight, line_before_color.
        padding_x, padding_y, padding.
        """

        def get_color(key):
            # Returns if the color is present else transparent.
            return colors.HexColor(kwargs.get(key)) if kwargs.get(key) else colors.transparent

        styles = [
            # alignment
            ('VALIGN', (0, 0), (-1, -1), kwargs.get('valign', 'MIDDLE')),
            ('ALIGN', (0, 0), (-1, -1), kwargs.get('align', 'LEFT')),

            # colors
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor(kwargs.get('text_color', '#6c757d'))),
            ('BACKGROUND', (0, 0), (-1, -1), get_color('bg_color')),

            # border
            ('INNERGRID', (0, 0), (-1, -1), kwargs.get('grid_weight', 0), get_color('grid_color')),
            ('BOX', (0, 0), (-1, -1), kwargs.get('box_weight', 0), get_color('box_color')),
            ('LINEBEFORE', (0, 0), (-1, -1), kwargs.get('line_before_weight', 0), get_color('line_before_color')),

            # padding
            ('LEFTPADDING', (0, 0), (-1, -1), kwargs.get('padding_x', 14)),
            ('RIGHTPADDING', (0, 0), (-1, -1), kwargs.get('padding_x', 14)),
            ('TOPPADDING', (0, 0), (-1, -1), kwargs.get('padding_y', 12)),
            ('BOTTOMPADDING', (0, 0), (-1, -1), kwargs.get('padding_y', 12)),
        ]

        if 'rowBg' in kwargs:
            row_colors = kwargs.get('row_colors', [colors.transparent, colors.HexColor('#f0f1f3')])
            styles.insert(0, ('ROWBACKGROUNDS', (0, 0), (-1, -1), row_colors))

        if 'columnBg' in kwargs:
            column_colors = kwargs.get('column_colors', [colors.transparent, colors.HexColor('#f0f1f3')])
            styles.insert(0, ('COLUMNBACKGROUNDS', (0, 0), (-1, -1), column_colors))

        if 'padding' in kwargs:
            styles.append(('LEFTPADDING', (0, 0), (-1, -1), kwargs.get('padding')))
            styles.append(('RIGHTPADDING', (0, 0), (-1, -1), kwargs.get('padding')))
            styles.append(('TOPPADDING', (0, 0), (-1, -1), kwargs.get('padding')))
            styles.append(('BOTTOMPADDING', (0, 0), (-1, -1), kwargs.get('padding')))

        return styles
