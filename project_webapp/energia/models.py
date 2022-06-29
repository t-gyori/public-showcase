from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext as _
import datetime

from project_webapp.models import *
from project_webapp.utils import slugify_instance_field


class WhMultiplierFields(models.Model):
    """abstract model - kWh szorzót leíró fieldek"""
    szorzo_kwh = models.DecimalField(
        max_digits=24, decimal_places=8, default=1, verbose_name=_("kWh szorzó"),
        help_text=_("Számérték, amivel az adatot megszorozva kWh mennyiséget kapunk. Ha kWh mennyiség nem értelmezhető, akkor az értéke megegyezik az adatot közös értékre átváltó szorzószámmal."))
    szorzo_kwh_forras = models.CharField(
        max_length=128, default=EXPORT_TEXTS["unknown"], verbose_name=_("kWh szorzó forrás"),
        help_text=_("A kWh szorzó adat forrása, szöveges leírás."))
    szorzo_kwh_datum = models.DateField(
        default=datetime.date.today, verbose_name=_(
            "kWh szorzó adatellenőrzés dátuma"),
        help_text=_("A kWh szorzó adat ellenőrzésének dátuma."))

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(check=models.Q(
                szorzo_kwh__gte=0), name='szorzo_kwh_gte_null'),
        ]


class CO2MultiplierFields(models.Model):
    """abstract model - CO2 szorzót leíró fieldek"""
    szorzo_t_co2 = models.DecimalField(
        max_digits=24, decimal_places=8, default=0, verbose_name=_("tonna CO2 szorzó"),
        help_text=_("Számérték, amivel az adatot megszorozva t CO2 mennyiséget kapunk. Ha t CO2 mennyiség nem értelmezhető, akkor az értéke megegyezik az adatot közös értékre átváltó szorzószámmal."))
    szorzo_t_co2_forras = models.CharField(
        max_length=128, default=EXPORT_TEXTS["unknown"], verbose_name=_("tonna CO2 szorzó forrás"),
        help_text=_("A CO2 szorzó adat forrása, szöveges leírás."))
    szorzo_t_co2_datum = models.DateField(
        default=datetime.date.today, verbose_name=_(
            "tonna CO2 szorzó adatellenőrzés dátuma"),
        help_text=_("A CO2 szorzó adat ellenőrzésének dátuma."))

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(check=models.Q(
                szorzo_t_co2__gte=0), name='szorzo_t_co2_gte_null'),
        ]


class KozosAdatTipus(BaseFields, NameFields):
    """energia típusok és fő mértékegységük"""
    nev_slug = models.SlugField(
        max_length=64, unique=True, editable=False, verbose_name=_("slug megnevezés"),
        help_text=_("Automatikusan generált bejegyzés azonosító."))
    mertekegyseg = models.CharField(
        max_length=8, verbose_name=_("mértékegység"),
        help_text=_("Az adatsor mértékegysége."))
    mennyiseg = models.BooleanField(
        default=True, verbose_name=_("mennyiség"),
        help_text=_("Az adatsor értékei mennyiségek (nem állapotértékek)."))
    energia = models.BooleanField(
        default=True, verbose_name=_("energia"),
        help_text=_("Az adatsor energia mennyiségeket tartalmaz."))

    class Meta(BaseFields.Meta, NameFields.Meta):
        verbose_name = _("közös adat típus")
        verbose_name_plural = _("közös adat típusok")


def kozosadattipus_pre_save(sender, instance, *args, **kwargs):
    # slug generálás
    field_source = "nev_teljes"
    field_slug = "nev_slug"
    if getattr(instance, field_slug) is None:
        slugify_instance_field(
            instance, field_source, field_slug, save=False)


pre_save.connect(kozosadattipus_pre_save, sender=KozosAdatTipus)


def kozosadattipus_post_save(sender, instance, created, *args, **kwargs):
    # slug generálás
    field_source = "nev_teljes"
    field_slug = "nev_slug"
    if created:
        slugify_instance_field(
            instance, field_source, field_slug, save=True)


post_save.connect(kozosadattipus_post_save, sender=KozosAdatTipus)


class MeresAdatTipus(BaseFields, NameFields):
    """energia típusok és egyedi mértékegységeik"""
    nev_slug = models.SlugField(
        max_length=64, unique=True, editable=False, verbose_name=_("slug megnevezés"),
        help_text=_("Automatikusan generált bejegyzés azonosító."))
    mertekegyseg = models.CharField(
        max_length=8, verbose_name=_("mértékegység"),
        help_text=_("Az adatsor mértékegysége."))
    kozosadattipus = models.ForeignKey(
        KozosAdatTipus, on_delete=models.PROTECT,
        verbose_name=_("közös adat típus"), help_text=_("Az adat típushoz tartozó közös típus."))

    class Meta(BaseFields.Meta, NameFields.Meta):
        verbose_name = _("mérés adat típus")
        verbose_name_plural = _("mérés adat típusok")


def meresadattipus_pre_save(sender, instance, *args, **kwargs):
    # slug generálás
    field_source = "nev_teljes"
    field_slug = "nev_slug"
    if getattr(instance, field_slug) is None:
        slugify_instance_field(
            instance, field_source, field_slug, save=False)


pre_save.connect(meresadattipus_pre_save, sender=MeresAdatTipus)


def meresadattipus_post_save(sender, instance, created, *args, **kwargs):
    # slug generálás
    field_source = "nev_teljes"
    field_slug = "nev_slug"
    if created:
        slugify_instance_field(
            instance, field_source, field_slug, save=True)


post_save.connect(meresadattipus_post_save, sender=MeresAdatTipus)


class KozosAdatTipusValtoszam(BaseFields, DateStartFields, WhMultiplierFields):
    """közös mértékegységek váltószámai"""
    kozosadattipus = models.ForeignKey(
        KozosAdatTipus, on_delete=models.PROTECT,
        verbose_name=_("közös adat típus"), help_text=_("A közös adat típus megnevezése."))

    def __str__(self):
        return str(self.datum_kezdo)

    class Meta(BaseFields.Meta, DateStartFields.Meta, WhMultiplierFields.Meta):
        verbose_name = _("közös adat típus váltószám")
        verbose_name_plural = _("közös adat típusok váltószámok")
        indexes = [models.Index(fields=["id"])]
        ordering = ["kozosadattipus__nev_teljes", "datum_kezdo"]
        constraints = [
            models.UniqueConstraint(
                fields=["kozosadattipus", "datum_kezdo"], name="%(class)s_unique_type_date"),
        ]


class MeresAdatTipusValtoszam(BaseFields, DateStartFields, WhMultiplierFields, CO2MultiplierFields):
    """egyedi mértékegységek váltószámai"""
    meresadattipus = models.ForeignKey(
        MeresAdatTipus, on_delete=models.PROTECT,
        verbose_name=_("mérés adat típus"), help_text=_("A mérés adat típus megnevezése."))

    def __str__(self):
        return str(self.datum_kezdo)

    class Meta(BaseFields.Meta, DateStartFields.Meta, WhMultiplierFields.Meta, CO2MultiplierFields.Meta):
        verbose_name = _("mérés adat típus váltószám")
        verbose_name_plural = _("mérés adat típusok váltószámok")
        indexes = [models.Index(fields=["id"])]
        ordering = ["meresadattipus__nev_teljes", "datum_kezdo"]
        constraints = [
            models.UniqueConstraint(
                fields=["meresadattipus", "datum_kezdo"], name="%(class)s_unique_type_date"),
        ]
