# dj-nepali-address

dj-nepali-address is a Django app to use predefined province, district and municipality.
You may add new data as required

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "nepali_address" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'nepali_address',
    ]

2. Run ``python manage.py migrate`` to create the nepali_address models.

3. Run ``python manage.py loaddata nepali_address`` to load data in nepali_address models.

Documentation
-------------

For full documentation, visit [dj-nepali-address-system.readthedocs.io](https://dj-nepali-address-system.readthedocs.io/en/latest/).
