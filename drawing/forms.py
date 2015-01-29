# -*- coding: utf-8 -*-
from django import forms

NO_OF_HRS = (('1.0','1.0'),
             ('1.1','1.1'),
             ('1.2','1.2')
             )

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл',
        error_messages={'required': 'Файл не выбран!!!'}
    )
    find_contur = forms.BooleanField(
        help_text='Контур изображения',
        initial=False, required=False
    )

    alpha = forms.CharField(widget=forms.Select(choices=NO_OF_HRS),
    label="Коэффициент",
    max_length=3)

    sepia = forms.BooleanField(
        help_text='Старинное фото',
        initial=False, required=False
    )