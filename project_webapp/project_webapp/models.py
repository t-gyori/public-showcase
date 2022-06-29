"""
Ebben a fájlban csak abstract modelek találhatók, amikre a többi app modeljei épülnek.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
import datetime
import uuid

User = settings.AUTH_USER_MODEL

EXPORT_TEXTS = {
    "yes": _("igen"),
    "no": _("nem"),
    "unknown": _("ismeretlen"),
    "fieldset1_name": _("Egyéb beállítások és tulajdonságok"),
}

class BaseFields(models.Model):
    megjegyzes = models.CharField(
        max_length=512, blank=True, verbose_name=_("megjegyzés"),
        help_text=_("Opcionális feljegyzés."))
    letrehozva_ido = models.DateTimeField(
        auto_now_add=True, verbose_name=_("létrehozás időpontja"),
        help_text=_("Létrehozás időpontja."))
    letrehozva_felhasznalo = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_creator",
        verbose_name=_("létrehozó felhasználó"), help_text=_("Létrehozó felhasználó."))
    modositva_ido = models.DateTimeField(
        auto_now=True, verbose_name=_("módosítás időpontja"),
        help_text=_("Utolsó módosítás időpontja."))
    modositva_felhasznalo = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_modifier",
        verbose_name=_("módosító felhasználó"), help_text=_("Utolsó módosítást végző felhasználó."))
    inaktiv = models.BooleanField(default=False, verbose_name=_("inaktív"),
                                  help_text=_("Inaktivált bejegyzés, ami csak az admin oldalon látható."))

    @classmethod
    def __pk_str__(cls):
        """
        Ezt CSV feltötlés során a PK fordítóhoz használom.
        Itt is érvényes a field nevekre az, hogy konvencionális elnevezéseket kell alkalmazni.
        Egy dict-et készít, amiben az "int" key alatt lesz egy számot váró egyedi field neve (pl. "id"),
        "str" alatt pedig egy nem számot váró egyedi field neve (pl. "nev_teljes").
        """
        # default értékek
        id_fields = {
            "int": "id",
            "str": None,
        }
        # field lista az ellenőrzéshez
        fields_int = ["id", ]
        fields_str = ["nev_teljes", ]
        field_int_valid = False
        field_str_valid = False
        # a model fieldjei
        fields = []
        for field in cls._meta.fields:
            fields.append(field.name)
        # fieldek keresése és hozzáadása dict-hez
        # note: a fields_int és fields_str első megtalált értékét tekinti véglegesnek
        for field in fields:
            if field in fields_int and not field_int_valid:
                id_fields["int"] = field
                field_int_valid = True
            elif field in fields_str and not field_str_valid:
                id_fields["str"] = field
                field_str_valid = True
            if field_int_valid and field_str_valid:
                break
        return id_fields

    class Meta:
        abstract = True


class NameFields(models.Model):
    nev_teljes = models.CharField(
        max_length=128, unique=True, verbose_name=_("teljes megnevezés"),
        help_text=_("Teljes megnevezés."))
    nev_teljes_mgh = models.BooleanField(
        default=False, verbose_name=_("kiejtés magánhangzóval kezdődik"),
        help_text=_("A teljes megnevezés kiejtése magánhangzóval kezdődik."))

    def __str__(self):
        # return self.nev_teljes.capitalize()
        return self.nev_teljes.capitalize()

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["nev_teljes"])]
        ordering = ["nev_teljes", ]


class AddressFields(models.Model):
    cim_orszagkod = models.CharField(
        max_length=10, default="HU", verbose_name=_("országkód"), help_text=_("Címhez tartozó országkód."))
    cim_irsz = models.CharField(
        max_length=10, verbose_name=_("ir. szám"), help_text=_("Címhez tartozó irányítószám."))
    cim_varos = models.CharField(
        max_length=64, verbose_name=_("város"), help_text=_("Címhez tartozó város."))
    cim_kozterulet = models.CharField(
        max_length=128, verbose_name=_("közterület"), help_text=_("Címhez tartozó közterület."))
    cim_hazszam = models.CharField(
        max_length=32, blank=True, verbose_name=_("házszám"), help_text=_("Címhez tartozó házszám (opcionális)."))

    class Meta:
        abstract = True


class ContactFields(models.Model):
    email = models.EmailField(
        max_length=128, verbose_name=_("e-mail cím"),
        help_text=_("Kapcsolattartási e-mail cím."))
    telefon = models.CharField(
        max_length=32, verbose_name=_("telefonszám"),
        help_text=_("Kapcsolattartási telefonszám."))

    class Meta:
        abstract = True


class UUIDFields(models.Model):
    uuid4 = models.UUIDField(
        default=uuid.uuid4, editable=False, verbose_name=_("adatsor UUID"),
        help_text=_("Automatikusan generált bejegyzés azonosító."))

    class Meta:
        abstract = True


class DateStartFields(models.Model):
    datum_kezdo = models.DateField(
        default=datetime.date.today, verbose_name=_("érvényesség kezdete"),
        help_text=_("Érvényesség kezdete."))

    class Meta:
        abstract = True
