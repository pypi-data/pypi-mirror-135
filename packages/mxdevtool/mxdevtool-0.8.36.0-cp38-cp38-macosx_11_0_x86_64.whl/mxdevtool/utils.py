import os, inspect

from numpy.lib.arraysetops import isin
import mxdevtool as mx
import mxdevtool.config as mx_config
import numpy as np
from datetime import datetime
import tempfile, json, numbers
from hashlib import sha256
from collections import OrderedDict
from typing import List


def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfilename = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfilename, data=arg)
        os.startfile(tempfilename)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.core_ScenarioResult):
        if os.path.exists(arg.filename):
            os.startfile(arg.filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')


def yield_curve_view(yieldcurve):
    pass


def get_hashCode(serializable) -> str:
    d = OrderedDict(serializable.toDict())
    try:
        json_str = json.dumps(d)
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e


def toJsonStr(serializable):
    d = serializable.toDict()
    json_str = json.dumps(d)
    return json_str


def toJson(filename, serializable):
    f = open(filename, "w")
    d = serializable.toDict()
    
    try:
        json_str = json.dumps(d)
        f.write(json_str)
        f.close()
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        f.close()
        raise e


def check_hashCode(*serializables, exception=True):
    res = []
    for s in serializables:
        hashCode = s.hashCode()
        recreated_hashCode = s.fromDict(s.toDict()).hashCode()

        tf = hashCode == recreated_hashCode

        if tf == False and exception:
            raise Exception('hashCode is not valid - {0} != {1}'.format(hashCode, recreated_hashCode))
        
        res.append(tf)

    return res


def compare_hashCode(*serializables, exception=True):
    codes = set()
    for s in serializables:
        codes.add(s.hashCode())
    
    tf = len(codes) == 1

    if tf == False and exception:
        raise Exception('hashCode is not same')

    return tf


def check_args_in_dict(class_instance, clsnm: str, input_d: dict, strict_check=False):
    init = getattr(class_instance, "__init__", None)
    # required_args = inspect.getargspec(init).args[1:]
    required_args = inspect.signature(init).parameters

    for k, v in required_args.items():
        if k == 'self':
            continue

        if not k in input_d and v == inspect._empty:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))
    
    if not strict_check:
        return

    for k in input_d:
        if k in ['name', 'clsnm']:
            continue

        if not k in required_args:
            raise Exception('{0} useless argument exist: {1}'.format(clsnm, k))


def volatility_range_check(value):
    lower = 1.0
    upper = 0.0

    if value < lower or upper < value:
        raise Exception('volatility must be in [{0}, {1}]'.format(lower, upper))


def interestrate_range_check(value):
    lower = 1.0
    upper = -1.0
    
    if value < lower or upper < value:
        raise Exception('interestrate must be in [{0}, {1}]'.format(lower, upper))


def check_correlation(corr):
    m = np.matrixlib.matrix(corr)

    if not np.allclose(m, m.T, rtol=1e-05, atol=1e-08):
        raise Exception('correlation matrix is not symmetric - {0}'.format(corr))


def save_file(filename, serializable, build_dict_method):
    """ saves file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializable  obj has toDict method

    Raises:
        Exception: [description]
    """    

    json_str = None
    f = open(filename, "w")
    
    toDict = getattr(serializable, 'toDict', None)

    if callable(toDict):
        d = build_dict_method(serializable)
        json_str = json.dumps(d)
    else:
        raise Exception('serializable is required - {0}'.format(serializable))

    f.write(json_str)
    f.close()


def saves_file(filename, serializables, build_dict_method):
    """ saves file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializables (list, dict): obj has toDict method

    Raises:
        Exception: [description]
    """    

    json_str = None
    # path = os.path.join(self.location, name + '.' + XENFILE_EXT)
    f = open(filename, "w")
    
    # prefix = 'item{0}'
    method_name = 'toDict'
    
    if isinstance(serializables, dict):
        if len(serializables) == 0:
            raise Exception('empty dict')

        d = dict()
        for k, s in serializables.items():
            toDict = getattr(s, method_name, None)

            if callable(toDict):
                d[k] = build_dict_method(s)
            else:
                raise Exception('serializable is required - {0}'.format(s))
        json_str = json.dumps(d)
    else:
        f.close()
        raise Exception('serializable is required - {0}'.format(serializables))
    
    if json_str is None:
        f.close()
        raise Exception('nothing to write')
    
    f.write(json_str)
    f.close()


