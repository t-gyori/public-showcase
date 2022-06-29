import pprint as pprint

from django.apps import apps
import csv


def upload_data(Model, import_data, import_fields, delimiter, table_options, admin_upload, manual_upload):
    """
    Kiolvassa, hogy milyen kötelező ill. opcionális mezőkbe lehet beírni a táblában.
    Egyes field típusok esetén formázza a kapott adatokat.
    Ellenőrzi, hogy az adatok megfelelők-e a feltöltéshez.
    Ha a fentiek alapján feltölthetők az adatok, akkor feltölti és menti az adatokat a táblában.
    """
    from django.db.models.fields import NOT_PROVIDED
    from django.contrib.auth import get_user_model

    # user definiálása
    User = get_user_model()
    if manual_upload:
        user = User.objects.get(id=1)
    else:
        user = User.objects.get(id=1)  # tba, nem terminálos feltöltéshez
    # Model fieldek kezelése - field típusok kigyűjtése
    field_types_numbers = [
        "AutoField", "BigAutoField", "BigIntegerField", "BinaryField",
        "DecimalField", "FloatField", "IntegerField", "PositiveBigIntegerField",
        "PositiveIntegerField", "PositiveSmallIntegerField", "SmallAutoField", "SmallIntegerField",
    ]
    field_types_booleans = [
        "BooleanField", "NullBooleanField"
    ]
    # Model fieldek kezelése
    """
    Az alábbi listákba tetszőleges field neveket lehet beírni, mivel később ellenőrzi a kód,
    hogy nem létező mezőkbe ne írjon be, valamint hogy ne legyen duplikálás a listák között.
    Note: a field nevek használata a táblák között legyen konvencionális.
    (Pl. a "felhasznalo" mező ne legyen az egyik modelben Foreign Key, máshol meg mondjuk Boolean.)
    """
    fields_tiltott = ["id", ]  # ezekbe fixen tiltott beírni
    fields_tiltott_add = []  # ezek tiltottak, ha admin_upload == True
    fields_kotelezo = []  # ezekbe kötelező beírni
    fields_opcionalis = []  # ezekbe be lehet írni
    fields_user_inj = ["letrehozva_felhasznalo",
                       "modositva_felhasznalo"]  # ezekbe a mezőkbe user instance-okat töltünk fel (terminál feltöltéshez)
    fields_admin = ["letrehozva_ido", "letrehozva_felhasznalo", "modositva_ido",
                    "modositva_felhasznalo", "nev_slug", ]  # ezek olyan mezők, amik normál körülmények között automatikusan generálódnak, így nem lehet/kell adatokat megadni
    # generált listák előtöltése
    if not admin_upload:  # az admin beírhat tiltott mezőkbe is
        fields_tiltott_add += fields_admin
    else:
        fields_opcionalis += fields_admin
    # mező default értéke akkor, ha nem adtunk meg semmit sem
    default_not_provided = [NOT_PROVIDED, ]
    # Model fieldek kezelése: előre definiált listák tisztítása a valós tábla mezők alapján
    field_lists = [fields_tiltott_add, fields_kotelezo, fields_opcionalis]
    for field_list in field_lists:
        if field_list != []:
            # a negatív loop miatt kell mindenből 1-et kivonni
            for item_id in range(len(field_list) - 1, -1, -1):
                if field_list[item_id] not in list(table_options.keys()):
                    field_list.pop(item_id)
    # Model fieldek kezelése: kötelező és opcionális fieldek kigyűjtése
    for field in list(table_options.keys()):
        if field in fields_kotelezo or field in fields_opcionalis or field in fields_tiltott or field in fields_tiltott_add:
            pass  # előre megadott értékek vagy előre tiltott értékek
        else:
            if table_options[field]["auto_created"]:
                pass  # automatikusan generált, nem szabad beírni
            else:
                if table_options[field]["default"] in default_not_provided:
                    # nincs default érték
                    if table_options[field]["blank"]:
                        # lehet üres, opcionális
                        fields_opcionalis.append(field)
                    else:
                        # nem lehet üres, kötelező
                        fields_kotelezo.append(field)
                else:
                    # van default érték, opcionális
                    fields_opcionalis.append(field)
    # Text fieldek kezelése: megtalálhatók-e a text fieldek a kötelező vagy opcionális field listákban
    fields_is_valid = True
    fields_errors = []
    for field in import_fields:
        if field in fields_kotelezo or field in fields_opcionalis:
            # print("Van " + str(field) + " nevű mező az adattáblában.")
            pass
        else:
            fields_errors.append(
                "Nincs " + str(field) + " nevű mező az adattáblában.")
            fields_is_valid = False
            # print("Nincs " + str(field) + " nevű mező az adattáblában.")
            pass
    # Text fieldek kezelése: megtalálhatók-e a kötelező fieldek a text field listában
    for field in fields_kotelezo:
        if field in import_fields:
            # print("A " + str(field) + " nevű mező megtalálható a szövegfájlban.")
            pass
        else:
            fields_errors.append(
                "A " + str(field) + " nevű mező nem található meg a szövegfájlban.")
            fields_is_valid = False
            # print("A " + str(field) + " nevű mező nem található meg a szövegfájlban.")
            pass
    # Text adatok kezelése
    if not fields_is_valid:
        data_is_valid = False
        data_errors = [
            "A mező/fejléc ellenőrzés hibája miatt az adatok vizsgálata nem történt meg.", ]
    else:
        data_is_valid = True
        data_errors = []
        # Text adatok kezelése: user fieldek beszúrása
        for user_field in fields_user_inj:
            if user_field in table_options.keys() and user_field not in import_fields:
                for list_item in range(0, len(import_data)):
                    import_data[list_item][user_field] = user
        pprint.pprint(import_data)
        # Text adatok kezelése: adatok módosítása
        for field in import_fields:
            field_type = Model._meta.get_field(
                field).get_internal_type()  # mező típus
            # foreign key fordító
            # if table_options[field]["is_relation"]:
            if field_type == "ForeignKey":
                Rel_Model = Model._meta.get_field(field).related_model
                for list_item in range(0, len(import_data)):
                    if import_data[list_item][field].isnumeric():  # számot kapunk: id
                        targetfields = Rel_Model.__pk_str__()
                        # legtöbbször az "id" field
                        targetfield = targetfields["int"]
                    else:  # nem számot kaptunk: nem id
                        targetfields = Rel_Model.__pk_str__()
                        # legtöbbször a "név_egyedi" field (v. valami hasonló)
                        targetfield = targetfields["str"]
                    try:
                        relation = Rel_Model.objects.get(
                            **{targetfield: import_data[list_item][field]})
                        import_data[list_item][field] = relation
                    except:
                        pass  # az adatok ellenőrzénél amúgy is elhasal, és érthetőbb az a hiba üzenet
            # dátum formátum javító
            if field_type == "DateField":
                for list_item in range(0, len(import_data)):
                    str_input = import_data[list_item][field]
                    str_output = None
                    # az elválasztó karakter helyei fixek, értékük bármi lehet, ami nem szám
                    # az elválasztó karaktereken kívül 3 db érvényes számnak kell szerepelnie az inputban
                    # 2 adatsorrendet fogad el: YYYY-MM-DD és DD-MM-YYYY (és így értelmezi az inputot)
                    if not str_input[4:5].isnumeric() and not str_input[7:8].isnumeric():
                        # YYYY-MM-DD formátum
                        if str_input[0:4].isnumeric() and str_input[5:7].isnumeric() and str_input[8:10].isnumeric():
                            str_output = str(
                                str_input[0:4]) + "-" + str_input[5:7] + "-" + str_input[8:10]
                    elif not str_input[2:3].isnumeric() and not str_input[5:6].isnumeric():
                        # DD-MM-YYYY formátum
                        if str_input[0:2].isnumeric() and str_input[3:5].isnumeric() and str_input[6:10].isnumeric():
                            str_output = str(
                                str_input[0:2]) + "-" + str_input[3:5] + "-" + str_input[6:10]
                    if str_output:
                        import_data[list_item][field] = str_output
            # szám elválasztó karakter és decimális hossz javító
            if field_type in field_types_numbers:
                # szám hossza (field jellemző)
                try:
                    max_digits = table_options[field]["max_digits"]
                except:
                    max_digits = 0
                try:
                    max_decimals = table_options[field]["decimal_places"]
                except:
                    max_decimals = 0
                # formázások
                for list_item in range(0, len(import_data)):
                    # elválasztó karakterek beállítása
                    str_input = import_data[list_item][field]
                    str_output = None
                    if delimiter == ";":
                        # tizedesjegy elválasztó karakter: ","
                        # ezres elválasztó karakter: " " vagy "."
                        str_output = str_input.replace(
                            " ", "").replace(".", "").replace(",", ".")
                    else:
                        # tizedesjegy elválasztó karakter: "."
                        # ezres elválasztó karakter: " "
                        str_output = str_input.replace(" ", "")
                    # szám formázása a lehetséges decimális karakterek alapján
                    if not str_output.count("."):  # van tizedeselválasztó
                        # jelenlegi dec. hossz
                        cur_decimals = str_output[::-1].find(".")
                        # jelenlegi int. hossz
                        cur_int_len = len(str(int(float(str_output))))
                        # output átalakítása a lehetséges dec. hossz alapján
                        if max_digits == cur_int_len:  # valid, nincs hely decimálisnak
                            str_output = str(int(float(str_output)))
                        elif max_digits > cur_int_len:  # valid, van hely decimálisnak
                            # lehetséges dec. hossz
                            pos_decimals = max_digits - cur_int_len
                            if pos_decimals > max_decimals:
                                pos_decimals = max_decimals
                            if pos_decimals > cur_decimals:
                                pos_decimals = cur_decimals
                            # eredmény
                            if pos_decimals > 0:
                                dec_start = cur_int_len + 1
                                dec_stop = dec_start + pos_decimals
                                str_output = str(int(float(str_output))) + \
                                    "." + str_output[dec_start:dec_stop]
                            else:
                                str_output = str(int(float(str_output)))
                        else:  # invalid
                            pass  # full_clean során kiesik
                    # módosított adat beírása
                    import_data[list_item][field] = str_output
            # boolean érték javító
            if field_type in field_types_booleans:
                for list_item in range(0, len(import_data)):
                    input_true = [
                        "true", "igaz", "yes", "igen", "1", 1,
                    ]
                    input_false = [
                        "false", "hamis", "no", "nem", "0", 0,
                    ]
                    if str(import_data[list_item][field]).lower() in input_true:
                        import_data[list_item][field] = 1
                    elif str(import_data[list_item][field]).lower() in input_false:
                        import_data[list_item][field] = 0
        # Text adatok kezelése: adatok ellenőrzése
        for list_item in range(0, len(import_data)):
            try:
                data = Model(**import_data[list_item])
                data.full_clean()
            except Exception as errors:
                data_is_valid = False
                try:
                    for error in errors:
                        data_errors.append(f"{list_item + 2}. sor: {error}")
                except:
                    data_errors.append(
                        f"{list_item + 2}. sor: {errors}")
        # Text adatok kezelése: adatok feltöltése
        if data_is_valid:
            for list_item in range(0, len(import_data)):
                data = Model(**import_data[list_item])
                data.save()
                pass
        else:
            pprint.pprint(data_errors)
    return(data_errors, data_is_valid, fields_errors, fields_is_valid)


