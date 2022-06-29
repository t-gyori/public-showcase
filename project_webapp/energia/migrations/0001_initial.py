# Generated by Django 3.2.13 on 2022-06-29 09:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KozosAdatTipus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('megjegyzes', models.CharField(blank=True, help_text='Opcionális feljegyzés.', max_length=512, verbose_name='megjegyzés')),
                ('letrehozva_ido', models.DateTimeField(auto_now_add=True, help_text='Létrehozás időpontja.', verbose_name='létrehozás időpontja')),
                ('modositva_ido', models.DateTimeField(auto_now=True, help_text='Utolsó módosítás időpontja.', verbose_name='módosítás időpontja')),
                ('inaktiv', models.BooleanField(default=False, help_text='Inaktivált bejegyzés, ami csak az admin oldalon látható.', verbose_name='inaktív')),
                ('nev_teljes', models.CharField(help_text='Teljes megnevezés.', max_length=128, unique=True, verbose_name='teljes megnevezés')),
                ('nev_teljes_mgh', models.BooleanField(default=False, help_text='A teljes megnevezés kiejtése magánhangzóval kezdődik.', verbose_name='kiejtés magánhangzóval kezdődik')),
                ('nev_slug', models.SlugField(editable=False, help_text='Automatikusan generált bejegyzés azonosító.', max_length=64, unique=True, verbose_name='slug megnevezés')),
                ('mertekegyseg', models.CharField(help_text='Az adatsor mértékegysége.', max_length=8, verbose_name='mértékegység')),
                ('mennyiseg', models.BooleanField(default=True, help_text='Az adatsor értékei mennyiségek (nem állapotértékek).', verbose_name='mennyiség')),
                ('energia', models.BooleanField(default=True, help_text='Az adatsor energia mennyiségeket tartalmaz.', verbose_name='energia')),
                ('letrehozva_felhasznalo', models.ForeignKey(help_text='Létrehozó felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_kozosadattipus_creator', to=settings.AUTH_USER_MODEL, verbose_name='létrehozó felhasználó')),
                ('modositva_felhasznalo', models.ForeignKey(help_text='Utolsó módosítást végző felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_kozosadattipus_modifier', to=settings.AUTH_USER_MODEL, verbose_name='módosító felhasználó')),
            ],
            options={
                'verbose_name': 'közös adat típus',
                'verbose_name_plural': 'közös adat típusok',
                'ordering': ['nev_teljes'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeresAdatTipus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('megjegyzes', models.CharField(blank=True, help_text='Opcionális feljegyzés.', max_length=512, verbose_name='megjegyzés')),
                ('letrehozva_ido', models.DateTimeField(auto_now_add=True, help_text='Létrehozás időpontja.', verbose_name='létrehozás időpontja')),
                ('modositva_ido', models.DateTimeField(auto_now=True, help_text='Utolsó módosítás időpontja.', verbose_name='módosítás időpontja')),
                ('inaktiv', models.BooleanField(default=False, help_text='Inaktivált bejegyzés, ami csak az admin oldalon látható.', verbose_name='inaktív')),
                ('nev_teljes', models.CharField(help_text='Teljes megnevezés.', max_length=128, unique=True, verbose_name='teljes megnevezés')),
                ('nev_teljes_mgh', models.BooleanField(default=False, help_text='A teljes megnevezés kiejtése magánhangzóval kezdődik.', verbose_name='kiejtés magánhangzóval kezdődik')),
                ('nev_slug', models.SlugField(editable=False, help_text='Automatikusan generált bejegyzés azonosító.', max_length=64, unique=True, verbose_name='slug megnevezés')),
                ('mertekegyseg', models.CharField(help_text='Az adatsor mértékegysége.', max_length=8, verbose_name='mértékegység')),
                ('kozosadattipus', models.ForeignKey(help_text='Az adat típushoz tartozó közös típus.', on_delete=django.db.models.deletion.PROTECT, to='energia.kozosadattipus', verbose_name='közös adat típus')),
                ('letrehozva_felhasznalo', models.ForeignKey(help_text='Létrehozó felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_meresadattipus_creator', to=settings.AUTH_USER_MODEL, verbose_name='létrehozó felhasználó')),
                ('modositva_felhasznalo', models.ForeignKey(help_text='Utolsó módosítást végző felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_meresadattipus_modifier', to=settings.AUTH_USER_MODEL, verbose_name='módosító felhasználó')),
            ],
            options={
                'verbose_name': 'mérés adat típus',
                'verbose_name_plural': 'mérés adat típusok',
                'ordering': ['nev_teljes'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeresAdatTipusValtoszam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('megjegyzes', models.CharField(blank=True, help_text='Opcionális feljegyzés.', max_length=512, verbose_name='megjegyzés')),
                ('letrehozva_ido', models.DateTimeField(auto_now_add=True, help_text='Létrehozás időpontja.', verbose_name='létrehozás időpontja')),
                ('modositva_ido', models.DateTimeField(auto_now=True, help_text='Utolsó módosítás időpontja.', verbose_name='módosítás időpontja')),
                ('inaktiv', models.BooleanField(default=False, help_text='Inaktivált bejegyzés, ami csak az admin oldalon látható.', verbose_name='inaktív')),
                ('datum_kezdo', models.DateField(default=datetime.date.today, help_text='Érvényesség kezdete.', verbose_name='érvényesség kezdete')),
                ('szorzo_kwh', models.DecimalField(decimal_places=8, default=1, help_text='Számérték, amivel az adatot megszorozva kWh mennyiséget kapunk. Ha kWh mennyiség nem értelmezhető, akkor az értéke megegyezik az adatot közös értékre átváltó szorzószámmal.', max_digits=24, verbose_name='kWh szorzó')),
                ('szorzo_kwh_forras', models.CharField(default='ismeretlen', help_text='A kWh szorzó adat forrása, szöveges leírás.', max_length=128, verbose_name='kWh szorzó forrás')),
                ('szorzo_kwh_datum', models.DateField(default=datetime.date.today, help_text='A kWh szorzó adat ellenőrzésének dátuma.', verbose_name='kWh szorzó adatellenőrzés dátuma')),
                ('szorzo_t_co2', models.DecimalField(decimal_places=8, default=0, help_text='Számérték, amivel az adatot megszorozva t CO2 mennyiséget kapunk. Ha t CO2 mennyiség nem értelmezhető, akkor az értéke megegyezik az adatot közös értékre átváltó szorzószámmal.', max_digits=24, verbose_name='tonna CO2 szorzó')),
                ('szorzo_t_co2_forras', models.CharField(default='ismeretlen', help_text='A CO2 szorzó adat forrása, szöveges leírás.', max_length=128, verbose_name='tonna CO2 szorzó forrás')),
                ('szorzo_t_co2_datum', models.DateField(default=datetime.date.today, help_text='A CO2 szorzó adat ellenőrzésének dátuma.', verbose_name='tonna CO2 szorzó adatellenőrzés dátuma')),
                ('letrehozva_felhasznalo', models.ForeignKey(help_text='Létrehozó felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_meresadattipusvaltoszam_creator', to=settings.AUTH_USER_MODEL, verbose_name='létrehozó felhasználó')),
                ('meresadattipus', models.ForeignKey(help_text='A mérés adat típus megnevezése.', on_delete=django.db.models.deletion.PROTECT, to='energia.meresadattipus', verbose_name='mérés adat típus')),
                ('modositva_felhasznalo', models.ForeignKey(help_text='Utolsó módosítást végző felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_meresadattipusvaltoszam_modifier', to=settings.AUTH_USER_MODEL, verbose_name='módosító felhasználó')),
            ],
            options={
                'verbose_name': 'mérés adat típus váltószám',
                'verbose_name_plural': 'mérés adat típusok váltószámok',
                'ordering': ['meresadattipus__nev_teljes', 'datum_kezdo'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KozosAdatTipusValtoszam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('megjegyzes', models.CharField(blank=True, help_text='Opcionális feljegyzés.', max_length=512, verbose_name='megjegyzés')),
                ('letrehozva_ido', models.DateTimeField(auto_now_add=True, help_text='Létrehozás időpontja.', verbose_name='létrehozás időpontja')),
                ('modositva_ido', models.DateTimeField(auto_now=True, help_text='Utolsó módosítás időpontja.', verbose_name='módosítás időpontja')),
                ('inaktiv', models.BooleanField(default=False, help_text='Inaktivált bejegyzés, ami csak az admin oldalon látható.', verbose_name='inaktív')),
                ('datum_kezdo', models.DateField(default=datetime.date.today, help_text='Érvényesség kezdete.', verbose_name='érvényesség kezdete')),
                ('szorzo_kwh', models.DecimalField(decimal_places=8, default=1, help_text='Számérték, amivel az adatot megszorozva kWh mennyiséget kapunk. Ha kWh mennyiség nem értelmezhető, akkor az értéke megegyezik az adatot közös értékre átváltó szorzószámmal.', max_digits=24, verbose_name='kWh szorzó')),
                ('szorzo_kwh_forras', models.CharField(default='ismeretlen', help_text='A kWh szorzó adat forrása, szöveges leírás.', max_length=128, verbose_name='kWh szorzó forrás')),
                ('szorzo_kwh_datum', models.DateField(default=datetime.date.today, help_text='A kWh szorzó adat ellenőrzésének dátuma.', verbose_name='kWh szorzó adatellenőrzés dátuma')),
                ('kozosadattipus', models.ForeignKey(help_text='A közös adat típus megnevezése.', on_delete=django.db.models.deletion.PROTECT, to='energia.kozosadattipus', verbose_name='közös adat típus')),
                ('letrehozva_felhasznalo', models.ForeignKey(help_text='Létrehozó felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_kozosadattipusvaltoszam_creator', to=settings.AUTH_USER_MODEL, verbose_name='létrehozó felhasználó')),
                ('modositva_felhasznalo', models.ForeignKey(help_text='Utolsó módosítást végző felhasználó.', on_delete=django.db.models.deletion.PROTECT, related_name='energia_kozosadattipusvaltoszam_modifier', to=settings.AUTH_USER_MODEL, verbose_name='módosító felhasználó')),
            ],
            options={
                'verbose_name': 'közös adat típus váltószám',
                'verbose_name_plural': 'közös adat típusok váltószámok',
                'ordering': ['kozosadattipus__nev_teljes', 'datum_kezdo'],
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='meresadattipusvaltoszam',
            index=models.Index(fields=['id'], name='energia_mer_id_a005dd_idx'),
        ),
        migrations.AddConstraint(
            model_name='meresadattipusvaltoszam',
            constraint=models.UniqueConstraint(fields=('meresadattipus', 'datum_kezdo'), name='meresadattipusvaltoszam_unique_type_date'),
        ),
        migrations.AddIndex(
            model_name='meresadattipus',
            index=models.Index(fields=['nev_teljes'], name='energia_mer_nev_tel_1444f2_idx'),
        ),
        migrations.AddIndex(
            model_name='kozosadattipusvaltoszam',
            index=models.Index(fields=['id'], name='energia_koz_id_1433f3_idx'),
        ),
        migrations.AddConstraint(
            model_name='kozosadattipusvaltoszam',
            constraint=models.UniqueConstraint(fields=('kozosadattipus', 'datum_kezdo'), name='kozosadattipusvaltoszam_unique_type_date'),
        ),
        migrations.AddIndex(
            model_name='kozosadattipus',
            index=models.Index(fields=['nev_teljes'], name='energia_koz_nev_tel_a47d60_idx'),
        ),
    ]