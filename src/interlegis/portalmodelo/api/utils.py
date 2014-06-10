# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime
from DateTime import DateTime
from plone.app.blob.field import BlobWrapper
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from z3c.relationfield.interfaces import IRelationValue


# XXX: can we reduce complexity here?
def type_cast(value, fieldname=None, obj=None):  # noqa
    """Convert the value to something serializable.

    :param value: [required] value to be converted
    :type value: almost anything
    :returns: serializable value
    :rtype: str
    """
    if value is None:
        return ''

    elif isinstance(value, date):
        return value.isoformat()

    elif isinstance(value, datetime):
        return value.isoformat()

    elif isinstance(value, DateTime):
        return value.ISO()

    elif isinstance(value, NamedBlobFile):
        path = '{0}/@@downloads/{1}'.format(obj.absolute_url(), value.filename)
        return {'uri': path,
                'size': value.size,
                'filename': value.filename}

    elif isinstance(value, NamedBlobImage) or isinstance(value, BlobWrapper):
        path = '{0}/@@images/{1}'.format(obj.absolute_url(), fieldname)
        return {'uri': path,
                'size': value.size(),
                'filename': value.filename,
                'width': value.width,
                'height': value.height}

    elif IRelationValue.providedBy(value):
        # return just the path to the related object for now
        return value.to_path

    elif isinstance(value, list):
        # XXX: we don't want to mess around the original list
        # object so we just create a copy of the value
        tmp = list(value)
        for i in tmp:
            # call function recursively on each value of the list
            if type(i) == dict:
                tmp[tmp.index(i)] = dict(
                    (v[0], type_cast(v[1])) for v in i.items())
            else:
                tmp[tmp.index(i)] = type_cast(i)
        return tmp

    return value