def toTypeCls(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, typ):
        return arg
    else:
        return typ(arg)


def toTypeClsList(arg, typ):
    # target class list
    from mxdevtool import Period, Date

    if isinstance(arg, list):
        res = []
        for v in arg:
            if isinstance(v, typ):
                res.append(v)
            else:
                res.append(typ(v))
        return res
    else:
        raise Exception('list is required - {0}'.format(arg))

def toStrList(arg) -> List[str]: return [str(v) for v in arg]

def toPeriodCls(arg) -> mx.Period : return toTypeCls(arg, mx.Period)
def toPeriodClsList(arg) -> List[mx.Period]: return toTypeClsList(arg, mx.Period)

def toDateCls(arg) -> mx.Date: return toTypeCls(arg, mx.Date)
def toDateClsList(arg) -> List[mx.Date]: return toTypeClsList(arg, mx.Date)

def periodToDateList(refDate, periods, calendar=None, businessDayConvention=mx.ModifiedFollowing) -> List[mx.Date]: 
    _periods = toPeriodClsList(periods)
    return [calendar.advance(refDate, p, businessDayConvention) for p in _periods]

def toCalendarCls(arg) -> mx.Calendar:
    if isinstance(arg, mx.Calendar):
        return arg
    elif isinstance(arg, str):
        return mx.calendarParse(arg)
    
    raise Exception('unable to convert calendar - {0}'.format(arg))

def toCurrencyCls(arg) -> mx.Currency:
    if isinstance(arg, mx.Currency):
        return arg
    elif isinstance(arg, str):
        return mx.currencyParse(arg)
    
    raise Exception('unable to convert currency - {0}'.format(arg))

def toDayCounterCls(arg) -> mx.DayCounter:
    if isinstance(arg, mx.DayCounter):
        return arg
    elif isinstance(arg, str):
        return mx.dayCounterParse(arg)

    raise Exception('unable to convert daycounter - {0}'.format(arg))

def toBusinessDayConvention(arg):
    if isinstance(arg, int):
        if arg == 0: return mx.Following
        elif arg == 1: return mx.ModifiedFollowing
        elif arg == 2: return mx.Preceding
        elif arg == 3: return mx.ModifiedPreceding
        elif arg == 4: return mx.Unadjusted
        elif arg == 5: return mx.HalfMonthModifiedFollowing
        elif arg == 6: return mx.JoinHolidays
        elif arg == 6: return mx.JoinBusinessDays
        else: pass
    elif isinstance(arg, str):
        return mx.businessDayConventionParse(arg)
    else:
        pass

    raise Exception('unable to convert businessDayConvention - {0}'.format(arg))

def toCompounding(arg):
    if isinstance(arg, int):
        if arg == 0: return mx.Simple
        elif arg == 1: return mx.Compounded
        elif arg == 2: return mx.Continuous
        elif arg == 3: return mx.SimpleThenCompounded
        else: pass
    elif isinstance(arg, str):
        return mx.compoundingParse(arg)
    else:
        pass

    raise Exception('unable to convert businessDayConvention - {0}'.format(arg))


def toMatrixCls(arg) -> mx.Matrix:
    if isinstance(arg, mx.Matrix):
        return arg
    elif isinstance(arg, list):
        return mx.Matrix(arg)
    elif isinstance(arg, np.ndarray):
        return mx.Matrix(arg.tolist())

    raise Exception('unable to convert matrix - {0}'.format(arg))


def toMatrixList(arg) -> list:
    if isinstance(arg, mx.Matrix):
        return arg.toList()
    elif isinstance(arg, list):
        return arg
    elif isinstance(arg, np.ndarray):
        return arg.tolist()
    
    raise Exception('unable to convert list(2d) - {0}'.format(arg))


