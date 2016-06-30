def isolate_origin_from_trip_name(str):
    """
    Isolates origin station name from trip name.

    Example:
    '8:10 pm from Ashmont - Inbound to Alewife' returns 'Ashmont'

    :param str: Trip name as a string
    :return: Origin station name
    """
    return str[str.index('from')+4:str.index('to')].strip().split('-')[0].strip()
