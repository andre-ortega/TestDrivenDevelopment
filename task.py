import math


def conv_num(num_str):
    # check for empty input, spaces, or incorrect arg type
    if not num_str or type(num_str) != str or ' ' in num_str:
        return

    # check if negative and drop negative sign if its there
    negative = True if num_str[0] == '-' else False
    if negative:
        num_str = num_str[1:]
    """ set up char value map, scared to use ord()/other
    builtins for char->val transl."""
    char_value_map = {}
    value = 0
    for char in '0123456789ABCDEF':
        char_value_map[char] = value
        value += 1

    # hex branch
    if len(num_str) >= 2 and num_str[0] == '0' and num_str[1] == 'x':
        # shouldn't have just hex prefix or . in hex num_str
        if num_str == '0x' or '.' in num_str:
            return

        # get rid of hex prefix
        num_str = num_str[2:]

        total = calc_hex_num(num_str, char_value_map)

    # float branch
    elif '.' in num_str:
        # can only have one fp
        if len([c for c in num_str if c == '.']) != 1:
            return

        total = calc_float_num(num_str, char_value_map)

    # int branch
    else:
        total = calc_int_num(num_str, char_value_map)

    return -total if negative and total else total


def calc_hex_num(num_str, char_value_map):
    # shouldn't have anything in hex num_str that isn't in 'ABCDEF0123456789'
    valid_hex_chars = 'ABCDEF0123456789'
    total = 0
    multiplier = 1

    for char in num_str[::-1]:
        if char not in valid_hex_chars:
            total = None
            break
        total += (char_value_map[char] * multiplier)
        multiplier *= 16

    return total


def calc_float_num(num_str, char_value_map):
    # assign total to float-zero to avoid using float()
    valid_float_chars = '.0123456789'
    period_index = num_str.index('.')
    i, j = period_index - 1, period_index + 1
    total = 0.0
    multiplier = 1

    # move right from fp then left from fp to compute a float from a float-str
    valid = True
    while i > -1:
        if num_str[i] not in valid_float_chars:
            valid = False
            total = None
            break
        total += (char_value_map[num_str[i]] * multiplier)
        multiplier *= 10
        i -= 1
    divisor = 10
    while valid and j < len(num_str):
        if num_str[j] not in valid_float_chars:
            total = None
            break
        total += (char_value_map[num_str[j]] / divisor)
        divisor *= 10
        j += 1

    return total


def calc_int_num(num_str, char_value_map):
    total = 0
    multiplier = 1
    valid_int_chars = '0123456789'
    for char in num_str[::-1]:
        if char not in valid_int_chars:
            return
        total += (char_value_map[char] * multiplier)
        multiplier *= 10

    return total


def conv_endian(num, endian='big'):

    # First validate input by checking invalid 'endian' overwrite
    if endian != 'big' and endian != 'little':
        return None

    # Easier to just preserve the negative property until string concatenation
    negative = False
    if num < 0:
        negative = True

    # Now we can just work with the positive number for peace of mind
    num = abs(num)

    # Let's get the raw hex string from num
    hexString = getRawHex(num)

    # Adding a trailing zero if there is an odd number of chars in hexString
    if len(hexString) % 2 != 0:
        hexString += '0'

    # Now we can finish up with some string operations depending on little/big
    if endian == 'big':

        # For big-endian we'll first reverse the string using python slice
        hexString = hexString[::-1]

        # For padding with spaces I found this function from stackoverflow
        #   (cited work #1)
        hexString = ' '.join(hexString[i:i+2]
                             for i in range(0, len(hexString), 2))

        # Did we start with a negative number? If yes make negative
        if negative is True:
            hexString = '-' + hexString

        # Found an edge-case in testing for when num == 0
        if hexString == '':
            hexString = '00'

        # .. and that's it, return the string
        return hexString

    # Little-endian
    else:

        # Need to swap characters, convert to list first
        hexStringList = list(hexString)

        # Swap every other character with the preceding char
        for x in range(len(hexStringList)//2):
            tmp = hexStringList[x*2]
            hexStringList[x*2] = hexStringList[x*2 + 1]
            hexStringList[x*2 + 1] = tmp

        # Convert back to string
        hexString = "".join(hexStringList)

        # Use the same function as above for padding spaces
        hexString = ' '.join(hexString[i:i+2]
                             for i in range(0, len(hexString), 2))

        # Convert to negative if needed
        if negative is True:
            hexString = '-' + hexString

        # Edge-case handling for zeroed bytes
        if hexString == '':
            hexString = '00'

        # Dunzo
        return hexString


# Takes an int, returns the same value in unformatted hex string
def getRawHex(num):

    hexString = ''
    # Iterate until nothing remains
    while num > 0:

        rem = num % 16
        num = num // 16

        # Convert each remainder to hex and add to string
        if rem < 10:
            hexString += str(rem)
        elif rem == 10:
            hexString += 'A'
        elif rem == 11:
            hexString += 'B'
        elif rem == 12:
            hexString += 'C'
        elif rem == 13:
            hexString += 'D'
        elif rem == 14:
            hexString += 'E'
        elif rem == 15:
            hexString += 'F'

    return hexString


"""
        Cited Work
1:
        https://stackoverflow.com/questions/3258573/
          pythonic-way-to-insert-every-2-elements-in-a-string
"""


# Return Boolean For Current Year Being A Leap Year or Not
def is_leap_year(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


# Keep Track of Total Days in a Month
def dates_in_month(year, month):
    total_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d = total_days[month]
    if(is_leap_year(year) and month == 2):
        return d+1
    else:
        return d


# String Format for Date
def format_str(m, d, y):
    if(m < 10):
        m = "0" + str(m)
    if(d < 10):
        d = "0" + str(d)
    m = str(m)
    d = str(d)
    y = str(y)
    return m + "-" + d + "-" + y


def my_datetime(num_sec):
    total_days = math.floor(num_sec / (24 * 60 * 60))
    # Counter from EPOCH
    month_counter = 1
    date_counter = 1
    year_counter = 1970

    # While Total Days is less than Zero
    counter = total_days
    for i in range(total_days):
        counter -= 1
        date_counter += 1
        if date_counter > dates_in_month(year_counter, month_counter):
            date_counter = 1
            month_counter += 1
        if month_counter > 12:
            month_counter = 1
            year_counter += 1
    return format_str(month_counter, date_counter, year_counter)


""" Cited Work
    https://stackoverflow.com/questions/15797597/problems-with-my-unix-epoch-time-converter
    https://stackoverflow.com/questions/7136385/calculate-day-number-from-an-unix-timestamp-in-a-math-way
    https://howardhinnant.github.io/date_algorithms.html#days_from_civil

"""
