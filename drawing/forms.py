# -*- coding: utf-8 -*-
from django import forms

NO_OF_HRS = (('1.0','1.0'),
             ('1.1','1.1'),
             ('1.2','1.2')
             )

CHOICES = (('1', 'Карандашный рисунок',), ('2', 'Старинное фото',),('3', 'Серый цвет',),('4', 'Контур',),('5', 'Водяные знак',),)

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл',
        error_messages={'required': 'Файл не выбран!!!'}
    )

    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label="Выберите фильтр:")


    alpha = forms.CharField(widget=forms.Select(choices=NO_OF_HRS),
    label="Коэффициент",
    max_length=3)

