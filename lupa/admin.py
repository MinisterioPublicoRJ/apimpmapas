from operator import attrgetter

from django.contrib import admin
from django.core.cache import cache as django_cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
import nested_admin
from ordered_model.admin import OrderedModelAdmin

from lupa.cache import wildcard_cache_key
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


def _remove_from_cache(key_prefix, model_args, queryset):
    cache_client = django_cache.get_master_client()
    for obj in queryset:
        key_args = [
            attrgetter(arg)(obj) for arg in model_args
        ]
        key = wildcard_cache_key(key_prefix, key_args)
        cache_keys = cache_client.keys(key)
        [cache_client.delete(cache_key) for cache_key in cache_keys]


def remove_entity_from_cache(modeladmin, request, queryset):
    key_prefix = 'lupa_entidade'
    model_args = ['abreviation']
    _remove_from_cache(key_prefix, model_args, queryset)


def remove_data_from_cache(modeladmin, request, queryset):
    key_prefix = 'lupa_dado'
    model_args = ['entity_type.abreviation', 'pk']
    _remove_from_cache(key_prefix, model_args, queryset)


remove_data_from_cache.short_description = 'Remove do cache'
remove_entity_from_cache.short_description = 'Remove do cache'


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
                'osm_default_level',
                'is_cacheable',
                'cache_timeout'
            )
        })
    )
    filter_horizontal = ('roles_allowed', )
    inlines = [MapaAdminInline]
    actions = [remove_entity_from_cache]


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
                'table',
                'is_cacheable',
                'cache_timeout'
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

    move_dado_to_position.short_description = "Mover para Posição..."
    actions = ['move_dado_to_position', remove_data_from_cache]


admin.site.register(Grupo)
admin.site.register(TipoDado)
admin.site.register(TemaDado)
