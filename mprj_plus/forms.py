import re

import xml.etree.cElementTree as et

from django import forms

from .models import Area, Tema, Icone
# from .scrapper import tableau_data

ERRORS = {
    'SVG_FILE_ABSENT': 'É necessário prover um ícone no formato SVG',
    'NOT_SVG': 'O arquivo submetido não é um SVG',
    'BLANK_FIELD': 'O campo não deve estar em branco',
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    'NOT_COLOR': 'O campo deve conter uma string de cor válida no '
                 'formato #FFFFFF'
=======
    'NOT_COLOR': 'O campo deve conter uma string de cor válida no formato #FFFFFF'
>>>>>>> Mprj + funcional
=======
    'NOT_COLOR': 'O campo deve conter uma string de cor válida no '
                 'formato #FFFFFF'
>>>>>>> Correção de flake8
=======
    'NOT_COLOR': 'O campo deve conter uma string de cor válida no formato #FFFFFF'
>>>>>>> Mprj + funcional
=======
    'NOT_COLOR': 'O campo deve conter uma string de cor válida no '
                 'formato #FFFFFF'
>>>>>>> Correção de flake8
}


class IconeForm(forms.ModelForm):
    image = forms.FileField()
    image_original = None

    class Meta:
        model = Icone
        fields = ['nome', 'image']

    def __init__(self, *args, **kwargs):
        super(IconeForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        if 'image' in kwargs:
            self.image_original = self.initial['image']

    def clean_image(self):
        file = self.files.get('image')
        if not file:
            if self.image_original:
                return self.image_original
            else:
                raise forms.ValidationError(ERRORS['SVG_FILE_ABSENT'])
        else:
            tag = None
            try:
                for event, el in et.iterparse(file, ('start',)):
                    tag = el.tag
                    break
            except et.ParseError:
                raise forms.ValidationError(ERRORS['NOT_SVG'])

            if not tag == '{http://www.w3.org/2000/svg}svg':
                raise forms.ValidationError(ERRORS['NOT_SVG'])

        file.seek(0)
        return file.read().decode()


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome', 'cor', 'icone', 'prioridade']

    def clean_nome(self):
        if self.nome.isspace():
            raise forms.ValidationError(ERRORS['BLANK_FIELD'])
        return self.nome

    def clean_cor(self):
        color_regex = r'^#([a-f0-9]{6})$'
        if re.match(color_regex, self.cor, re.IGNORECASE):
            return self.cor
        raise forms.ValidationError(ERRORS['NOT_COLOR'])


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = '__all__'

    def clean_titulo(self):
        if self.titulo.isspace():
            raise forms.ValidationError(ERRORS['BLANK_FIELD'])
        return self.titulo

    def clean_subtitulo(self):
        if self.subtitulo.isspace():
            raise forms.ValidationError(ERRORS['BLANK_FIELD'])
        return self.subtitulo

    def clean_fonte_dados(self):
        if self.fonte_dados.isspace():
            raise forms.ValidationError(ERRORS['BLANK_FIELD'])
        return self.fonte_dados
