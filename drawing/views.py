# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from drawing.forms import DocumentForm


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