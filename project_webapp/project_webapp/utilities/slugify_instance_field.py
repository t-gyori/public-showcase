import random
from django.utils.text import slugify


def ext_slugify_instance_field(instance, source_field, slug_field, save=False, new_slug=None):
    """
    Egy model object egy instance-ában egy field értékéből egy egyedi slugot csinál, és beírja egy másik fieldbe.
    A source végére egy 100000...999999 közötti random szám kerül.
    Névegyezés esetén új számot oszt a slugra, így elvileg 900 ezer egyedi slug készülhet.

    instance: pre_save és post_save instance, alapból instance
    source_field: field neve, amiből a slug-ot képezzük
    slug_field: field neve, ahova a slug-ot írjuk
    save: pre_save esetén False, post_save esetén True
    new_slug: átvett slug érték (de nem vesz át semmit sem, dunno, utána nézni)
    """
    Klass = instance.__class__
    if new_slug is not None:  # van létező slug (biztosan valid)
        slug = new_slug
        valid_slug = True
    else:  # nincs létező slug: generál egy új (még nem validált) slugot
        rand_int = random.randint(100000, 999999)
        slug = f"{slugify(getattr(instance, source_field))}-{rand_int}"
        valid_slug = False
    while not valid_slug:  # validálás
        # megnézi, hogy van-e másik slug ilyen névvel
        qs = Klass.objects.filter(**{slug_field: slug}).exclude(id=instance.id)
        if qs.exists():  # ha van, akkor csinál egy újat, majd újrakezdi a loopot
            rand_int = random.randint(100000, 999999)
            slug = f"{slugify(getattr(instance, source_field))}-{rand_int}"
        else:  # ha nincs, akkor valid, újrakezdi a loopot, majd kilép
            valid_slug = True
            break
    setattr(instance, slug_field, slug)
    if save:
        instance.save()
    return instance
