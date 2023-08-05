import mxdevtool.shock as mx_s
import inspect


class Output:
    def __init__(self, name, shock_scen_args):
        self.name = name
        self.shock_scen_args = shock_scen_args
        
        # self.func = func

    def func(self, shocked_scen_data_d: dict(), calc_kwargs, npv_func):
        return 0.0


class Npv(Output):
    def __init__(self, scen: str, currency=None):
        super().__init__(Npv.__name__.lower(), [scen])
        self.scen = scen

    def func(self, shocked_scen_data_d: dict(), calc_kwargs, npv_func):
        v = npv_func(shocked_scen_data_d[self.scen], calc_kwargs)
        return v


class CashFlow(Output):
    def __init__(self, scen: str, currency=None, discount=None):
        super().__init__(CashFlow.__name__.lower(), [scen])

        self.scen = scen

    def func(self, shocked_scen_data_d: dict(), calc_kwargs, cf_func):
        cf = cf_func(shocked_scen_data_d[self.scen], calc_kwargs)
        return cf


class Delta(Output):
    def __init__(self, up: str=None, down: str=None, h=1.0):
        """ 
        center method : ( s_up - s_down ) / (2h)

        Args:
            up (str, optional): shock name for up. Defaults to None.
            down (str, optional): shock name for down. Defaults to None.
            h (float, optional): interval. Defaults to 1.0.

        Raises:
            Exception: [description]
        """        
        super().__init__(Delta.__name__.lower(), [up, down])

        if up is None and down is None:
            raise Exception('up or down is required')

        self.up = up
        self.down = down
        self.h = h


    def func(self, shocked_scen_data_d: dict(), calc_kwargs, npv_func):
        #if self.up is None: -> ?
        #if self.down is None: -> ?

        upshock_scen = shocked_scen_data_d[self.up]
        downshock_scen = shocked_scen_data_d[self.down]

        v = npv_func(upshock_scen, calc_kwargs) - npv_func(downshock_scen, calc_kwargs)
        v = v / ( 2 * self.h )

        return v


class Gamma(Output):
    def __init__(self, up, center, down, h=1.0):
        super().__init__(Gamma.__name__.lower(), [up, center, down])

        if up is None and down is None:
            raise Exception('up or down is required')

        self.up = up
        self.down = down


class UserFunc(Output):
    def __init__(self, scen, userfunc, **kwargs):
        super().__init__(UserFunc.__name__.lower(), [scen])

        self.scen = scen
        self.userfunc = userfunc

        # check func signature
        args = inspect.signature(userfunc).parameters
        if not all(k in args for k in ['scen_data_d', 'calc_kwargs'] ):
            raise Exception('signature is not match')

    def func(self, shocked_scen_data_d: dict(), calc_kwargs, cf_func):
        return self.userfunc(self.scen, calc_kwargs)

        
