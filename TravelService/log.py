import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def create_pdf(output="disk_report.pdf"):
    now = datetime.datetime.today()
    date = now.strftime("%h %d %Y %H:%M:%S")
    c = canvas.Canvas(output)
    textobject = c.beginText()
    textobject.setTextOrigin(inch, 11*inch)
    textobject.textLines('''Disk Capcity Report: %s''' %date)
    input = [u'大家好我是吃烧烤戴婧放辣烧烤', u'大家开心吗']
    for line in input:
        textobject.textLine(line.strip())
    c.drawText(textobject)
    c.showPage()
    c.save()


create_pdf()