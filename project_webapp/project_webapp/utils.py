from .utilities.slugify_instance_field import ext_slugify_instance_field
from .utilities.text_import import ext_upload_from_tabletext_to_database


def slugify_instance_field(instance, source_field, slug_field, save=False, new_slug=None):
    # adatbázisba beíráskor slug mező adatának létrehozása
    ext_slugify_instance_field(
        instance, source_field, slug_field, save, new_slug)
    return instance


def upload_from_tabletext_to_database(file_path, App, Table, delimiter=None, Test=None, admin_upload=False, manual_upload=False):
    # adatbázisba beírás text fájlból
    data_errors, data_is_valid, fields_errors, fields_is_valid = ext_upload_from_tabletext_to_database(
        file_path, App, Table, delimiter, Test, admin_upload, manual_upload)
    return (data_errors, data_is_valid, fields_errors, fields_is_valid)
