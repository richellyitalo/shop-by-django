from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from datetime import datetime
from django.urls import reverse
from .models import Todo, Imagem
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView, DetailView


def tempo_atual(request):
    agora = datetime.now()
    http = "<html><body>Agora são %s<br/>Link: <a href='%s'>Link para nome</a></body></html>" % (
        agora, reverse('todos:view'))
    return HttpResponse(http)


@require_GET
def view(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        raise Http404('Todo não encontrado.')
    return render(request, 'todos/view.html', {'todo': todo, 'imagens': todo.imagem_set.all()})

    # tpl = TemplateResponse(request, 'todos/view.html', {'todo': todo, 'imagens': todo.imagem_set.all()})
    # return tpl.render()



class TodoListView(ListView):
    model = Todo
    context_object_name = 'teste'
    # queryset = Todo.objects.filter(titulo__contains='todo')

    def head(self, *args, **kwargs):
        last_todo = self.get_queryset().last('created_at')

        response = HttpResponse('Lista-todos')
        response['Last-Modified'] = last_todo.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['ultimas_imagens'] = Imagem.get_ultimas(3)
        context['ultimas_imagens'] = Imagem.objects.pegar_ultimas(3)
        return context


# Templates views
# https://docs.djangoproject.com/en/2.2/topics/class-based-views/
class SobreView(TemplateView):
    template_name = 'misc/sobre.html'


class TodoDetail(DetailView):
    model = Todo
    queryset = Todo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imagens'] = self.object.imagem_set.all()
        return context


