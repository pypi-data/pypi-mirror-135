pyramid_cloudflare_access
=========================

Introduction
------------


Installation
------------

Just do

``pip install pyramid_cloudflare_access``

or

``easy_install pyramid_cloudflare_access``


Compatibility
-------------

pyramid_cloudflare_access runs with pyramid>=1.7 and python>=3.6.
Other versions might also work.


Usage
-----

Add Cloudfalre config to a production.ini::

    pyramid_cloudflare_access.policy_audience = "my_audience"
    pyramid_cloudflare_access.team = "https://team.cloudfare-access.com"


More information can be found at https://developers.cloudflare.com/cloudflare-one/identity/users/validating-json#python-example

Usage example for the tween::

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_cloudflare_access')
        return config.make_wsgi_app()


Releasing
---------

#. Update CHANGES.rst.
#. Update pyproject.toml version.
#. Run ``poetry check``.
#. Run ``poetry publish --build``.


We're hiring!
-------------

At Niteo we regularly contribute back to the Open Source community. If you do too, we'd like to invite you to `join our team
<https://niteo.co/careers/>`_!
