# -*- coding: utf-8 -*-
#
# This file is part of CERN Open Data Portal.
# Copyright (C) 2017 CERN.
#
# CERN Open Data Portal is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Open Data Portal is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Open Data Portal; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""CERN Open Data theme."""

from __future__ import absolute_import, print_function

import operator

from flask import Blueprint

blueprint = Blueprint(
    'cernopendata_theme',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.app_template_filter('get_record_title')
def get_record_title(recid):
    """Fetches record title by id."""
    from invenio_records.api import Record
    from invenio_pidstore.models import PersistentIdentifier
    from invenio_pidstore.errors import PIDDoesNotExistError
    try:
        pid = PersistentIdentifier.get('recid', recid)
    except PIDDoesNotExistError:
        return None
    record = Record.get_record(pid.object_uuid)
    return record.get('title', '')


@blueprint.app_template_filter('get_first_file')
def get_first_file(file_list):
    """Fetches first file from a list."""
    l = [f.get('key') for f in file_list
         if f.get('key', '').endswith('.ig')]
    if l:
        return l[0]


@blueprint.app_template_filter('sort_multi')
def sort_multi(l, *operators):
    """Sorts list by multiple fields."""
    l.sort(key=operator.itemgetter(*operators))
    return l
