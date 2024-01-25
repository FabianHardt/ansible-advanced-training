# opitz_to_upper filter

def filter_to_upper(in_string):
  return in_string.upper()

# filter
class FilterModule(object):
  def filters(self):
    return {
      'opitz_to_upper': filter_to_upper
    }