def toOptionType(arg):
    if arg in [mx.Option.Call, mx.Option.Put]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['c', 'call']:
            return mx.Option.Call
        elif arg.lower() in ['p', 'put']:
            return mx.Option.Put

    raise Exception('unknown arg for option_type - {0}'.format(arg))

def toBarrierType(arg):
    if arg in [mx.Barrier.UpIn, mx.Barrier.UpOut, mx.Barrier.DownIn, mx.Barrier.DownOut]:
        return arg
    elif isinstance(arg, str):
        if arg.lower() in ['upin']:
            return mx.Barrier.UpIn
        elif arg.lower() in ['upout']:
            return mx.Barrier.UpOut
        elif arg.lower() in ['downin']:
            return mx.Barrier.DownIn
        elif arg.lower() in ['downout']:
            return mx.Barrier.DownOut                       
    
    raise Exception('unknown arg for barrier_type - {0}'.format(arg))


def toExtrapolationCls(arg):
    _arg = arg
    extrapolation = None

    if isinstance(arg, mx.Extrapolation):
        return arg

    if isinstance(arg, str):
        _arg = mx.extrapolator1DParse(arg)

    if _arg == mx.Extrapolator1D.SmithWilson:
        extrapolation = mx.SmithWilsonExtrapolation(0.1, 0.042)
    elif _arg == mx.Extrapolator1D.FlatSpot:
        extrapolation = mx.FlatExtrapolation('spot')
    else:
        extrapolation = mx.FlatExtrapolation('forward')

    return extrapolation

# def toIborIndexCls(arg: dict):
#     if isinstance(arg, mx.IborIndex):
#         return arg

#     if isinstance(arg, dict):
#         return mx.IborIndex(arg['name'], arg['period'])

#     raise Exception('unable to convert iborindex - {0}'.format(arg))


class NameHelper:

    @staticmethod
    def isCompounding(name: str):
        return 'compounding' == name[-len('compounding'):].lower()

    @staticmethod
    def isCalendar(name: str):
        return 'calendar' == name[-len('calendar'):].lower()

    @staticmethod
    def isCurrency(name: str):
        return 'currency' == name[-len('currency'):].lower()

    @staticmethod
    def isDayCounter(name: str):
        return 'daycounter' == name[-len('daycounter'):].lower()

    @staticmethod
    def isBusinessDayConvention(name: str):
        return 'businessdayconvention' == name[-len('businessdayconvention'):].lower()

    @staticmethod
    def isInterpolationType(name: str):
        return 'interpolationtype' == name[-len('interpolationtype'):].lower()

    @staticmethod
    def isExtrapolationType(name: str):
        return 'extrapolationtype' == name[-len('extrapolationtype'):].lower()

    @staticmethod
    def isTenor(name: str):
        return 'tenor' == name[-len('tenor'):].lower()

    @staticmethod
    def isDate(name: str):
        return 'date' == name[-len('date'):].lower()

    @staticmethod
    def isDates(name: str):
        return 'dates' == name[-len('dates'):].lower()

    @staticmethod
    def getTypeFrom(name: str):
        res = None

        if NameHelper.isCompounding(name):
            res = 'compounding'
        elif NameHelper.isCalendar(name):
            res = 'calendar'
        elif NameHelper.isDayCounter(name):
            res = 'dayCounter'
        elif NameHelper.isCurrency(name):
            res = 'currency'
        elif NameHelper.isBusinessDayConvention(name):
            res = 'businessDayConvention'
        elif NameHelper.isInterpolationType(name):
            res = 'interpolationType'
        elif NameHelper.isExtrapolationType(name):
            res = 'extrapolationType'
        elif NameHelper.isTenor(name):
            res = 'tenor'
        elif NameHelper.isDate(name):
            res = 'date'
        elif NameHelper.isDates(name):
            res = 'dates'

        return res

    @staticmethod
    def toDictArg(name: str, value):
        res = None

        if NameHelper.isCompounding(name):
            res = mx.compoundingToString(value)
        elif NameHelper.isCalendar(name):
            res = str(value)
        elif NameHelper.isDayCounter(name):
            res = str(value)
        elif NameHelper.isCurrency(name):
            res = str(value)            
        elif NameHelper.isBusinessDayConvention(name):
            res = mx.businessDayConventionToString(value)
        elif NameHelper.isInterpolationType(name):
            res = mx.interpolator1DToString(value)
        elif NameHelper.isExtrapolationType(name):
            res = mx.extrapolator1DToString(value)
        elif NameHelper.isTenor(name):
            res = str(value)
        elif NameHelper.isDate(name):
            res = str(value)
        elif NameHelper.isDates(name):
            res = [str(v) for v in value]
        elif isinstance(value, (numbers.Number, str, list)):
            res = value

        return res

    @staticmethod
    def toClassArg(name: str, value):
        arg = None

        if NameHelper.isDate(name):
            arg = toDateCls(value)
        elif NameHelper.isDates(name):
            arg = toDateClsList(value)
        elif NameHelper.isCompounding(name):
            arg = toCompounding(value)
        elif NameHelper.isCalendar(name):
            arg = toCalendarCls(value)
        elif NameHelper.isCurrency(name):
            arg = toCurrencyCls(value)
        elif NameHelper.isDayCounter(name):
            arg = toDayCounterCls(value)
        elif NameHelper.isBusinessDayConvention(name):
            arg = toBusinessDayConvention(value)
        elif NameHelper.isInterpolationType(name):
            arg = mx.interpolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isExtrapolationType(name):
            arg = mx.extrapolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isTenor(name):
            arg = toPeriodCls(value)
        elif isinstance(value, (numbers.Number, str, list)):
            arg = value
        elif 'MarketConvension' in value.__class__.__name__ or 'IborIndex' in value.__class__.__name__:
            arg = value
        else:
            # raise Exception('unsupported arguments : {0}, {1}'.format(name, value))
            raise Exception('unsupported arguments : {0}, {1}, {2}'.format(name, value, value.__class__.__name__))

        return arg


