from celery import chain
from django.contrib import admin
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
from lupa.serializers import (
    EntidadeSerializer,
    DadoEntidadeSerializer,
    DadoDetalheSerializer)
from lupa.tasks import (
    asynch_repopulate_cache_entity,
    asynch_repopulate_cache_data_entity,
    asynch_repopulate_cache_data_detail,
    asynch_remove_from_cache
)


def remove_entity_from_cache(modeladmin, request, queryset):
    key_prefix = 'lupa_entidade'
    model_args = ['abreviation']
    proc1 = asynch_remove_from_cache.si(key_prefix, model_args, queryset)
    proc2 = asynch_repopulate_cache_entity.si(
        key_prefix,
        queryset,
        EntidadeSerializer
    )
    flow = chain(proc1, proc2)
    flow.delay()


def remove_data_from_cache(modeladmin, request, queryset):
    entity_data_ids = [d.id for d in queryset]
    entity_key_prefix = 'lupa_dado_entidade'
    model_args = ['entity_type.abreviation', 'pk']

    proc1 = asynch_remove_from_cache.si(
        entity_key_prefix,
        model_args,
        queryset
    )

    proc2 = asynch_repopulate_cache_data_entity.si(
        entity_key_prefix, queryset, DadoEntidadeSerializer
    )

    flow = chain(proc1, proc2)
    flow.delay()

    # Remove related DadoDetalhe from cache
    detail_queryset = DadoDetalhe.objects.filter(
        dado_main__id__in=entity_data_ids
    ).order_by('pk')
    detail_key_prefix = 'lupa_dado_detalhe'
    detail_model_args = ['dado_main.entity_type.abreviation', 'pk']

    proc1 = asynch_remove_from_cache.si(
        detail_key_prefix,
        detail_model_args,
        detail_queryset
    )

    proc2 = asynch_repopulate_cache_data_detail.si(
        detail_key_prefix,
        detail_queryset,
        DadoDetalheSerializer,
    )

    flow = chain(proc1, proc2)

    flow.delay()


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
                'cache_timeout_days'
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
                'cache_timeout_days'
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