def ext_upload_from_tabletext_to_database(file_path, App, Table, delimiter=None, Test=None, admin_upload=False, manual_upload=False):
    # input adatok frissítése
    if Test:
        if not App:
            App = "energia"
        if not Table:
            Table = "KozosAdatTipus"
#            Table = "KozosAdatTipusValtoszam"
        if not file_path:
            file_path = r".\project_webapp\.dummydata\kozosadattipus_tesztadat1.txt"
#            file_path = r".\project_webapp\.dummydata\kozosadattipus_valtoszam_tesztadat1.txt"
        if not admin_upload:
            admin_upload = True
        if not manual_upload:
            manual_upload = True

    if not delimiter == "\t" and not delimiter == "," and not delimiter == ";":
        delimiter = "\t"
    # model (tábla) definiálás
    Model = apps.get_model(App, Table)
    # szövegfájl importálása
    """
    Importál egy szövegfájlba mentett táblázatot, aminek van fejléc sora.
    Az eredmény egy lista. A lista minden eleme tartalmaz egy dict-et.
    A dict-en belül találhatók a fejlécek és az értékek.
    Input:  fejléc1 fejléc2
            adat1   adat2
            adat3   adat4
    Output: [{'fejlec1': 'adat1', 'fejlec2': 'adat2'},
        {'fejlec1': 'adat3', 'fejlec2': 'adat4'},]
    """
    import_data = []
    with open(file_path, newline='', mode="r", encoding="utf-8") as rows:
        row_reader = csv.DictReader(rows, delimiter=delimiter)
        for row in row_reader:
            import_data.append(dict(row))
    if not import_data:
        print("A külső szövegfájl beolvasása nem sikerült.")
        return
    # szövegfájlban levő fejlécek kigyűjtése
    import_fields = list(import_data[0].keys())
    # adattábla (model) field beállításainak kigyűjtése
    """
    Kigyűjti egy model/tábla összes field option-jét.
    Eredmény: dict_A{dict_a{}, dict_b{},}
    dict_A: fő dict; a neve megegyezik azzal, ahova meghívják (return)
    dict_a: sub dict; a neve megegyezik a tábla field neveivel (pl. id, name, stb.)
            ezen belül találhatók az optionök és értékeik (pl. "primary_key": True, stb.)
    """
    table_options = {}
    for field in Model._meta.fields:
        table_options[field.name] = {}
    for field in table_options:
        table_options[field] = Model._meta.get_field(field).__dict__
    # adatok ellenőrzése és feltöltése
    """
    Előkészíti az adatokat a feltöltéshez. Ha nincsen hiba, akkor feltölti. Hiba esetén output készül (tba).

    """
    data_errors, data_is_valid, fields_errors, fields_is_valid = upload_data(
        Model=Model, import_data=import_data, import_fields=import_fields,
        delimiter=delimiter, table_options=table_options,
        admin_upload=admin_upload, manual_upload=manual_upload
    )
    return (data_errors, data_is_valid, fields_errors, fields_is_valid)

# from django.apps import apps
# from django.contrib.auth import get_user_model

# App = "energia"
# Table = "KozosAdatTipus"

# User = get_user_model()
# user = User.objects.get(id=1)
# Model = apps.get_model(App, Table)

# a, b, c, d = ext_upload_from_tabletext_to_database("", "", "", Test=True)
