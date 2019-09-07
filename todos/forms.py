from django import forms


class FormBootstrap(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


ASSUNTOS_CHOICES = [
    ('comercial', 'Comercial'),
    ('financeiro', 'Financeiro'),
]


class ContactForm(forms.Form):
    class Media:
        css = {
            'all': ('todo-contato.css',),
        }
        js = ('todo-contato.js',)

    attrs_bs = {'class': 'form-control'}

    nome = forms.CharField(widget=forms.TextInput(attrs=attrs_bs), label='Informe seu nome')
    email = forms.EmailField(widget=forms.EmailInput(attrs=attrs_bs))
    mensagem = forms.CharField(widget=forms.Textarea(attrs=attrs_bs))
    assunto = forms.ChoiceField(
        widget=forms.Select(attrs=attrs_bs),
        choices=ASSUNTOS_CHOICES
    )


    def enviar_email(self):
        print(self.cleaned_data)
        print('------------- enviar ----------------')
