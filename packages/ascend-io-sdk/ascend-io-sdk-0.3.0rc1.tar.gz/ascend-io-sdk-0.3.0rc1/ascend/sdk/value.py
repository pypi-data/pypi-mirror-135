import ascend.protos.ascend.ascend_pb2 as ascend


def Bool(value: bool) -> ascend.Value:
  return ascend.Value(bool_value=value)


def Date(value=None) -> ascend.Value:
  return ascend.Value(date_value=value)


def DateTime(value=None) -> ascend.Value:
  return ascend.Value(datetime_value=value)


def Double(value=None) -> ascend.Value:
  return ascend.Value(double_value=value)


def Int(value: int) -> ascend.Value:
  return ascend.Value(int_value=value)


def Long(value=None) -> ascend.Value:
  return ascend.Value(long_value=value)


def Short(value=None) -> ascend.Value:
  return ascend.Value(short_value=value)


def String(value: str) -> ascend.Value:
  return ascend.Value(string_value=value)


def Struct(fields=None) -> ascend.Value:
  return ascend.Value(struct_value=ascend.Struct(fields=fields))


def Timestamp(value=None) -> ascend.Value:
  return ascend.Value(timestamp_value=value)


def Union(tag, value=Struct(), fields=None) -> ascend.Value:
  if fields is not None:
    return ascend.Value(union_value=ascend.Union(tag=tag, value=Struct(fields)))
  else:
    return ascend.Value(union_value=ascend.Union(tag=tag, value=value))
