from reportlab.lib import colors
from reportlab.platypus import Paragraph, Image, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.contrib.staticfiles.finders import find
from my_project.settings import BASE_DIR
import decimal


class BaseReportLabPlatypus:

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
        paragraph1 = self.get_p(title, is_bold=is_bold, text_color='#727cf5')
        paragraph2 = self.get_p(description)
        address = [paragraph1, Spacer(0, 2), paragraph2]
        return address

    @staticmethod
    def get_p(text, **kwargs):
        """
        Arguments:

        style ('Normal') - 'Heading1', 'Heading6', 'Title', 'Code', 'Bullet', etc.
        leading (14) - Line height.
        font_size (10).
        text_color ('#6c757d').
        alignment (0) - left-0, center-1, right-2.
        is_bold (False).
        text_transform (None) - uppercase, lowercase, None
        """
        styles = getSampleStyleSheet()
        style = styles[kwargs.get('style', 'Normal')]
        style.textColor = colors.HexColor(kwargs.get('text_color', '#6c757d'))
        style.alignment = kwargs.get('alignment', 0)
        style.textTransform = kwargs.get('text_transform')

        if 'style' not in kwargs:
            style.leading = kwargs.get('leading', 14)
            style.fontSize = kwargs.get('font_size', 10)

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


class InvoiceReportLabPlatypus(BaseReportLabPlatypus):

    def __init__(self, invoice, items):
        self.invoice = invoice
        self.items = items

    def get_pdf_content(self):
        header = self.get_header()
        body = self.get_body()
        footer = self.get_footer()

        return header + [Spacer(0, 30)] + body + [Spacer(0, 50)] + footer

    def get_header(self):
        # logo
        logo = self.get_logo(path='assets/logo.png', width=0.5, height=0.5)

        # address
        address = f'''{self.invoice.sender_address_line1}<br/>{self.invoice.sender_address_line2}<br/>
                      {self.invoice.sender_country}'''
        sender_p = self.get_title_p(self.invoice.sender_name, address)

        # table
        table = Table([[logo, sender_p]], colWidths=[320, 180])
        styles = self.get_table_styles()
        table.setStyle(TableStyle(styles))
        return [table]

    def get_body(self):
        # table1
        table1_left_content = f'Invoice #{self.invoice.invoice_number}'
        table1_left = self.get_p(table1_left_content, style='Heading1', text_color='#ffffff')

        date = self.invoice.created_at.strftime('%b %d, %Y')
        time = self.invoice.created_at.strftime('%I:%M %p')
        table1_right = Table([
            ['Order', self.get_p(f'#{self.invoice.order_number}', text_color='#ffffff', alignment=2, is_bold=True)],
            ['Date', self.get_p(date, text_color='#ffffff', alignment=2, is_bold=True)],
            ['Time', self.get_p(time, text_color='#ffffff', alignment=2, is_bold=True)]
        ])
        table1_right_styles = self.get_table_styles(text_color='#ffffff', bg_color='#727cf5', padding=0)
        table1_right.setStyle(TableStyle(table1_right_styles))

        table1 = Table([[table1_left, table1_right]], colWidths=[320, 180])
        table1_styles = self.get_table_styles(bg_color='#000865')
        table1_styles += [('BACKGROUND', (-1, -1), (-1, -1), colors.HexColor('#727cf5'))]
        table1.setStyle(TableStyle(table1_styles))

        # table2
        table2_left_content = f'''{self.invoice.recipient_name}<br/>{self.invoice.recipient_address_line1}<br/>
                                  {self.invoice.recipient_address_line2}<br/>{self.invoice.recipient_country}<br/>
                                  T: {self.invoice.recipient_phone}'''
        table2_left = self.get_p(table2_left_content)

        table2_right = [self.get_title_p('Shipping Method', self.invoice.shipping_type), Spacer(0, 15),
                        self.get_title_p('Payment Method', self.invoice.payment_type)]

        table2 = Table([[table2_left, table2_right]], colWidths=[320, 180])
        table2_styles = self.get_table_styles(padding_y=0, line_before_weight=1, line_before_color='#f0f1f3')
        table2.setStyle(TableStyle(table2_styles))

        # table3
        table3_content = [['Items', 'Qty', 'Subtotal']]
        for item in self.items:
            row = [self.get_title_p(item.name, f'SKU: {item.sku}', False), self.get_p(str(item.quantity)),
                   self.get_p('${:.2f}'.format(item.price), alignment=2)]
            table3_content.append(row)

        table3 = Table(table3_content, colWidths=[250, 125, 125])
        table3_styles = self.get_table_styles(text_color='#ffffff', rowBg=None, padding=6)
        table3_styles += [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#727cf5')),
                          ('ALIGN', (-1, 0), (-1, 0), 'RIGHT')]
        table3.setStyle(TableStyle(table3_styles))

        # table4
        sub_total = sum(item.price for item in self.items)
        discount = sum((item.price * (decimal.Decimal(item.discount or 0) / 100)) for item in self.items)
        tax = sub_total * decimal.Decimal(5 / 100)
        charges = decimal.Decimal(2.00)
        grand_total = sub_total - discount + tax + charges
        table4_content = [
            ['', self.get_p('Subtotal', alignment=2), self.get_p('${:.2f}'.format(sub_total), alignment=2)],
            ['', self.get_p('Discount', alignment=2), self.get_p('- ${:.2f}'.format(discount), alignment=2, text_color='#169955')],
            ['', self.get_p('Tax', alignment=2), self.get_p('${:.2f}'.format(tax), alignment=2)],
            ['', self.get_p('Shipping & Handling', alignment=2), self.get_p('${:.2f}'.format(charges), alignment=2)],
            ['', self.get_p('Grand Total', alignment=2, is_bold=True, text_color='#727cf5'),
             self.get_p('${:.2f}'.format(grand_total), alignment=2, is_bold=True, text_color='#727cf5')],
        ]
        table4 = Table(table4_content, colWidths=[250, 125, 125])
        table4_styles = self.get_table_styles(align='RIGHT', grid_weight=1, box_weight=1, grid_color='#ffffff',
                                              box_color='#ffffff', padding=6)
        table4_styles += [('BACKGROUND', (-1, 0), (-1, -1), colors.HexColor('#f0f1f3'))]
        table4.setStyle(TableStyle(table4_styles))

        return [table1, Spacer(0, 30), table2, Spacer(0, 30), table3, table4]

    def get_footer(self):
        content1 = 'Thank you for your order!'
        content2 = 'If you have any questions about your order, you can email us at sales@django.com'

        content1_p = self.get_p(content1, style='Heading2', is_bold=True, text_color='#727cf5', alignment=1,
                                text_transform='uppercase')
        content2_p = self.get_p(content2, alignment=1)

        return [content1_p, content2_p]
