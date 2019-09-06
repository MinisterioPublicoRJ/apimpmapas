from django.contrib import admin
from django import forms
import nested_admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    Dado,
    Icone,
    Entidade,
    Mapa,
    TipoDado,
    TemaDado,
    ColunaDado,
    ColunaMapa
)


class ColunaDadoForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaDado.INFO_CHOICES,
        help_text=ColunaDado.help_info_type
    )


class ColunaMapaForm(forms.ModelForm):
    info_type = forms.ChoiceField(
        choices=ColunaMapa.INFO_CHOICES,
        help_text=ColunaMapa.help_info_type
    )


class ColunaDadoAdminInline(admin.TabularInline):
    model = ColunaDado
    form = ColunaDadoForm


class ColunaMapaAdminInline(nested_admin.NestedTabularInline):
    model = ColunaMapa
    form = ColunaMapaForm


class MapaAdminInline(nested_admin.NestedStackedInline):
    model = Mapa
    inlines = [ColunaMapaAdminInline]


@admin.register(Entidade)
class EntidadeAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'abreviation')
    fieldsets = (
        (None, {
            'fields': ('name', 'abreviation')
        }),
        ('Dados principais', {
            'fields': (
                'database',
                'schema',
                'table',
                'id_column',
                'name_column')
        })
    )
    inlines = [MapaAdminInline]


@admin.register(Dado)
class DadoAdmin(OrderedModelAdmin):
    list_display = ('title', 'entity_type', 'theme', 'move_up_down_links')
    list_filter = ('entity_type__name',)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'exibition_field',
                'data_type',
                'entity_type',
                'theme',
                'icon'
            )
        }),
        ('Dados exibidos', {
            'fields': (
                'database',
                'schema',
                'table')
        })
    )
    inlines = [ColunaDadoAdminInline]


admin.site.register(Icone)
admin.site.register(TipoDado)
admin.site.register(TemaDado)
