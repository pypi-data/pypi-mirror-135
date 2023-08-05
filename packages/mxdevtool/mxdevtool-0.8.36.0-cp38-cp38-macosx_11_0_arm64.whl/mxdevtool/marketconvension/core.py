import mxdevtool as mx
import mxdevtool.utils as utils


class IborIndex(mx.core_IborIndex):
    def __init__(self, familyName, tenor, settlementDays,
                 currency, calendar, convention,
                 endOfMonth, dayCounter):

        args = utils.set_init_self_args(self, familyName, tenor, settlementDays,
                 currency, calendar, convention, endOfMonth, dayCounter)

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


class FixedBondMarketConvension(mx.core_FixedBondMarketConvension):
    def __init__(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, compounding, familyname):

        args = utils.set_init_self_args(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, compounding, familyname)

        # this for intellisense
        self.calendar: mx.Calendar = self._calendar
        self.dayCounter: mx.DayCounter = self._dayCounter
        self.businessDayConvention: int = self._businessDayConvention
        self.settlementDays: int = self._settlementDays
        self.couponTenor: mx.Period = self._couponTenor
        self.compounding: int = self._compounding
        self.familyname: str = self._familyname

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


class VanillaSwapMarketConvension(mx.core_VanillaSwapMarketConvension):
    def __init__(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, iborIndex, familyname):

        args = utils.set_init_self_args(self, calendar, dayCounter, businessDayConvention,
                 settlementDays, couponTenor, iborIndex, familyname)

        # this for intellisense
        self.calendar: mx.Calendar = self._calendar
        self.dayCounter: mx.DayCounter = self._dayCounter
        self.businessDayConvention: int = self._businessDayConvention
        self.settlementDays: int = self._settlementDays
        self.couponTenor: mx.Period = self._couponTenor
        self.iborIndex: IborIndex = self._iborIndex
        self.familyname: str = self._familyname

        super().__init__(*args)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


def get_iborIndex(name: str, tenor: mx.Period) -> IborIndex:
    if name == 'krwcd':
        return IborIndex("KrwCD", tenor, 1, utils.toCurrencyCls('krw'), utils.toCalendarCls('kr'), mx.ModifiedFollowing, True, mx.Actual365Fixed())
    else:
        pass

    raise Exception('unknown iborIndex - {0}'.format(name))


def marketConvensionFromDict(d: dict):
    if not isinstance(d, dict):
        raise Exception('dictionary is required - {0}'.format(d))

    clsnm = d[mx.CLASS_TYPE_NAME]
    if clsnm == FixedBondMarketConvension.__name__:
        return FixedBondMarketConvension.fromDict(d)
    elif clsnm == VanillaSwapMarketConvension.__name__:
        return VanillaSwapMarketConvension.fromDict(d)

    raise Exception('unknown marketConvension - {0}'.format(clsnm))


def get_marketConvension_fixedbond(name) -> FixedBondMarketConvension:
    if name == 'ktb1':
        return FixedBondMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('3m'), mx.Compounded, name)
    elif name == 'ktb2':
        return FixedBondMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('6m'), mx.Compounded, name)

    return None


def get_marketConvension_vanillaswap(name) -> VanillaSwapMarketConvension:
    if name in ('irskrw', 'irskrw_krccp'):
        iborIndex = get_iborIndex('krwcd', '3m')
        return VanillaSwapMarketConvension(
            mx.SouthKorea(), mx.Actual365Fixed(), mx.ModifiedFollowing, 1, mx.Period('3m'), iborIndex, name)

    return None


def get_marketConvension(name):
    fb = get_marketConvension_fixedbond(name)
    if fb != None: return fb

    vs = get_marketConvension_vanillaswap(name)
    if vs != None: return vs

    raise Exception('unknown marketConvension - {0}'.format(name))