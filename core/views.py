from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
class ReporteFacturaPDF(View):
    def cabecera(self, pdf):
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/fish.png'
        pdf.drawImage(archivo_imagen, 40,750,120,90,preserveAspectRatio=True)

        pdf.setFont("Helvetica",16)
        pdf.drawString(230,790,"REPORTE FACTURA")
        pdf.setFont("Helvetica",14)
        pdf.drawString(200,770,"La Paz - Bolivia")

    def tabla(self,pdf, y):
        # Encabezado para la tabla
        cabezera = ('CANT.','DESCRIPCIÓN','PRECIO UNITARIO','IMPORTE')
        
        # Contenido de la tabla
        contenido = ["1","Contenidos Media","50","50"]

        # Tamanio de las columnas
        tamanio = Table([cabezera]+contenido,colWidths=[2 * cm, 5 * cm, 5 * cm, 5 * cm])

        # Estilos a las celdas de la tabla
        tamanio.setStyle(TableStyle(
            [
                #La primera fila(encabezado) centrada
                ('ALIGN',(0,0),(3,0),1,colors.black),
                #tamaño de letra 10
                ('FONTSIZE',(0,0),(-1,-1),10),
            ]
        )) 

        # Tamanio de la hoja que ocupara la tabla
        tamanio.wrapOn(pdf, 800,600)
        # Coordenadas donde se dibujara la tabla
        tamanio.drawOn(pdf,60,560)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

""" # Create your views here.
def some_view(request):
    # Crear un archivo parecido a un buffer 
    # para recibir datos de pdf
    buffer = io.BytesIO()

    # Crear el objeto PDF, usando el buffer
    # como su "archivo"

    p = canvas.Canvas(buffer)
    p.drawString(100,100,"Hello world.")


    p.showPage()
    p.save()

    buffer.seek(0)  

    return FileResponse(buffer,as_attachment=True, filename='hello.pdf') """