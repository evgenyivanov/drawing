# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont, ImageEnhance
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from drawing.forms import DocumentForm



def add_watermark(in_file, text, angle=45, opacity=0.35):
    FONT=os.path.join(os.path.dirname(__file__), 'ARIAL.TTF')
    img = in_file.convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font)
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    return Image.composite(watermark, img, watermark)




def make_linear_ramp(white):
    # putpalette expects [r,g,b,r,g,b,...]
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
    return ramp

def dodge(a, b, alpha):
    return min(int(a*255/(256-b*alpha)), 255)



def home(request):
    # Handle file upload
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():

            filters_type = int(form.cleaned_data['choice_field'])

            if filters_type == 3:
                im1 = Image.open(request.FILES['docfile']).convert('LA')
                response = HttpResponse(mimetype="image/png")
                im1.save(response, "PNG")
                return response

            if filters_type == 4:
                im1 = Image.open(request.FILES['docfile']).convert('L')
                im1 = im1.filter(ImageFilter.CONTOUR)
                response = HttpResponse(mimetype="image/png")
                im1.save(response, "PNG")
                return response

            if filters_type == 5:
                im1 = Image.open(request.FILES['docfile'])
                im1 = add_watermark(im1,'JULIA CORONELLI ARCHIVE')
                response = HttpResponse(mimetype="image/png")
                im1.save(response, "PNG")
                return response




            alpha = float(form.cleaned_data['alpha'])

            im1 = Image.open(request.FILES['docfile']).convert('L')
            im2 = im1.copy()

            im2 = ImageOps.invert(im2)


            for i in range(25):
                im2 = im2.filter(ImageFilter.BLUR)

            width, height = im1.size

            for x in range(width):
                for y in range(height):
                    a = im1.getpixel((x, y))
                    b = im2.getpixel((x, y))
                    im1.putpixel((x, y), dodge(a, b, alpha))



            if filters_type == 2:
                sepia = make_linear_ramp((255, 240, 192))
                #im1 = ImageOps.autocontrast(im1)
                HttpResponse(4)
                im1.putpalette(sepia)


            response = HttpResponse(mimetype="image/png")
            im1.save(response, "PNG")
            return response

    else:
        form = DocumentForm(initial={'alpha': '1.1','choice_field':'1'}) # A empty, unbound form



    # Render list page with the documents and the form
    return render_to_response(
        'home.html',
        { 'form': form},
        context_instance=RequestContext(request)
    )