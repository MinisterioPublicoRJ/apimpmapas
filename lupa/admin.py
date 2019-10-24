from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
import nested_admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    DadoDetalhe,
    DadoEntidade,
    Entidade,
    Grupo,
    Mapa,
    TipoDado,
    TemaDado,
    ColunaDado,
    ColunaDetalhe,
    ColunaMapa,
)


class ColunaDadoForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaDado.INFO_CHOICES,
        help_text=ColunaDado.help_info_type
    )


class ColunaDetalheForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaDetalhe.INFO_CHOICES,
        help_text=ColunaDetalhe.help_info_type
    )


class ColunaMapaForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaMapa.INFO_CHOICES,
        help_text=ColunaMapa.help_info_type
    )


class ColunaDadoAdminInline(nested_admin.NestedTabularInline):
    model = ColunaDado
    form = ColunaDadoForm


class ColunaMapaAdminInline(nested_admin.NestedTabularInline):
    model = ColunaMapa
    form = ColunaMapaForm


class MapaAdminInline(nested_admin.NestedStackedInline):
    model = Mapa
    inlines = [ColunaMapaAdminInline]


class ColunaDetalheAdminInline(nested_admin.NestedTabularInline):
    model = ColunaDetalhe
    form = ColunaDetalheForm


class DadoDetalheAdminInline(nested_admin.NestedStackedInline):
    model = DadoDetalhe
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'exibition_field',
                'data_type',
                'limit_fetch',
            )
        }),
        ('Dados exibidos', {
            'fields': (
                'database',
                'schema',
                'table'
            )
        })
    )
    inlines = [ColunaDetalheAdminInline]


@admin.register(Entidade)
class EntidadeAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'abreviation')
    fieldsets = (
        (None, {
            'fields': ('name', 'abreviation', 'roles_allowed')
        }),
        ('Dados principais', {
            'fields': (
                'database',
                'schema',
                'table',
                'id_column',
                'name_column',
                'geojson_column',
                'osm_value_attached',
                'osm_default_level'
            )
        })
    )
    filter_horizontal = ('roles_allowed', )
    inlines = [MapaAdminInline]


@admin.register(DadoEntidade)
class DadoEntidadeAdmin(nested_admin.NestedModelAdmin, OrderedModelAdmin):
    list_display = (
        'title',
        'entity_type',
        'theme',
        'show_box',
        'order',
        'move_up_down_links',
    )
    ordering = ('order',)
    list_filter = ('entity_type__name', 'show_box',)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'exibition_field',
                'data_type',
                'entity_type',
                'theme',
                'icon',
                'limit_fetch',
                'roles_allowed',
                'show_box',
            )
        }),
        ('Dados exibidos', {
            'fields': (
                'database',
                'schema',
                'table'
            )
        })
    )
    filter_horizontal = ('roles_allowed', )
    inlines = [ColunaDadoAdminInline, DadoDetalheAdminInline, ]
    search_fields = [
        'title',
        'exibition_field'
    ]

    def move_dado_to_position(self, request, queryset):
        if 'apply' in request.POST:
            dado = queryset[0]
            dado.to(int(request.POST['new_order']))

            self.message_user(
                request,
                f'Atualizei a ordem da caixinha {dado}'
            )

            return HttpResponseRedirect(request.get_full_path())
        return render(
            request,
            'lupa/move_to_position.html',
            context={
                'dado': queryset[0]
            })

    def change_to_detail(self, request, queryset):
        entidades = queryset\
            .order_by('entity_type__name')\
            .distinct('entity_type__name')\
            .values_list('entity_type__name', flat=True)
        if len(entidades) > 1:
            messages.error(
                request,
                f'Foram selecionados dados de '
                f'{len(entidades)} entidades diferentes. '
                f'Selecione apenas dados de uma mesma entidade.'
            )
            return

        if 'apply' in request.POST:
            dado_base = DadoEntidade.objects.filter(
                id=request.POST['dado_base']
            )[0]
            print(dado_base)

            for dado_changer in queryset:
                pass
                dado_changer.copy_to_detail(dado_base)

            self.message_user(
                request,
                f'Caixinhas alteradas para detalhes de {dado_base}'
            )
            return

        entity_id = queryset\
            .order_by('entity_type')\
            .distinct('entity_type')\
            .values_list('entity_type', flat=True)
        possible = DadoEntidade.objects\
            .filter(entity_type__in=entity_id)\
            .exclude(id__in=[q.id for q in queryset])
        return render(
            request,
            'lupa/change_detail.html',
            context={
                'entidade': entidades[0],
                'caixinhas': queryset.all(),
                'possiveis': possible
            })

    move_dado_to_position.short_description = "Mover para Posição..."
    change_to_detail.short_description = "Transformar em detalhe..."
    actions = ['change_to_detail']


admin.site.register(Grupo)
admin.site.register(TipoDado)
admin.site.register(TemaDado)
