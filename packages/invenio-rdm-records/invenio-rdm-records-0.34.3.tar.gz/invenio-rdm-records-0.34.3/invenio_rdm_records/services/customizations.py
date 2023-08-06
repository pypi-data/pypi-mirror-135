# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Helpers for customizing the configuration in a controlled manner."""

# NOTE: Overall these classes should be refactored to be simply instantiations
# of the config class instead (e.g. "RDMRecordServiceConfig(...)"). However,
# that requires changing the pattern used also in Invenio-Drafts-Resources and
# Invenio-Records-Resources so we have a consistent way of instantiating
# configs.


#
# Helpers
#
def _make_cls(cls, attrs):
    """Make the custom config class."""
    return type(f'Custom{cls.__name__}', (cls, ), attrs, )


#
# Mixins
#
class SearchOptionsMixin:
    """Customization of search options."""

    @classmethod
    def customize(cls, opts):
        """Customize the search options."""
        attrs = {}
        if opts.facets:
            attrs['facets'] = opts.facets
        if opts.sort_options:
            attrs['sort_options'] = opts.sort_options
            attrs['sort_default'] = opts.sort_default
            attrs['sort_default_no_query'] = opts.sort_default_no_query
        return _make_cls(cls, attrs) if attrs else cls


class FileConfigMixin:
    """Shared customization for file service configs."""

    @classmethod
    def customize(cls, permission_policy=None):
        """Class method to customize the config for an instance."""
        attrs = {}
        # Permission policy
        if permission_policy:
            attrs['permission_policy_cls'] = permission_policy
        # Create the config class
        return _make_cls(cls, attrs) if attrs else cls


class RecordConfigMixin:
    """Shared customization for record service configs."""

    @classmethod
    def customize(cls, permission_policy=None, pid_providers=None, pids=None,
                  doi_enabled=False, **kwargs):
        """Class method to customize the config for an instance."""
        attrs = {}

        # Permission policy
        if permission_policy:
            attrs['permission_policy_cls'] = permission_policy

        # Search options
        for opt in ['search', 'search_drafts', 'search_versions']:
            if opt in kwargs:
                search_opt_cls = getattr(cls, opt)
                attrs[opt] = search_opt_cls.customize(kwargs[opt])

        # PID Providers and required PIDs
        attrs['pids_providers'] = {}
        attrs['pids_required'] = []
        providers = {p.name: p for p in pid_providers}

        for scheme, conf in pids.items():
            if scheme == 'doi' and not doi_enabled:
                continue
            if conf.get('required', False):
                attrs['pids_required'].append(scheme)

            attrs['pids_providers'][scheme] = {
                "default": None,
            }
            for name in conf.get("providers", []):
                attrs['pids_providers'][scheme][name] = providers[name]
                if attrs['pids_providers'][scheme]['default'] is None:
                    attrs['pids_providers'][scheme]['default'] = name

        # Create the config class
        return _make_cls(cls, attrs)
