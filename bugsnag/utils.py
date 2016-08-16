from __future__ import division, print_function, absolute_import

import inspect
import traceback
import six

import bugsnag

try:
    import json
except ImportError:
    import simplejson as json


MAX_PAYLOAD_LENGTH = 128 * 1024
MAX_STRING_LENGTH = 1024


def sanitize_object(obj, **kwargs):
    filters = kwargs.get("filters", [])
    ignored = kwargs.get("ignored", [])
    kwargs["ignored"] = ignored

    if id(obj) in ignored:
        return "[RECURSIVE]"
    if isinstance(obj, dict):
        ignored.append(id(obj))
        clean_dict = {}
        for k, v in six.iteritems(obj):
            # Remove values for keys matching filters
            is_string = isinstance(k, six.string_types)
            if is_string and any(f.lower() in k.lower() for f in filters):
                clean_dict[k] = "[FILTERED]"
            else:
                clean_obj = sanitize_object(v, **kwargs)
                if clean_obj is not None:
                    clean_dict[k] = clean_obj

        return clean_dict
    elif any(isinstance(obj, t) for t in (list, set, tuple)):
        ignored.append(id(obj))
        return [sanitize_object(x, **kwargs) for x in obj]
    elif any(isinstance(obj, t) for t in (bool, float, int)):
        return obj
    elif obj is None:
        return obj
    else:
        try:
            if six.PY3 and isinstance(obj, bytes):
                string = six.text_type(obj, encoding='utf-8', errors='replace')
            else:
                string = six.text_type(obj)

        except Exception:
            exc = traceback.format_exc()
            bugsnag.warn("Could not add object to metadata: %s" % exc)
            string = "[BADENCODING]"

        return string


def shrink_object(obj):
    if isinstance(obj, six.string_types):
        return obj[:MAX_STRING_LENGTH]

    elif isinstance(obj, dict):
        for k, v in six.iteritems(obj):
            obj[k] = shrink_object(v)

    elif any(isinstance(obj, t) for t in (list, set, tuple)):
        return [shrink_object(x) for x in obj]

    return obj


def json_encode(obj):

    payload = json.dumps(obj)

    if len(payload) > MAX_PAYLOAD_LENGTH:
        obj = shrink_object(json.loads(payload))
        payload = json.dumps(obj)

    return payload.encode('utf-8', 'replace')


def fully_qualified_class_name(obj):
    module = inspect.getmodule(obj)
    if module is not None and module.__name__ != "__main__":
        return module.__name__ + "." + obj.__class__.__name__
    else:
        return obj.__class__.__name__


def package_version(package_name):
    try:
        import pkg_resources
    except ImportError:
        return None
    else:
        try:
            return pkg_resources.get_distribution(package_name).version
        except pkg_resources.DistributionNotFound:
            return None
