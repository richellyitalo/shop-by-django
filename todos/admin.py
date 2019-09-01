from django.contrib import admin
from .models import Todo, Categoria, Imagem
from django import forms
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType


# admin.site.register(Imagem)


class CategoriaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
    exclude = ['user']
    list_display = ('descricao', 'qtd_todos')

    def qtd_todos(self, obj):
        return Todo.objects.filter(categoria=obj).count()

    qtd_todos.short_description = 'Quantidade de todos'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Categoria, CategoriaAdmin)


class ImagemForm(admin.TabularInline):
    model = Imagem


def action_batch_remove_descricao(modeladmin, request, queryset):
    queryset.update(descricao='')


action_batch_remove_descricao.short_description = 'Remover descrição'


class TodoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    exclude = ['user']
    list_display = ('titulo', 'descricao_resumo', 'qtd_imagens', 'categoria')
    inlines = [
        ImagemForm,
    ]
    actions = [
        action_batch_remove_descricao,
        'action_batch_remove_imagens'
    ]

    def action_batch_remove_imagens(self, request, queryset):
        imagens = Imagem.objects.filter(todo__in=queryset.all())
        for imagem in imagens:
            imagem.delete()

    action_batch_remove_imagens.short_description = 'Remover imagens'

    def descricao_resumo(self, obj):
        return obj.descricao[:80] + (' [...]' if len(obj.descricao) > 0 else '-')

    descricao_resumo.short_description = 'Descrição'

    def qtd_imagens(self, obj):
        return Imagem.objects.filter(todo=obj).count()

    qtd_imagens.short_description = 'Imagens'

    # fieldsets = (
    #     ('Dados básicos', {
    #         'classes': ('wide',),
    #         'fields': ('titulo', 'categoria', 'descricao'),
    #     }),
    # )
    # forms = ImagemForm

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Todo, TodoAdmin)