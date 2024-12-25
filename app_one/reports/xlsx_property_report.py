from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter

class XlsxPropertyReport(http.Controller):

    @http.route('/property/excel/report/<string:property_ids>',type='http',auth='user')
    def download_property_excel_report(self,property_ids):
        property_ids=request.env['property'].browse(literal_eval(property_ids))
        output=io.BytesIO()
        workbook=xlsxwriter.Workbook(output,{'in_memory':True})
        worksheet=workbook.add_worksheet('Properties')
        header_format=workbook.add_format({'bold':True,
                                           'bg_color':'gray',
                                           'border':1,
                                           'align':'center'})
        string_format=workbook.add_format({'bold':True,
                                           'align':'center'})
        #for currency formate 
        # price_format=workbook.add_format({'num_format':'$##,##00.000'})
        
        headers=['Name','Post code','Bedrooms']
        
        for col_num,header in enumerate(headers):
            worksheet.write(0,col_num,header,header_format)

        row_num=1
        for property in property_ids:
            worksheet.write(row_num,0,property.name,string_format)
            worksheet.write(row_num,1,property.postcode,string_format)
            worksheet.write(row_num,2,property.bed_rooms,string_format)
            #for boolean type
            #worksheet.write(row_num,3,'Yes' if property.field else 'No',string_format)
            row_num+=1
        
        workbook.close()
        output.seek(0)
        file_name='Property Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment;filname={file_name}')
            ]
        )