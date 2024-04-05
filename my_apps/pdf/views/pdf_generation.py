from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from my_apps.pdf.report_labs import CustomReportLabMethods


def generate_pdf_view(request):
    """
    It uses reportlab to generate the pdf and send it as a response.
    """
    if request.method == 'GET':
        # disposition: 'inline' will render the pdf, 'attachment' will download the pdf
        disposition = 'attachment' if request.GET.get('download') else 'inline'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="generated_pdf.pdf"'
        pdf = SimpleDocTemplate(response, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

        instance = ReportLabPdfElements()
        header_content = instance.get_pdf_content()
        pdf.build(header_content)
        return response


class ReportLabPdfElements(CustomReportLabMethods):

    def get_pdf_content(self):
        header = self.get_header()
        body = self.get_body()
        return [header, Spacer(0, 30)] + body

    def get_header(self):
        # logo
        logo = self.get_logo(path='assets/logo.png', width=0.5, height=0.5)

        # address
        address_content1 = '<b>Django Project</b>'
        address_content2 = '6162 Honey Bluff Parkway<br/>Calder, Michigan, 34567-8912<br/>United States'
        address = self.get_title_p(address_content1, address_content2)

        # table
        table = Table([[logo, address]], colWidths=[320, 180])
        styles = self.get_table_styles()
        table.setStyle(TableStyle(styles))
        return table

    def get_body(self):
        # table1
        table1_left_content1 = "Invoice #000000006"
        table1_left = self.get_p(table1_left_content1, style='Heading1', textColor='#ffffff')

        table1_right = Table([
            ['Order', self.get_p('#110000000006', textColor='#ffffff', alignment=2, is_bold=True)],
            ['Date', self.get_p('Nov 01, 2024', textColor='#ffffff', alignment=2, is_bold=True)],
            ['Time', self.get_p('12:50 PM', textColor='#ffffff', alignment=2, is_bold=True)]
        ])
        table1_right_styles = self.get_table_styles(text_color='#ffffff', bg_color='#727cf5', padding=0)
        table1_right.setStyle(TableStyle(table1_right_styles))

        table1 = Table([[table1_left, table1_right]], colWidths=[320, 180])
        table1_styles = self.get_table_styles(bg_color='#000865')
        table1_styles += [('BACKGROUND', (-1, -1), (-1, -1), colors.HexColor('#727cf5'))]
        table1.setStyle(TableStyle(table1_styles))

        # table2
        table2_left_content = '''Veronica Costello<br/>6162 Honey Bluff Parkway<br/>Calder, Michigan, 
                                 34567-8912<br/>United States<br/>T: (555) 321-4567'''
        table2_left = self.get_p(table2_left_content)

        table2_right = [self.get_title_p('Shipping Method', 'Flat Rate - Fixed'), Spacer(0, 15),
                        self.get_title_p('Payment Method', 'Check / Money order')]

        table2 = Table([[table2_left, table2_right]], colWidths=[320, 180])
        table2_styles = self.get_table_styles(padding_y=0, line_before_weight=1, line_before_color='#f0f1f3')
        table2.setStyle(TableStyle(table2_styles))

        # table3
        table3_content = [
            ['Items', 'Qty', 'Subtotal'],
            [self.get_title_p('Clamber Watch', 'SKU: 24-WG03', False), self.get_p('2'),
             self.get_p('$100.00', alignment=2)],
            [self.get_title_p('Olivia 1/4 Zip Light Jacket', 'SKU: WJ12-M-Purple', False), self.get_p('1'),
             self.get_p('$77.00', alignment=2)],
            [self.get_title_p('Rival Field Messenger', 'SKU: 24-MB06', False), self.get_p('1'),
             self.get_p('$145.00', alignment=2)]
        ]
        table3 = Table(table3_content, colWidths=[250, 125, 125])
        table3_styles = self.get_table_styles(text_color='#ffffff', rowBg=None, padding_x=4, padding_y=6)
        table3_styles += [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#727cf5')),
                          ('ALIGN', (-1, 0), (-1, 0), 'RIGHT')]
        table3.setStyle(TableStyle(table3_styles))

        # table4
        table4_content = [
            ['', self.get_p('Subtotal', alignment=2), self.get_p('$222.00', alignment=2)],
            ['', self.get_p('Discount', alignment=2), self.get_p('-$24.40', alignment=2)],
            ['', self.get_p('Tax', alignment=2), self.get_p('$36.06', alignment=2)],
            ['', self.get_p('Shipping & Handling', alignment=2), self.get_p('$20.00', alignment=2)],
            ['', self.get_p('Grand Total', alignment=2), self.get_p('$256.66', alignment=2)],
        ]
        table4 = Table(table4_content, colWidths=[250, 125, 125])
        table4_styles = self.get_table_styles(align='RIGHT', grid_weight=1, box_weight=1, grid_color='#ffffff',
                                              box_color='#ffffff', padding_x=4, padding_y=6)
        table4_styles += [('BACKGROUND', (-1, 0), (-1, -1), colors.HexColor('#f0f1f3'))]
        table4.setStyle(TableStyle(table4_styles))

        return [table1, Spacer(0, 30), table2, Spacer(0, 30), table3, table4]
