import mxdevtool as mx
import mxdevtool.termstructures as ts
import mxdevtool.marketconvension as mc
import mxdevtool.utils as utils

from .pricing import *

import numpy as np


class VanillaSwap(mx.core_VanillaSwapExt, ScenPricing):
    def __init__(self, side, notional, settlementDate, maturityTenor, 
                 fixedRate, spread, marketConvension):

        args = utils.set_init_self_args(self, side, notional, settlementDate, maturityTenor, 
                 fixedRate, spread, marketConvension)
        
        super().__init__(*args)

    # def cashflows(self):
    #    pass

    def setPricingParams_YieldCurve(self, yieldCurve):
        self._setPricingParams_YieldCurve(yieldCurve)
        return self


class VanillaSwapCCP(mx.core_VanillaSwapCCPExt, ScenPricing):
    def __init__(self, side, notional, settlementDate, maturityTenor, 
                 fixedRate, iborIndex, spread, family_name):

        args = utils.set_init_self_args(self, side, notional, settlementDate, maturityTenor, 
                 fixedRate, iborIndex, spread, family_name)

        super().__init__(*args)

    def setPricingParams_YieldCurve(self, yieldCurve):
        self._setPricingParams_YieldCurve(yieldCurve)
        return self


class Swaption(mx.core_Swaption):
    def __init__(self, swap, exerciseDate, engine):
        mx.core_Swaption.__init__(self, swap, exerciseDate)
        self.setPricingEngine(engine)
        self.swap = swap
        self.exerciseDate = exerciseDate


def makeSwap(side=mx.VanillaSwap.Receiver, notional=10000, 
             maturityTenor=mx.Period(3, mx.Years),
             fixedRate=0.01, spread=0.0, settlementDate=None,
             yieldCurve=None, family_name='krwirs'):

    if not isinstance(yieldCurve, mx.YieldTermStructure):
        raise Exception('yieldCurve is required')

    mc_vanillaswap = mc.get_marketConvension_vanillaswap(family_name)

    calendar = mc_vanillaswap._calendar
    bdc = mc_vanillaswap._businessDayConvention

    if settlementDate is None:
        date = mx.Date.todaysDate()
        settlementDate = calendar.advance(date, '1d', bdc)
    
    swap = VanillaSwap(side, notional, settlementDate, maturityTenor, fixedRate, spread, mc_vanillaswap)
    swap.setPricingParams_YieldCurve(yieldCurve)
    # print('swap npv : ', swap.NPV())

    return swap


def makeSwaption(side=mx.VanillaSwap.Receiver, notional=10000, expiryTenor=mx.Period(1, mx.Years), 
                 maturityTenor=mx.Period(3, mx.Years), strike=None, settlementDate=None, yieldCurve=None, vol=0.3, family_name='irskrw_krccp'):
    
    mc_vanillaswap = mc.get_marketConvension_vanillaswap(family_name)
    calendar = mc_vanillaswap._calendar
    bdc = mc_vanillaswap._businessDayConvention

    if settlementDate is None:
        date = mx.Date.todaysDate()
        expiryDate = calendar.advance(date, expiryTenor, bdc)
    else:
        expiryDate = calendar.advance(settlementDate, expiryTenor, bdc)
    
    if strike is None:
        temp_swap = makeSwap(side, notional, maturityTenor, 0.0, 0.0, expiryDate, yieldCurve, family_name)
        fixedRate = temp_swap.fairRate()

    swap = makeSwap(side, notional, maturityTenor, fixedRate, 0.0, expiryDate, yieldCurve, family_name)
    engine = mx.core_BlackSwaptionEngine(yieldCurve, vol)

    return Swaption(swap, expiryDate, engine)


if __name__ == "__main__":
    
    ref_date = mx.Date_todaysDate()

    curve = ts.FlatForward(ref_date, 0.03)

    side = mx.VanillaSwap.Receiver
    notional = 10000
    settlementDate = ref_date + 1
    maturityTenor = '10y' 
    fixedRate = 0.02
    spread = 0.0
    marketConvension = mc.get_marketConvension('irskrw')

    swap = VanillaSwap(side, notional, settlementDate, maturityTenor, 
                 fixedRate, spread, marketConvension).setPricingParams_YieldCurve(curve)
    