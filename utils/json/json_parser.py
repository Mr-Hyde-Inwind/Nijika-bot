import json
import functools
import numbers

@functools.singledispatch
def _recursive_parse(obj):
  return obj
  # err_msg = 'Unsupported object type: %s' % type(obj).__name__
  # raise TypeError(err_msg)

@_recursive_parse.register(dict)
def _(json_dict: dict):
  for key in json_dict.keys():
    try:
      sub = json.loads(json_dict[key])
    except (ValueError, TypeError) as err:
      pass
    else:
      json_dict[key] = _recursive_parse(sub)
  return json_dict

@_recursive_parse.register(list)
def _(json_list: list):
  return [_recursive_parse(item) for item in json_list]

@_recursive_parse.register(str)
def _(json_str: str):
  try:
    json_item = json.loads(json_str)
  except (ValueError, TypeError) as err:
    return json_str
  else:
    return _recursive_parse(json_item)

def parse(obj):
  content = _recursive_parse(obj)
  if not isinstance(content, list):
    return [content]
  return content
