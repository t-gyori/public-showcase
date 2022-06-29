# root admin meghívása (az energia app az egy biztos pont, biztosan mindig aktív lesz)
# from project_webapp.admin import *

from django.contrib import admin
from django.utils.translation import gettext as _
from import_export import resources
from import_export.admin import ExportMixin
from .models import (KozosAdatTipus,
                     MeresAdatTipus,
                     KozosAdatTipusValtoszam,
                     MeresAdatTipusValtoszam
                     )
from project_webapp.models import EXPORT_TEXTS


class KozosAdatTipusValtoszamInline(admin.StackedInline):
    model = KozosAdatTipusValtoszam
    extra = 0
    readonly_fields = ("letrehozva_ido", "letrehozva_felhasznalo",
                       "modositva_ido", "modositva_felhasznalo", )
    fieldsets = (
        (None, {
            "fields": ("datum_kezdo", "inaktiv", "szorzo_kwh", "szorzo_kwh_forras", "szorzo_kwh_datum", "megjegyzes",)
        }),
        (EXPORT_TEXTS["fieldset1_name"], {
            "classes": ("collapse",),
            "fields": ("letrehozva_ido", "letrehozva_felhasznalo", "modositva_ido", "modositva_felhasznalo", )
        }),
    )


class MeresAdatTipusValtoszamInline(admin.StackedInline):
    model = MeresAdatTipusValtoszam
    extra = 0
    readonly_fields = ("letrehozva_ido", "letrehozva_felhasznalo",
                       "modositva_ido", "modositva_felhasznalo", )
    fieldsets = (
        (None, {
            "fields": (
                "meresadattipus", "datum_kezdo", "inaktiv", "szorzo_kwh", "szorzo_kwh_forras", "szorzo_kwh_datum",
                "szorzo_t_co2", "szorzo_t_co2_forras", "szorzo_t_co2_datum", "megjegyzes",
            )
        }),
        (EXPORT_TEXTS["fieldset1_name"], {
            "classes": ("collapse",),
            "fields": ("letrehozva_ido", "letrehozva_felhasznalo", "modositva_ido", "modositva_felhasznalo", )
        }),
    )


class KozosAdatTipusResource(resources.ModelResource):
    """
    Ez a django-import-export package beállításait tartalmazza.
    """
    class Meta:
        model = KozosAdatTipus
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True
        fields = ("id", "nev_teljes", "mertekegyseg",
                  "mennyiseg", "energia", )
        export_order = fields

    def dehydrate_mennyiseg(self, KozosAdatTipus):
        if KozosAdatTipus.mennyiseg:
            return EXPORT_TEXTS["yes"]
        else:
            return EXPORT_TEXTS["no"]

    def dehydrate_energia(self, KozosAdatTipus):
        if KozosAdatTipus.energia:
            return EXPORT_TEXTS["yes"]
        else:
            return EXPORT_TEXTS["no"]


class MeresAdatTipusResource(resources.ModelResource):
    """
    Ez a django-import-export package beállításait tartalmazza.
    """
    class Meta:
        model = MeresAdatTipus
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True
        fields = ("id", "nev_teljes", "mertekegyseg",
                  "kozosadattipus", )
        export_order = fields


@admin.register(KozosAdatTipus)
class KozosAdatTipusAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = KozosAdatTipusResource
    inlines = [KozosAdatTipusValtoszamInline]
    save_as = True
    list_filter = ()
    list_display = ("id", "nev_teljes", "mertekegyseg",
                    "modositva_ido", "modositva_felhasznalo",)
    list_display_links = ("nev_teljes", )
    search_fields = ("nev_teljes", "mertekegyseg",)
    readonly_fields = ("letrehozva_ido", "letrehozva_felhasznalo",
                       "modositva_ido", "modositva_felhasznalo", "nev_slug",)
    fieldsets = (
        (None, {
            "fields": ("nev_teljes", "mertekegyseg", "mennyiseg", "energia", "inaktiv", "megjegyzes",)
        }),
        (EXPORT_TEXTS["fieldset1_name"], {
            "classes": ("collapse",),
            "fields": ("nev_teljes_mgh", "letrehozva_ido", "letrehozva_felhasznalo", "modositva_ido", "modositva_felhasznalo", "nev_slug",)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Ez kell ahhoz, hogy mentéskor beírja az aktív felhasználót a
        léterehozó és a módosító személy mezőkbe *ezen* a modellen.
        """
        obj.user = request.user
        obj.letrehozva_felhasznalo = obj.user
        obj.modositva_felhasznalo = obj.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        Ez kell ahhoz, hogy mentéskor beírja az aktív felhasználót a
        léterehozó és a módosító személy mezőkbe az *inline* modelleken.
        Note: az inline modellre emiatt külön nem került save_model override.
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.letrehozva_felhasznalo = instance.user
            instance.modositva_felhasznalo = instance.user
            instance.save()
        formset.save_m2m()


@admin.register(MeresAdatTipus)
class MeresAdatTipusAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = MeresAdatTipusResource
    inlines = [MeresAdatTipusValtoszamInline]
    save_as = True
    list_filter = ("kozosadattipus", )
    list_display = ("id", "nev_teljes", "mertekegyseg", "kozosadattipus",
                    "modositva_ido", "modositva_felhasznalo",)
    list_display_links = ("nev_teljes", )
    search_fields = ("nev_teljes", "mertekegyseg", "kozosadattipus",)
    readonly_fields = ("letrehozva_ido", "letrehozva_felhasznalo",
                       "modositva_ido", "modositva_felhasznalo", "nev_slug",)
    fieldsets = (
        (None, {
            "fields": (
                "nev_teljes", "mertekegyseg", "kozosadattipus", "inaktiv", "megjegyzes",
            )
        }),
        (EXPORT_TEXTS["fieldset1_name"], {
            "classes": ("collapse",),
            "fields": ("nev_teljes_mgh", "letrehozva_ido", "letrehozva_felhasznalo", "modositva_ido", "modositva_felhasznalo", "nev_slug",)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Ez kell ahhoz, hogy mentéskor beírja az aktív felhasználót a
        léterehozó és a módosító személy mezőkbe *ezen* a modellen.
        """
        obj.user = request.user
        obj.letrehozva_felhasznalo = obj.user
        obj.modositva_felhasznalo = obj.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        Ez kell ahhoz, hogy mentéskor beírja az aktív felhasználót a
        léterehozó és a módosító személy mezőkbe az *inline* modelleken.
        Note: az inline modellre emiatt külön nem került save_model override.
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.letrehozva_felhasznalo = instance.user
            instance.modositva_felhasznalo = instance.user
            instance.save()
        formset.save_m2m()
