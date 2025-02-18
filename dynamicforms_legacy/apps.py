from django.apps import AppConfig


class DynamicformsConfig(AppConfig):
    name = "dynamicforms"

    def ready(self):
        import django

        if django.VERSION >= (5, 0):
            # Django 5.x introduces ValueError if related objects are fetched on non saved instance.
            # This gives us troubles when we create forms for new entries and filter forms.
            # Also (mostly) on __str__ functions of instances, until they are saved.
            #
            # So here is monkeypatch of this django function when in such case we return empty queryset.

            from django.db.models.fields.related_descriptors import (
                create_forward_many_to_many_manager,
                create_reverse_many_to_one_manager,
            )

            # Shranimo originalno funkcijo
            original_create_reverse_many_to_one_manager = create_reverse_many_to_one_manager
            original_create_forward_many_to_many_manager = create_forward_many_to_many_manager

            def patched_create_reverse_many_to_one_manager(superclass, rel):
                # Dobimo originalni RelatedManager razred
                manager_class = original_create_reverse_many_to_one_manager(superclass, rel)

                # Shranimo njegovo originalno get_queryset metodo
                original_get_queryset = manager_class.get_queryset

                # Naredimo novo get_queryset metodo
                def patched_get_queryset(_self):
                    try:
                        return original_get_queryset(_self)
                    except ValueError as e:
                        if "instance needs to have a primary key value" in str(e):
                            return _self.model.objects.none()
                        raise

                # Zamenjamo metodo na razredu
                manager_class.get_queryset = patched_get_queryset

                # Vrnemo modificiran razred
                return manager_class

            def patched_create_forward_many_to_many_manager(superclass, rel, reverse):
                manager_class = original_create_forward_many_to_many_manager(superclass, rel, reverse)

                # noinspection PyTypeChecker
                original_init = manager_class.__init__

                def patched_init(_self, instance=None):
                    try:
                        # noinspection PyArgumentList
                        original_init(_self, instance)
                    except ValueError as e:
                        if (
                            ("needs to have a value for field" in str(e))
                            or ("instance needs to have a primary key value before" in str(e))
                        ) and ("many-to-many relationship can be used." in str(e)):
                            # Adding filter that will make sure that returned queryset is empty.
                            _self.core_filters["id"] = None
                            pass
                        else:
                            raise

                manager_class.__init__ = patched_init
                return manager_class

            # Zamenjamo originalno funkcijo
            django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager = (
                patched_create_reverse_many_to_one_manager
            )
            django.db.models.fields.related_descriptors.create_forward_many_to_many_manager = (
                patched_create_forward_many_to_many_manager
            )
