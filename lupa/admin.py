from celery import chain
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
import nested_admin
from ordered_model.admin import OrderedModelAdmin

from lupa.cache import (
    ENTITY_KEY_PREFIX,
    DATA_ENTITY_KEY_PREFIX,
    DATA_DETAIL_KEY_PREFIX
)
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
from lupa.tasks import (
    asynch_repopulate_cache_entity,
    asynch_repopulate_cache_data_entity,
    asynch_repopulate_cache_data_detail,
    asynch_remove_from_cache
)


def remove_entity_from_cache(modeladmin, request, queryset):
    key_prefix = ENTITY_KEY_PREFIX
    model_args = ['abreviation']
    proc1 = asynch_remove_from_cache.si(key_prefix, model_args, queryset)
    proc2 = asynch_repopulate_cache_entity.si(
        key_prefix,
        queryset,
    )
    flow = chain(proc1, proc2)
    flow.delay()
    messages.success(
        request,
        'Seu pedido de renovação de cache foi recebido e será processado'
    )


def remove_data_from_cache(modeladmin, request, queryset):
    entity_data_ids = [d.id for d in queryset]
    entity_key_prefix = DATA_ENTITY_KEY_PREFIX
    model_args = ['entity_type.abreviation', 'pk']

    proc1 = asynch_remove_from_cache.si(
        entity_key_prefix,
        model_args,
        queryset
    )

    proc2 = asynch_repopulate_cache_data_entity.si(
        entity_key_prefix,
        queryset
    )

    flow = chain(proc1, proc2)
    flow.delay()

    # Remove related DadoDetalhe from cache
    detail_queryset = DadoDetalhe.objects.filter(
        dado_main__id__in=entity_data_ids
    ).order_by('pk')
    detail_key_prefix = DATA_DETAIL_KEY_PREFIX
    detail_model_args = ['dado_main.entity_type.abreviation', 'pk']

    proc1 = asynch_remove_from_cache.si(
        detail_key_prefix,
        detail_model_args,
        detail_queryset
    )

    proc2 = asynch_repopulate_cache_data_detail.si(
        detail_key_prefix,
        detail_queryset,
    )

    flow = chain(proc1, proc2)

    flow.delay()

    messages.success(
        request,
        'Seu pedido de renovação de cache foi recebido e será processado'
    )


remove_data_from_cache.short_description = 'Renovar o cache'
remove_entity_from_cache.short_description = 'Renovar o cache'


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
                'cache_timeout_days',
                'last_cache_update'
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
                'cache_timeout_days',
                'last_cache_update'
            )
        })
    )
    filter_horizontal = ('roles_allowed', )
    inlines = [ColunaDadoAdminInline, DadoDetalheAdminInline, ]
    search_fields = [
        'title',
        'exibition_field'
    ]

    @classmethod
    def _get_entities(cls, queryset):
        entidades = queryset\
            .order_by('entity_type__name')\
            .distinct('entity_type__name')\
            .values_list('entity_type__name', flat=True)
        return [i for i in entidades]

    @classmethod
    def _valida_entidade_detailer(cls, request, entidades):
        if len(entidades) == 1:
            return True

        messages.error(
            request,
            f'Foram selecionados dados de '
            f'{len(entidades)} entidades diferentes. '
            f'Selecione apenas dados de uma mesma entidade.'
        )
        return False

    @classmethod
    def _render_changer(cls, request, queryset):
        entidades = DadoEntidadeAdmin._get_entities(queryset)
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

    def _execute_change(self, request, queryset):
        dado_base = DadoEntidade.objects.get(
            id=request.POST['dado_base']
        )

        for dado_changer in queryset:
            dado_changer.copy_to_detail(dado_base)

        self.message_user(
            request,
            f'Caixinhas alteradas para detalhes de {dado_base}'
        )
        return

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
        entidades = DadoEntidadeAdmin._get_entities(queryset)
        if not self._valida_entidade_detailer(request, entidades):
            return

        if 'apply' in request.POST:
            return self._execute_change(request, queryset)

        return DadoEntidadeAdmin._render_changer(request, queryset)

    move_dado_to_position.short_description = "Mover para Posição..."
    change_to_detail.short_description = "Transformar em detalhe..."
    actions = [
        'change_to_detail',
        remove_data_from_cache,
        'move_dado_to_position'
    ]


admin.site.register(Grupo)
admin.site.register(TipoDado)
admin.site.register(TemaDado)
