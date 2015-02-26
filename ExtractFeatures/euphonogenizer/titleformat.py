#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ai

from __future__ import unicode_literals

import binascii
import codecs
import itertools
import os
import platform
import random
import re
import sys
import unicodedata

from common import dbg, unistr


def magic_map_filename(formatter, track):
  value = track.get('@')
  if value is not None and value is not False:
    return unistr(foo_filename(None, None, [value]))
  return None

def magic_map_filename_ext(formatter, track):
  value = track.get('@')
  if value is not None and value is not False:
    filename = unistr(foo_filename(None, None, [value]))
    ext = unistr(foo_ext(None, None, [value]))
    if ext:
      filename += '.' + ext
    return filename
  return None

def magic_map_track_artist(formatter, track):
  artist = formatter.magic_resolve_variable(track, 'artist')
  album_artist = formatter.magic_resolve_variable(track, 'album artist')
  if artist != album_artist:
    return artist
  return None

def magic_map_tracknumber(formatter, track):
  value = track.get('TRACKNUMBER')
  if value is not None and value is not False:
    return value.zfill(2)
  return None

def magic_map_track_number(formatter, track):
  value = track.get('TRACKNUMBER')
  if value is not None and value is not False:
    return unistr(int(value))
  return None


magic_mappings = {
    'album artist': ['ALBUM ARTIST', 'ARTIST', 'COMPOSER', 'PERFORMER'],
    'album': ['ALBUM', 'VENUE'],
    'artist': ['ARTIST', 'ALBUM ARTIST', 'COMPOSER', 'PERFORMER'],
    'discnumber': ['DISCNUMBER', 'DISC'],
    'filename': magic_map_filename,
    'filename_ext': magic_map_filename_ext,
    'track artist': magic_map_track_artist,
    'title': ['TITLE', '@'],
    'tracknumber': magic_map_tracknumber,
    'track number': magic_map_track_number,
    '_date_': ['DATE'],
}

def __foo_bool(b):
  if b:
    return True
  return False

def __foo_int(n):
  # Note that this "string value" might actually already be an int, in which
  # case, this function simply ends up stripping the atom wrapper.
  try:
    if n is not None and n != '':
      return int(n.string_value)
  except AttributeError:
    try:
      return int(n)
    except ValueError:
      return 0
  return 0

def __foo_va_conv_n(n):
  strval = ''
  truth = False

  integer_value = 0

  try:
    strval = n.string_value
    truth = n.truth_value
  except AttributeError:
    strval = n

  if strval:
    try:
      integer_value = int(strval)
    except ValueError:
      try:
        start = 1 if strval[0] == '-' else 0
        last_found_number = -1
        try:
          for i in range(start, len(strval)):
            if int(strval[i]) > 0:
              last_found_number = i
        except ValueError:
          if last_found_number >= 0:
            integer_value = int(strval[0:last_found_number+1])
      except ValueError:
        pass
      except KeyError:
        pass

  return EvaluatorAtom(integer_value, truth)

def __foo_va_conv_n_lazy(n):
  try:
    value = n.eval()
    if value.string_value:
      return __foo_va_conv_n(value.string_value)
  except AttributeError:
    return n
  return 0

def __foo_va_conv_bool_lazy(b):
  try:
    value = b.eval()
    try:
      return value.truth_value
    except AttributeError:
      return value
  except AttributeError:
    if b:
      return True
  return False

def __foo_va_conv_n_lazy_int(n):
  return __foo_int(__foo_va_conv_n_lazy(n))

def __foo_va_lazy(x):
  return x.eval()

def __foo_is_word_sep(c):
  return c in ' /\\()[]'

def foo_true(track, memory, va):
  return True

def foo_false(track, memory, va):
  pass

def foo_zero(track, memory, va):
  return '0'

def foo_one(track, memory, va):
  return '1'

def foo_nop(track, memory, va):
  return va[0].eval()

def foo_if_arity2(track, memory, va_cond_then):
  if va_cond_then[0].eval():
    return va_cond_then[1].eval()

def foo_if_arity3(track, memory, va_cond_then_else):
  if va_cond_then_else[0].eval():
    return va_cond_then_else[1].eval()
  return va_cond_then_else[2].eval()

def foo_if2(track, memory, va_a_else):
  return va_a_else[0].eval() if va_a_else[0].eval() else va_a_else[1].eval()

def foo_if3(track, memory, va_a1_a2_aN_else):
  for i in range(0, len(va_a1_a2_aN_else) - 1):
    if va_a1_a2_aN_else[i].eval():
      return va_a1_a2_aN_else[i].eval()
  return va_a1_a2_aN_else[-1].eval()

def foo_ifequal(track, memory, va_n1_n2_then_else):
  n1 = __foo_va_conv_n_lazy_int(va_n1_n2_then_else[0])
  n2 = __foo_va_conv_n_lazy_int(va_n1_n2_then_else[1])
  if n1 == n2:
    return va_n1_n2_then_else[2].eval()
  return va_n1_n2_then_else[3].eval()

def foo_ifgreater(track, memory, va_n1_n2_then_else):
  n1 = __foo_va_conv_n_lazy_int(va_n1_n2_then_else[0])
  n2 = __foo_va_conv_n_lazy_int(va_n1_n2_then_else[1])
  if n1 > n2:
    return va_n1_n2_then_else[2].eval()
  return va_n1_n2_then_else[3].eval()

def foo_iflonger(track, memory, va_s_n_then_else):
  n = __foo_va_conv_n_lazy_int(va_s_n_then_else[1])
  if len(va_s_n_then_else[0].eval()) > n:
    return va_s_n_then_else[2].eval()
  return va_n1_n2_then_else[3].eval()

def foo_select(track, memory, va_n_a1_aN):
  n = __foo_va_conv_n_lazy_int(va_n_a1_aN[0])
  if n > 0 and n <= len(va_n_a1_aN) - 1:
    return va_n_a1_aN[n].eval()

def foo_add(track, memory, va_aN):
  return sum(map(__foo_va_conv_n_lazy_int, va_aN))