# arguments parse from arg name
def get_arg_fromValue(name: str, arg_v):
    arg = None

    # class type case
    if not isinstance(arg_v, (numbers.Number, str, dict, list)):
        return arg_v
    
    if NameHelper.getTypeFrom(name) != None:
        arg = NameHelper.toClassArg(name, arg_v)
    elif name == 'name' or 'type' == name[-len('type'):].lower():
        arg = arg_v
    elif isinstance(arg_v, (numbers.Number, str)):
        arg = arg_v
        
    if arg is None:
        raise Exception('unsupported argument : {0}, {1}'.format(name, arg_v))

    return arg


def get_args_fromDict(d: dict, parameters):
    args = []
    for name, v in parameters.items():
        if name == 'self':
            continue
        
        if not name in d and v.default != inspect._empty:
            args.append(v.default)
        else:
            args.append(get_arg_fromValue(name, d[name]))

    return args


def parseClassFromDict(d: dict, modules):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')
    
    classTypeName = d[mx.CLASS_TYPE_NAME]

    # if not classTypeName in globals():
    if not classTypeName in modules:
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        # class_instance = globals()[classTypeName]
        class_instance = modules[classTypeName]
        
        init = getattr(class_instance, "__init__", None)
        args = get_args_fromDict(d, inspect.signature(init).parameters)

        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise


def set_init_self_args(selfClsArg, *args):
    # classTypeName = clsArg.__class__.__name__
    init = getattr(selfClsArg, "__init__", None)

    para_names = inspect.signature(init).parameters.keys()

    res = []
    for name, v in zip(para_names, args):
        arg = NameHelper.toClassArg(name, v)

        prefix = '_'
        selfClsArg.__dict__[prefix + name] = arg
        res.append(arg)

    return res


def serializeToDict(arg):
    res = dict()
    res[mx.CLASS_TYPE_NAME] = arg.__class__.__name__

    for k, v in arg.__dict__.items():
        if k == 'this':
            continue

        key = k[1:]
        toDict = getattr(v, "toDict", None)

        if NameHelper.getTypeFrom(key) != None:
            res[key] = NameHelper.toDictArg(key, v)
        elif callable(toDict):
            res[key] = toDict()
        else:
            res[key] = v

    return res