def foo_div(track, memory, va_aN):
  return reduce(lambda x, y: x // y, map(__foo_va_conv_n_lazy_int, va_aN))

def foo_greater(track, memory, va_a_b):
  a = __foo_va_conv_n_lazy_int(va_a_b[0])
  b = __foo_va_conv_n_lazy_int(va_a_b[1])
  if a > b:
    return True
  return False

def foo_max(track, memory, va_a_b):
  value = foo_ifgreater(track, memory, va_a_b + va_a_b)
  return EvaluatorAtom(__foo_int(__foo_va_conv_n(value)), __foo_bool(value))

def foo_maxN(track, memory, va_aN):
  return reduce(lambda x, y: foo_max(track, memory, [x, y]), va_aN)

def foo_min(track, memory, va_a_b):
  value = foo_ifgreater(track, memory, va_a_b + reverse(va_a_b))
  return EvaluatorAtom(__foo_int(__foo_va_conv_n(value)), __foo_bool(value))

def foo_minN(track, memory, va_aN):
  return reduce(lambda x, y: foo_min(track, memory, [x, y]), va_aN)

def foo_mod(track, memory, va_a_b):
  a = __foo_va_conv_n_lazy_int(va_a_b[0])
  b = __foo_va_conv_n_lazy_int(va_a_b[1])
  if not b:
    return a
  return a % b

def foo_modN(track, memory, va_aN):
  return reduce(lambda x, y: foo_mod(track, memory, [x, y]),
      map(__foo_va_conv_n_lazy_int, va_aN))

def foo_mul(track, memory, va_aN):
  return reduce(lambda x, y: x * y, map(__foo_va_conv_n_lazy_int, va_aN))

def foo_muldiv(track, memory, va_a_b_c):
  c = __foo_va_conv_n_lazy_int(va_a_b_c[2])
  return (foo_mul(track, memory, [va_a_b_c[0], va_a_b_c[1]]) + c // 2) // c

def foo_rand(track, memory, va):
  random.seed()
  return random.randint(0, sys.maxint)

def foo_sub(track, memory, va_aN):
  return reduce(lambda x, y: x - y, map(__foo_va_conv_n_lazy_int, va_aN))

def foo_and(track, memory, va_N):
  for each in va_N:
    if not __foo_va_conv_bool_lazy(each):
      return False
  return True

def foo_or(track, memory, va_N):
  for each in va_N:
    if __foo_va_conv_bool_lazy(each):
      return True
  return False

def foo_not(track, memory, va_x):
  return not __foo_va_conv_bool_lazy(va_x[0])

def foo_xor(track, memory, va_N):
  return reduce(lambda x, y: x ^ y, map(__foo_va_conv_bool_lazy, va_N))

def foo_abbr(string_value):
  parts = re.sub('[()]', '', string_value).split()
  abbr = ''
  for each in parts:
    if each[0].isalnum():
      abbr += each[0]
    else:
      abbr += each
  return abbr

def foo_abbr_arity1(track, memory, va_x):
  x = va_x[0].eval()
  abbr = foo_abbr(unistr(x))
  return EvaluatorAtom(abbr, __foo_bool(x))

def foo_abbr_arity2(track, memory, va_x_len):
  x = va_x_len[0].eval()
  length = __foo_va_conv_n_lazy_int(va_x_len[1])
  if len(unistr(x)) > length:
    return foo_abbr_arity1(track, memory, [x])
  return x

def foo_ansi(track, memory, va_x):
  x = va_x[0].eval()
  # Doing the conversion this way will probably not produce the same output with
  # wide characters as Foobar, which produces two '??' instead of one. I don't
  # have a multibyte build of Python lying around right now, so I can't
  # confirm at the moment. But really, it probably doesn't matter.
  result = unistr(unistr(x).encode('latin-1', errors='replace'))
  return EvaluatorAtom(result, __foo_bool(x))

def foo_ascii(track, memory, va_x):
  x = va_x[0].eval()
  result = unistr(unistr(x).encode('ascii', errors='replace'))
  return EvaluatorAtom(result, __foo_bool(x))

def foo_caps_impl(va_x, lower):
  x = va_x[0].eval()
  result = ''
  new_word = True
  for c in unistr(x):
    if __foo_is_word_sep(c):
      new_word = True
      result += c
    else:
      if new_word:
        result += c.upper()
        new_word = False
      else:
        if lower:
          result += c.lower()
        else:
          result += c
  return EvaluatorAtom(result, __foo_bool(x))

def foo_caps(track, memory, va_x):
  return foo_caps_impl(va_x, lower=True)

def foo_caps2(track, memory, va_x):
  return foo_caps_impl(va_x, lower=False)

def foo_char(track, memory, va_x):
  x = __foo_va_conv_n_lazy_int(va_x[0])
  if x <= 0:
    return ''
  try:
    return unichr(x)
  except ValueError:
    # Also happens when using a narrow Python build
    return '?'
  except OverflowError:
    return ''

def foo_crc32(track, memory, va_x):
  x = va_x[0].eval()
  crc = binascii.crc32(unistr(x))
  return EvaluatorAtom(crc, __foo_bool(x))

def foo_crlf(track, memory, va):
  return '\r\n'

def foo_cut(track, memory, va_a_len):
  return foo_left(track, memory, va_a_len)

def foo_directory_arity1(track, memory, va_x):
  x = va_x[0].eval()
  parts = re.split('[\\\\/:|]', unistr(x))
  if len(parts) < 2:
    return EvaluatorAtom('', __foo_bool(x))
  return EvaluatorAtom(parts[-2], __foo_bool(x))

def foo_directory_arity2(track, memory, va_x_n):
  x = va_x_n[0].eval()
  n = __foo_va_conv_n_lazy_int(va_x_n[1])
  if n <= 0:
    return EvaluatorAtom('', __foo_bool(x))
  parts = re.split('[\\\\/:|]', unistr(x))
  parts_len = len(parts)
  if n >= parts_len or parts_len < 2:
    return EvaluatorAtom('', __foo_bool(x))
  return EvaluatorAtom(parts[parts_len - n - 1], __foo_bool(x))

def foo_directory_path(track, memory, va_x):
  x = va_x[0].eval()
  parts = re.split('[\\\\/:|]', unistr(x)[::-1], 1)
  if len(parts) < 2:
    return EvaluatorAtom('', __foo_bool(x))
  return EvaluatorAtom(parts[1][::-1], __foo_bool(x))

def foo_ext(track, memory, va_x):
  x = va_x[0]

  try:
    x = x.eval()
  except AttributeError:
    pass

  ext = unistr(x).split('.')[-1]
  for c in ext:
    if c in '/\\|:':
      return EvaluatorAtom('', __foo_bool(x))
  return EvaluatorAtom(ext.split('?')[0], __foo_bool(x))

def foo_filename(track, memory, va_x):
  x = va_x[0]

  try:
    x = x.eval()
  except AttributeError:
    pass

  x_str = unistr(x)
  parts = re.split('[\\\\/:|]', x_str)
  parts_len = len(parts)
  if parts_len <= 0:
    return EvaluatorAtom('', __foo_bool(x))
  filename = x_str
  if parts_len >= 2:
    filename = parts[-1]
  return EvaluatorAtom(filename[::-1].split('.', 1)[-1][::-1], __foo_bool(x))

def foo_fix_eol_arity1(track, memory, va_x):
  return foo_fix_eol_arity2(track, memory, va_x + [' (...)'])

def foo_fix_eol_arity2(track, memory, va_x_indicator):
  x = va_x_indicator[0].eval()
  indicator = va_x_indicator[1]

  try:
    indicator = unistr(indicator.eval())
  except AttributeError:
    pass

  result = unistr(x).split('\r\n')[0].split('\n')[0]

  return EvaluatorAtom(result + indicator, __foo_bool(x))

def foo_hex_arity1(track, memory, va_n):
  return foo_hex_arity2(track, memory, [va_n[0], 0])

def foo_hex_arity2(track, memory, va_n_len):
  n = __foo_va_conv_n_lazy_int(va_n_len[0])
  length = __foo_va_conv_n_lazy_int(va_n_len[1])
  if length < 0:
    length = 0
  value = None
  if n < 0:
    value = hex(((abs(n) ^ 0xFFFFFFFF) + 1) & 0xFFFFFFFF)
  elif n > 2**63-1:
    value = '0xFFFFFFFF'
  else:
    value = hex(n)
  hex_value = value.split('L')[0][2:]
  if len(hex_value) > 8:
    hex_value = hex_value[-8:]
  return hex_value.upper().zfill(length)

def foo_insert(track, memory, va_a_b_n):
  a = va_a_b_n[0].eval()
  a_str = unistr(a)
  b = va_a_b_n[1].eval()
  b_str = unistr(b)
  n = __foo_va_conv_n_lazy_int(va_a_b_n[2])
  return EvaluatorAtom(a_str[0:n] + b_str + a_str[n:], __foo_bool(a))

def foo_left(track, memory, va_a_len):
  a = va_a_len[0].eval()
  length = __foo_va_conv_n_lazy_int(va_a_len[1])
  a_str = unistr(a)
  a_len = len(a_str)
  if length < 0 or a_len == 0 or length >= a_len:
    return a
  elif length == 0:
    return EvaluatorAtom('', __foo_bool(a))
  return EvaluatorAtom(a_str[0:length], __foo_bool(a))

def foo_len(track, memory, va_a):
  a = va_a[0].eval()
  return EvaluatorAtom(len(unistr(a)), __foo_bool(a))

def foo_len2(track, memory, va_a):
  a = va_a[0].eval()
  length = 0
  str_a = unistr(a)
  for c in str_a:
    width = unicodedata.east_asian_width(c)
    if width == 'N' or width == 'Na' or width == 'H':
      # Narrow / Halfwidth character
      length += 1
    elif width == 'W' or width == 'F' or width == 'A':
      # Wide / Fullwidth / Ambiguous character
      length += 2
  return EvaluatorAtom(length, __foo_bool(a))

def foo_longer(track, memory, va_a_b):
  len_a = len(unistr(va_a_b[0].eval()))
  len_b = len(unistr(va_a_b[1].eval()))
  return len_a > len_b

def foo_lower(track, memory, va_a):
  a = va_a[0].eval()
  return EvaluatorAtom(unistr(a).lower(), __foo_bool(a))

def foo_longest(track, memory, va_a1_aN):
  longest = None
  longest_len = -1
  for each in va_a1_aN:
    current = each.eval()
    current_len = len(unistr(current))
    if current_len > longest_len:
      longest = current
      longest_len = current_len
  return longest

def foo_num(track, memory, va_n_len):
  n = va_n_len[0].eval()
  length = __foo_va_conv_n_lazy_int(va_n_len[1])
  string_value = None
  if (length > 0):
    string_value = unistr(__foo_va_conv_n(n)).zfill(length)
  else:
    string_value = unistr(__foo_int(__foo_va_conv_n(n)))
  return EvaluatorAtom(string_value, __foo_bool(n))

def foo_pad_universal(va_x_len_char, right):
  x = va_x_len_char[0].eval()
  length = __foo_va_conv_n_lazy_int(va_x_len_char[1])
  char = va_x_len_char[2]

  try:
    char = unistr(char.eval())[0]
  except AttributeError:
    pass

  if not char:
    return x

  x_str = unistr(x)
  x_len = len(x_str)

  if x_len < length:
    padded = None
    if not right:
      padded = x_str + char * (length - x_len)
    else:
      padded = char * (length - x_len) + x_str
    return EvaluatorAtom(padded, __foo_bool(x))
  return x

def foo_pad_arity2(track, memory, va_x_len):
  return foo_pad_arity3(track, memory, va_x_len + [' '])

def foo_pad_arity3(track, memory, va_x_len_char):
  return foo_pad_universal(va_x_len_char, right=False)

def foo_pad_right_arity2(track, memory, va_x_len):
  return foo_pad_right_arity3(track, memory, va_x_len + [' '])

def foo_pad_right_arity3(track, memory, va_x_len_char):
  return foo_pad_universal(va_x_len_char, right=True)

def foo_padcut(track, memory, va_x_len):
  cut = foo_cut(track, memory, va_x_len)
  return foo_pad_arity2(track, memory, [cut, va_x_len[1]])

def foo_padcut_right(track, memory, va_x_len):
  cut = foo_cut(track, memory, va_x_len)
  return foo_pad_right_arity2(track, memory, [cut, va_x_len[1]])

def foo_progress_universal(va_pos_range_len_a_b, is2):
  pos = va_pos_range_len_a_b[0].eval()
  range_value = va_pos_range_len_a_b[1].eval()
  length = __foo_va_conv_n_lazy_int(va_pos_range_len_a_b[2])
  a = unistr(va_pos_range_len_a_b[3].eval())
  b = unistr(va_pos_range_len_a_b[4].eval())
  pos_int = __foo_int(__foo_va_conv_n(pos))
  range_int = __foo_int(__foo_va_conv_n(range_value))

  if pos_int > range_int:
    pos_int = range_int
  elif pos_int < 0:
    pos_int = 0

  progress = None

  if not is2:
    cursor_pos = 0

    if range_int == 0:
      if __foo_va_conv_n_lazy_int(pos) > 0:
        progress = a + b * (length - 1)
      else:
        progress = b * (length - 1) + a
    else:
      cursor_pos = (pos_int * length + range_int // 2) // range_int

      # This appears to be a foobar2000 bug. The cursor position is off by one.
      # Remove this line if the bug is ever fixed.
      cursor_pos += 1

      if cursor_pos <= 0:
        cursor_pos = 1
      elif cursor_pos >= length:
        cursor_pos = length

      progress = a * (cursor_pos - 1) + b + a * (length - cursor_pos)
  else:
    if range_int == 0:
      if __foo_va_conv_n_lazy_int(pos) > 0:
        progress = a * length
      else:
        progress = b * length
    else:
      left_count = pos_int * length // range_int

      progress = a * left_count + b * (length - left_count)

  return EvaluatorAtom(progress, foo_and(None, [pos, range_value]))

def foo_progress(track, memory, va_pos_range_len_a_b):
  return foo_progress_universal(va_pos_range_len_a_b, False)

def foo_progress2(track, memory, va_pos_range_len_a_b):
  return foo_progress_universal(va_pos_range_len_a_b, True)

def foo_repeat(track, memory, va_a_n):
  a = va_a_n[0].eval()
  n = __foo_va_conv_n_lazy_int(va_a_n[1])
  return EvaluatorAtom(unistr(a) * n, __foo_bool(a))

def foo_replace_explode_recursive(a, va_a_bN_cN, i):
  if i + 1 < len(va_a_bN_cN):
    b = unistr(va_a_bN_cN[i].eval())
    splits = a.split(b)
    current = []
    for each in splits:
      sub_splits = foo_replace_explode_recursive(each, va_a_bN_cN, i + 2)
      if sub_splits is not None:
        current.append(sub_splits)
    if not current:
      current = splits
    return current

def foo_replace_join_recursive(splits, va_a_bN_cN, i):
  if i < len(va_a_bN_cN):
    current = []
    for each in splits:
      sub_joined = foo_replace_join_recursive(each, va_a_bN_cN, i + 2)
      if sub_joined is not None:
        current.append(sub_joined)
    c = unistr(va_a_bN_cN[i].eval())
    if not current:
      current = splits
    joined = c.join(current)
    return joined

def foo_replace(track, memory, va_a_bN_cN):
  a = va_a_bN_cN[0].eval()
  splits = foo_replace_explode_recursive(unistr(a), va_a_bN_cN, 1)
  result = foo_replace_join_recursive(splits, va_a_bN_cN, 2)
  # Truthfully, I have no idea if this is actually right, but it's probably good
  # enough for what it does. The sample cases check out, at least.
  return EvaluatorAtom(result, __foo_bool(a))

def foo_right(track, memory, va_a_len):
  a = va_a_len[0].eval()
  length = __foo_va_conv_n_lazy_int(va_a_len[1])
  a_str = unistr(a)
  a_len = len(a_str)
  if a_len == 0 or length >= a_len:
    return a
  elif length <= 0:
    return EvaluatorAtom('', __foo_bool(a))
  return EvaluatorAtom(a_str[a_len-length:], __foo_bool(a))

__roman_numerals = (
    ('M',  1000),
    ('CM', 900),
    ('D',  500),
    ('CD', 400),
    ('C',  100),
    ('XC', 90),
    ('L',  50),
    ('XL', 40),
    ('X',  10),
    ('IX', 9),
    ('V',  5),
    ('IV', 4),
    ('I',  1),
)

def foo_roman(track, memory, va_n):
  n = va_n[0].eval()
  n_int = __foo_int(__foo_va_conv_n(n))
  result = ''
  if n_int > 0 and n_int <= 100000:
    for numeral, value in __roman_numerals:
      while n_int >= value:
        result += numeral
        n_int -= value
  return EvaluatorAtom(result, __foo_bool(n))

def foo_rot13(track, memory, va_a):
  a = va_a[0].eval()
  rot = codecs.encode(unistr(a), 'rot_13')
  return EvaluatorAtom(rot, __foo_bool(a))

def foo_shortest(track, memory, va_aN):
  shortest = None
  shortest_len = -1
  for each in va_aN:
    current = each.eval()
    current_len = len(unistr(current))
    if shortest_len == -1 or current_len < shortest_len:
      shortest = current
      shortest_len = current_len
  return shortest

def foo_strchr(track, memory, va_s_c):
  s = unistr(va_s_c[0].eval())
  c = unistr(va_s_c[1].eval())
  if c:
    c = c[0]
    for i, char in enumerate(s):
      if c == char:
        return EvaluatorAtom(i + 1, True)
  return EvaluatorAtom(0, False)

def foo_strrchr(track, memory, va_s_c):
  s = unistr(va_s_c[0].eval())
  c = unistr(va_s_c[1].eval())
  if c:
    c = c[0]
    for i, char in itertools.izip(reversed(xrange(len(s))), reversed(s)):
      if c == char:
        return EvaluatorAtom(i + 1, True)
  return EvaluatorAtom(0, False)

def foo_strstr(track, memory, va_s1_s2):
  s1 = unistr(va_s1_s2[0].eval())
  s2 = unistr(va_s1_s2[1].eval())
  found_index = 0
  if s1 and s2:
    found_index = s1.find(s2) + 1
  return EvaluatorAtom(found_index, __foo_bool(found_index))

def foo_strcmp(track, memory, va_s1_s2):
  s1 = va_s1_s2[0].eval()
  s2 = va_s1_s2[1].eval()
  if unistr(s1) == unistr(s2):
    return EvaluatorAtom(1, True)
  return EvaluatorAtom('', False)

def foo_stricmp(track, memory, va_s1_s2):
  s1 = va_s1_s2[0].eval()
  s2 = va_s1_s2[1].eval()
  if unistr(s1).lower() == unistr(s2).lower():
    return EvaluatorAtom(1, True)
  return EvaluatorAtom('', False)

def foo_substr(track, memory, va_s_m_n):
  s = va_s_m_n[0].eval()
  m = __foo_va_conv_n_lazy_int(va_s_m_n[1]) - 1
  n = __foo_va_conv_n_lazy_int(va_s_m_n[2])
  if n < m:
    return EvaluatorAtom('', __foo_bool(s))
  if m < 0:
    m = 0
  s_str = unistr(s)
  s_len = len(s_str)
  result = None
  if n > s_len:
    n = s_len
  if m == 0 and n == s_len:
    return s
  elif n == s_len:
    result = s_str[m:]
  else:
    result = s_str[m:n]
  return EvaluatorAtom(result, __foo_bool(s))

def foo_strip_swap_prefix(va_x_prefixN, should_swap):
  x = va_x_prefixN[0].eval()
  x_str = unistr(x)
  x_str_lower = x_str.lower()

  for i in range(1, len(va_x_prefixN)):
    prefix = va_x_prefixN[i]

    try:
      prefix = unistr(prefix.eval())
    except AttributeError:
      pass

    if x_str_lower.startswith(prefix.lower() + ' '):
      prefix_len = len(prefix)
      result = x_str[prefix_len+1:]

      if should_swap:
        actual_prefix = x_str[0:prefix_len]
        result += ', ' + actual_prefix

      return EvaluatorAtom(result, __foo_bool(x))

  return x

def foo_stripprefix_arity1(track, memory, va_x):
  return foo_stripprefix_arityN(track, memory, va_x + ['A', 'The'])

def foo_stripprefix_arityN(track, memory, va_x_prefixN):
  return foo_strip_swap_prefix(va_x_prefixN, False)

def foo_swapprefix_arity1(track, memory, va_x):
  return foo_swapprefix_arityN(track, memory, va_x + ['A', 'The'])

def foo_swapprefix_arityN(track, memory, va_x_prefixN):
  return foo_strip_swap_prefix(va_x_prefixN, True)

def foo_trim(track, memory, va_s):
  s = va_s[0].eval()
  return EvaluatorAtom(unistr(s).strip(), __foo_bool(s))

def foo_tab_arity0(track, memory, va):
  return '\t'

def foo_tab_arity1(track, memory, va_n):
  n = __foo_va_conv_n_lazy_int(va_n[0])
  if n < 0 or n > 16:
    n = 16
  return '\t' * n

def foo_upper(track, memory, va_s):
  s = va_s[0].eval()
  return EvaluatorAtom(unistr(s).upper(), __foo_bool(s))

def foo_meta_arity1(track, memory, va_name):
  return foo_meta_sep_arity2(track, memory, va_name + [', '])

def foo_meta_arity2(track, memory, va_name_n):
  name = unistr(va_name_n[0].eval())
  n = __foo_va_conv_n_lazy_int(va_name_n[1])
  if n < 0:
    return False
  value = track.get(name)
  if not value:
    value = track.get(name.upper())
    if not value:
      return False
  if isinstance(value, list):
    if n >= len(value):
      return False
    value = value[n]
  elif n != 0:
    return False
  return EvaluatorAtom(value, True)

def foo_meta_sep_arity2(track, memory, va_name_sep):
  name = unistr(va_name_sep[0].eval())

  sep = va_name_sep[1]
  try:
    sep = unistr(sep.eval())
  except AttributeError:
    pass

  value = track.get(name)
  if not value:
    value = track.get(name.upper())
    if not value:
      return False
  if isinstance(value, list):
    value = sep.join(value)
  return EvaluatorAtom(value, True)

def foo_meta_sep_arity3(track, memory, va_name_sep_lastsep):
  name = unistr(va_name_sep_lastsep[0].eval())
  sep = unistr(va_name_sep_lastsep[1].eval())
  lastsep = unistr(va_name_sep_lastsep[2].eval())
  value = track.get(name)
  if not value:
    value = track.get(name.upper())
    if not value:
      return False
  if isinstance(value, list):
    if len(value) > 1:
      value = sep.join(value[:-1]) + lastsep + value[-1]
    else:
      value = value[0]
  return EvaluatorAtom(value, True)

def foo_meta_test(track, memory, va_nameN):
  for each in va_nameN:
    name = unistr(each.eval())
    value = track.get(name)
    if not value:
      value = track.get(name.upper())
      if not value:
        return False
  return EvaluatorAtom(1, True)

def foo_meta_num(track, memory, va_name):
  name = unistr(va_name[0].eval())
  value = track.get(name)
  if not value:
    value = track.get(name.upper())
    if not value:
      return 0
  if isinstance(value, list):
    return EvaluatorAtom(len(value), True)
  return EvaluatorAtom(1, True)

def foo_get(track, memory, va_name):
  name = va_name[0].eval()
  name_str = unistr(name)
  if name_str == '':
    return False
  value = memory.get(name_str)
  if value is not None and value is not False and value != '':
    return EvaluatorAtom(value, True)
  return False

def foo_put(track, memory, va_name_value):
  name = unistr(va_name_value[0].eval())
  value = va_name_value[1].eval()
  if name != '':
    memory[name] = unistr(value)
  return value

def foo_puts(track, memory, va_name_value):
  value = foo_put(track, memory, va_name_value)
  return __foo_bool(value)


foo_function_vtable = {
    'if': {'2': foo_if_arity2, '3': foo_if_arity3},
    'if2': {'2': foo_if2},
    'if3': {'0': foo_false, '1': foo_nop, 'n': foo_if3},
    'ifequal': {'4': foo_ifequal},
    'ifgreater': {'4': foo_ifgreater},
    'iflonger': {'4': foo_iflonger},
    'select': {'0': foo_false, '1': foo_false, 'n': foo_select},
    'add': {'0': foo_zero, '1': foo_nop, 'n': foo_add},
    'div': {'0': foo_false, '1': foo_nop, 'n': foo_div},
    'greater': {'2': foo_greater},
    'max': {'0': foo_false, '1': foo_nop, '2': foo_max, 'n': foo_maxN},
    'min': {'0': foo_false, '1': foo_nop, '2': foo_min, 'n': foo_minN},
    'mod': {'0': foo_false, '1': foo_nop, '2': foo_mod, 'n': foo_modN},
    'mul': {'0': foo_one, '1': foo_nop, 'n': foo_mul},
    'muldiv': {'3': foo_muldiv},
    'rand': {'0': foo_rand},
    'sub': {'0': foo_false, 'n': foo_sub},
    'and': {'0': foo_true, '1': foo_nop, 'n': foo_and},
    'or': {'0': foo_false, '1': foo_nop, 'n': foo_or},
    'not': {'1': foo_not},
    'xor': {'0': foo_false, '1': foo_nop, 'n': foo_xor},
    'abbr': {'1': foo_abbr_arity1, '2': foo_abbr_arity2},
    'ansi': {'1': foo_ansi},
    'ascii': {'1': foo_ascii},
    'caps': {'1': foo_caps},
    'caps2': {'1': foo_caps2},
    'char': {'1': foo_char},
    'crc32': {'1': foo_crc32},
    'crlf': {'0': foo_crlf},
    'cut': {'2': foo_cut},
    'directory': {'1': foo_directory_arity1, '2': foo_directory_arity2},
    'directory_path': {'1': foo_directory_path},
    'ext': {'1': foo_ext},
    'filename': {'1': foo_filename},
    'fix_eol': {'1': foo_fix_eol_arity1, '2': foo_fix_eol_arity2},
    'hex': {'1': foo_hex_arity1, '2': foo_hex_arity2},
    'insert': {'3': foo_insert},
    'left': {'2': foo_left},
    'len': {'1': foo_len},
    'len2': {'1': foo_len2},
    'longer': {'2': foo_longer},
    'lower': {'1': foo_lower},
    'longest': {'0': foo_false, '1': foo_nop, 'n': foo_longest},
    'num': {'2': foo_num},
    'pad': {'2': foo_pad_arity2, '3': foo_pad_arity3},
    'pad_right': {'2': foo_pad_right_arity2, '3': foo_pad_right_arity3},
    'padcut': {'2': foo_padcut},
    'padcut_right': {'2': foo_padcut_right},
    'progress': {'5': foo_progress},
    'progress2': {'5': foo_progress2},
    'repeat': {'2': foo_repeat},
    'replace': {
        '0': foo_false,
        '1': foo_false,
        '2': foo_false,
        'n': foo_replace
    },
    'right': {'2': foo_right},
    'roman': {'1': foo_roman},
    'rot13': {'1': foo_rot13},
    'shortest': {'0': foo_false, '1': foo_nop, 'n': foo_shortest},
    'strchr': {'2': foo_strchr},
    'strrchr': {'2': foo_strrchr},
    'strstr': {'2': foo_strstr},
    'strcmp': {'2': foo_strcmp},
    'stricmp': {'2': foo_stricmp},
    'substr': {'3': foo_substr},
    'stripprefix': {
        '0': foo_false,
        '1': foo_stripprefix_arity1,
        'n': foo_stripprefix_arityN
    },
    'swapprefix': {
        '0': foo_false,
        '1': foo_swapprefix_arity1,
        'n': foo_swapprefix_arityN
    },
    'trim': {'1': foo_trim},
    'tab': {'0': foo_tab_arity0, '1': foo_tab_arity1},
    'upper': {'1': foo_upper},
    'meta': {'1': foo_meta_arity1, '2': foo_meta_arity2},
    'meta_sep': {'2': foo_meta_sep_arity2, '3': foo_meta_sep_arity3},
    'meta_test': {'n': foo_meta_test},
    'meta_num': {'1': foo_meta_num},
    'get': {'0': foo_false, '1': foo_get},
    'put': {'2': foo_put},
    'puts': {'2': foo_puts},
}


class FunctionVirtualInvocationException(Exception):
  pass


def vmarshal(value):
  if value is None:
    return None

  string_value = value
  truth_value = False

  try:
    string_value = value.string_value
    truth_value = value.truth_value
  except AttributeError:
    if value is True or value is False:
      string_value = ''
      truth_value = value

  return EvaluatorAtom(string_value, truth_value)

def vinvoke(track, function, argv, memory={}):
  arity = unistr(len(argv))
  funcref = None
  try:
    funcref = foo_function_vtable[function][arity]
  except KeyError:
    try:
      funcref = foo_function_vtable[function]['n']
    except KeyError:
      message = 'No function with name %s and arity %s exists' % (
          function, arity)
      raise FunctionVirtualInvocationException(message)
  return vmarshal(funcref(track, memory, argv))


class EvaluatorAtom:
  def __init__(self, string_value, truth_value):
    self.string_value = string_value
    self.truth_value = truth_value

  def __str__(self):
    return str(self.string_value)

  def __unicode__(self):
    return unistr(self.string_value)

  def __nonzero__(self):
    return self.truth_value

  def __bool__(self):
    return self.truth_value

  def __repr__(self):
    return 'atom(%s, %s)' % (repr(self.string_value), self.truth_value)

  def eval(self):
    # Evaluating an expression that's already been evaluated returns itself.
    return self


class LazyExpression:
  def __init__(self,
      formatter, track, expression, conditional, depth, offset, track_memory):
    self.formatter = formatter
    self.track = track
    self.current = expression
    self.conditional = conditional
    self.depth = depth
    self.offset = offset
    self.memory = track_memory
    self.value = None
    self.evaluated = False

  def eval(self):
    if not self.evaluated:
      self.value = self.formatter.eval(
          self.track, self.current, self.conditional, self.depth, self.offset,
          self.memory)
      self.evaluated = True
    return self.value

  def __str__(self):
    return self.current

  def __repr__(self):
    return "lazy(%s)" % repr(self.current)


class TitleFormatParseException(Exception):
  pass


class TitleFormatter:
  def __init__(
      self, case_sensitive=False, magic=True, for_filename=False, debug=False):
    self.case_sensitive = case_sensitive
    self.magic = magic
    self.for_filename = for_filename
    self.debug = debug

  def format(self, track, title_format):
    evaluated_value = self.eval(track, title_format)
    if evaluated_value is not None:
      return unistr(evaluated_value)
    return None

  def eval(self, track, title_format, conditional=False, depth=0, offset=0,
      memory={}):
    lookbehind = None
    outputting = True
    literal = False
    literal_count = None
    parsing_variable = False
    parsing_function = False
    parsing_function_args = False
    parsing_function_recursive = False
    parsing_conditional = False
    offset_start = 0
    fn_offset_start = 0
    bad_var_char = None
    conditional_parse_count = 0
    evaluation_count = 0
    recursive_lparen_count = 0
    recursive_rparen_count = 0
    output = ''
    current = ''
    current_fn = ''
    current_argv = []

    if self.debug:
      dbg('fresh call to eval(); format="%s" offset=%s' % (
        title_format, offset), depth)

    for i, c in enumerate(title_format):
      if outputting:
        if literal:
          next_output, literal, chars_parsed = self.parse_literal(
              c, i, lookbehind, literal_count, False, depth, offset + i)
          output += next_output
          literal_count += chars_parsed
        else:
          if c == "'":
            if self.debug:
              dbg('entering literal mode at char %s' % i, depth)
            literal = True
            literal_count = 0
          elif c == '%':
            if self.debug:
              dbg('begin parsing variable at char %s' % i, depth)
            if parsing_variable or parsing_function or parsing_conditional:
              raise TitleFormatParseException(
                  "Something went horribly wrong while parsing token '%'")
            outputting = False
            parsing_variable = True
          elif c == '$':
            if self.debug:
              dbg('begin parsing function at char %s' % i, depth)
            if parsing_variable or parsing_function or parsing_conditional:
              raise TitleFormatParseException(
                  "Something went horribly wrong while parsing token '$'")
            outputting = False
            parsing_function = True
            fn_offset_start = i + 1
          elif c == '[':
            if self.debug:
              dbg('begin parsing conditional at char %s' % i, depth)
            if parsing_variable or parsing_function or parsing_conditional:
              raise TitleFormatParseException(
                  "Something went horribly wrong while parsing token '['")
            outputting = False
            parsing_conditional = True
            offset_start = i + 1
          elif c == ']':
            message = self.make_backwards_error(']', '[', offset, i)
            raise TitleFormatParseException(message)
          else:
            output += c
      else:
        if parsing_variable:
          if literal:
            raise TitleFormatParseException(
                'Invalid parse state: Cannot parse names while in literal mode')
          if c == '%':
            evaluated_value = self.resolve_variable(track, current, i, depth)

            if self.debug:
              dbg('value is: %s' % evaluated_value, depth)
            evaluated_value_str = unistr(evaluated_value)
            if evaluated_value or evaluated_value == '':
              if evaluated_value is not True:
                output += evaluated_value_str
              evaluation_count += 1
            elif evaluated_value is not None and evaluated_value is not False:
              # This is the case where no evaluation happened but there is still
              # a string value (that won't output conditionally).
              output += evaluated_value_str
            else:
              output += '?'
            if self.debug:
              dbg('evaluation count is now %s' % evaluation_count, depth)

            current = ''
            outputting = True
            parsing_variable = False
          elif not self.is_valid_var_identifier(c):
            dbg('probably an invalid character: %s at char %i' % (c, i), depth)
            # Only record the first instance.
            if bad_var_char is None:
              bad_var_char = (c, offset + i)

            current += c
          else:
            current += c
        elif parsing_function:
          if literal:
            raise TitleFormatParseException(
                'Invalid parse state: Cannot parse names while in literal mode')
          if c == '(':
            if current == '':
              raise TitleFormatParseException(
                  "Can't call function with no name at char %s" % i)
            if self.debug:
              dbg('parsed function %s at char %s' % (current, i), depth)

            current_fn = current
            current = ''
            parsing_function = False
            parsing_function_args = True
            offset_start = i + 1
          elif c == ')':
            message = self.make_backwards_error(')', '(', offset, i)
            raise TitleFormatParseException(message)
          elif not (c == '_' or c.isalnum()):
            raise TitleFormatParseException(
                "Illegal token '%s' encountered at char %s" % (c, i))
          else:
            current += c
        elif parsing_function_args:
          if not parsing_function_recursive:
            if literal:
              next_current, literal, chars_parsed = self.parse_literal(
                  c, i, lookbehind, literal_count, True, depth, offset + i)
              current += next_current
              literal_count += chars_parsed
            else:
              if c == ')':
                if current != '' or len(current_argv) > 0:
                  current, arg = self.parse_fn_arg(track, current_fn, current,
                      current_argv, c, i, depth, offset + offset_start, memory)
                  current_argv.append(arg)

                if self.debug:
                  dbg('finished parsing function arglist at char %s' % i, depth)

                fn_result = self.invoke_function(
                    track, current_fn, current_argv,
                    depth, offset + fn_offset_start)

                if self.debug:
                  dbg('finished invoking function %s, value: %s' % (
                      current_fn, repr(fn_result)), depth)

                if fn_result is not None and fn_result is not False:
                  str_fn_result = unistr(fn_result)
                  if str_fn_result:
                    output += str_fn_result
                if fn_result:
                  evaluation_count += 1

                if self.debug:
                  dbg('evaluation count is now %s' % evaluation_count, depth)

                current_argv = []
                outputting = True
                parsing_function_args = False
              elif c == "'":
                if self.debug:
                  dbg('entering arglist literal mode at char %s' % i, depth)
                literal = True
                literal_count = 0
                # Include the quotes because we reparse function arguments.
                current += c
              elif c == ',':
                current, arg = self.parse_fn_arg(track, current_fn, current,
                    current_argv, c, i, depth, offset + offset_start, memory)
                current_argv.append(arg)
                offset_start = i + 1
              elif c == '$':
                if self.debug:
                  dbg('stopped evaluation for function in arg at char %s' % i,
                      depth)
                current += c
                parsing_function_recursive = True
                recursive_lparen_count = 0
                recursive_rparen_count = 0
              else:
                current += c
          else: # parsing_function_recursive
            current += c
            if c == '(':
              recursive_lparen_count += 1
            elif c == ')':
              recursive_rparen_count += 1
              if recursive_lparen_count == recursive_rparen_count:
                # Stop skipping evaluation.
                if self.debug:
                  dbg('resumed evaluation at char %s' % i, depth)
                parsing_function_recursive = False
              elif recursive_lparen_count < recursive_rparen_count:
                message = self.make_backwards_error(')', '(', offset, i)
                raise TitleFormatParseException(message)
        elif parsing_conditional:
          if literal:
            current += c
            if c == "'":
              if self.debug:
                dbg('leaving conditional literal mode at char %s' % i, depth)
              literal = False
          else:
            if c == '[':
              if self.debug:
                dbg('found a pending conditional at char %s' % i, depth)
              conditional_parse_count += 1
              if self.debug:
                dbg('conditional parse count now %s' % conditional_parse_count,
                    depth)
              current += c
            elif c == ']':
              if conditional_parse_count > 0:
                if self.debug:
                  dbg('found a terminating conditional at char %s' % i, depth)
                conditional_parse_count -= 1
                if self.debug:
                  dbg('conditional parse count now %s at char %s' % (
                    conditional_parse_count, i), depth)
                current += c
              else:
                if self.debug:
                  dbg('finished parsing conditional at char %s' % i, depth)
                evaluated_value = self.eval(
                    track, current, True, depth + 1, offset + offset_start,
                    memory)

                if self.debug:
                  dbg('value is: %s' % evaluated_value, depth)
                if evaluated_value:
                  output += unistr(evaluated_value)
                  evaluation_count += 1
                if self.debug:
                  dbg('evaluation count is now %s' % evaluation_count, depth)

                current = ''
                conditional_parse_count = 0
                outputting = True
                parsing_conditional = False
            elif c == "'":
              if self.debug:
                dbg('entering conditional literal mode at char %s' % i, depth)
              current += c
              literal = True
            else:
              current += c
        else:
          # Whatever is happening is invalid.
          raise TitleFormatParseException(
              "Invalid title format parse state: Can't handle character " + c)
      lookbehind = c

    # At this point, we have reached the end of the input.
    if outputting:
      if literal:
        message = self.make_unterminated_error('literal', "'", offset, i)
        raise TitleFormatParseException(message)
    else:
      message = None
      if parsing_variable:
        message = self.make_unterminated_error('variable', '%', offset, i)
        if bad_var_char is not None:
          message += " (probably caused by char '%s' in position %s)" % (
              bad_var_char[0], bad_var_char[1])
      elif parsing_function:
        message = self.make_unterminated_error('function', '(', offset, i)
      elif parsing_function_args:
        message = self.make_unterminated_error('function call', ')', offset, i)
      elif parsing_conditional:
        message = self.make_unterminated_error('conditional', ']', offset, i)
      else:
        message = "Invalid title format parse state: Unknown error"

      raise TitleFormatParseException(message)

    if conditional and evaluation_count == 0:
      if self.debug:
        dbg('about to return nothing for output: %s' % output, depth)
      return None

    if depth == 0 and self.for_filename:
      system = platform.system()
      if system == 'Windows' and re.match('^[A-Z]:', output, flags=re.I):
        disk_id = output[0:2]
        output = disk_id + re.sub('[\\\\/:|]', re.escape(os.sep), output[2:])
      else:
        output = re.sub('[\\\\/:|]', re.escape(os.sep), output)
      output = re.sub('[*]', 'x', output)
      output = re.sub('"', "''", output)
      output = re.sub('[?<>]', '_', output)

    result = EvaluatorAtom(output, False if evaluation_count == 0 else True)

    if self.debug:
      dbg('eval() is returning: ' + repr(result), depth)

    return result

  def is_valid_var_identifier(self, c):
    return c == ' ' or c == '@' or c == '_' or c == '-' or c.isalnum()

  def make_backwards_error(self, right, left_expected, offset, i):
    message = "Encountered '%s' with no matching '%s'" % (right, left_expected)
    message += " at position %s" % (offset + i)
    return message

  def make_unterminated_error(self, token, expected, offset, i):
    message = "Unterminated %s; " % token
    if offset == 0:
      message += "reached end of input, "
    message += "expected '%s'" % expected
    if offset != 0:
      message += " at position %s" % (offset + i + 1)

    return message

  def parse_literal(self, c, i, lookbehind, literal_count, include_quote,
      depth=0, offset=0):
    next_output = ''
    next_literal_state = True
    literal_chars_parsed = 0

    if c == "'":
      if lookbehind == "'" and literal_count == 0:
        if self.debug:
          dbg('output of single quote due to lookbehind at char %s' % i, depth)
        next_output += c
      elif include_quote:
        next_output += c
      if self.debug:
        dbg('leaving literal mode at char %s' % i, depth)
      next_literal_state = False
    else:
      next_output += c
      literal_chars_parsed += 1

    return (next_output, next_literal_state, literal_chars_parsed)

  def parse_fn_arg(self, track, current_fn, current, current_argv, c, i,
      depth=0, offset=0, memory={}):
    next_current = ''

    if self.debug:
      dbg('finished argument %s for function "%s" at char %s' % (
          len(current_argv), current_fn, i), depth)
    # The lazy expression will parse the current buffer if it's ever needed.
    lazy = LazyExpression(
        self, track, current, False, depth + 1, offset, memory)
    return (next_current, lazy)

  def resolve_variable(self, track, field, i, depth):
    if field == '':
      if self.debug:
        dbg('output of single percent at char %s' % i, depth)
      return EvaluatorAtom('%', False)

    local_field = field
    if not self.case_sensitive:
      local_field = field.upper()
    if self.debug:
      dbg('parsed variable %s at char %s' % (local_field, i), depth)

    resolved = None

    if not self.magic:
      resolved = track.get(local_field)
    else:
      resolved = self.magic_resolve_variable(track, local_field, depth)

    if resolved is None or resolved is False:
      return None

    if self.for_filename:
      resolved = re.sub('[\\\\/:|]', '-', resolved)

    return EvaluatorAtom(resolved, True)

  def magic_resolve_variable(self, track, field, depth):
    field_lower = field.lower()
    if self.debug:
      dbg('checking %s for magic mappings' % field_lower, depth)
    if field_lower in magic_mappings:
      mapping = magic_mappings[field_lower]
      if not mapping:
        dbg('mapping "%s" is not valid' % field_lower, depth)
        return track.get(field)
      else:
        # First try to call it -- the mapping can be a function.
        try:
          magically_resolved = mapping(self, track)
          if self.debug:
            dbg('mapped %s via function mapping' % field_lower, depth)
          return magically_resolved
        except TypeError:
          # That didn't work. It's a list.
          if self.debug:
            dbg('mapping "%s" is not a function' % field_lower, depth)
          for each in mapping:
            if self.debug:
              dbg('attempting to map "%s"' % each, depth)
            if each in track:
              return track.get(each)
            if self.case_sensitive:
              each_lower = each.lower()
              if self.debug:
                dbg('attempting to map "%s"' % each_lower, depth)
              if each_lower in track:
                return track.get(each_lower)

          # Still couldn't find it.
          if self.debug:
            dbg('mapping %s failed to map magic variable' % field_lower, depth)
          return track.get(field)

    if self.debug:
      dbg('mapping %s not found in magic variables' % field_lower, depth)
    return track.get(field)

  def invoke_function(
      self, track, function_name, function_argv, depth=0, offset=0, memory={}):
    if self.debug:
      dbg('invoking function %s, args %s' % (
          function_name, function_argv), depth)
    return vinvoke(track, function_name, function_argv, memory)

