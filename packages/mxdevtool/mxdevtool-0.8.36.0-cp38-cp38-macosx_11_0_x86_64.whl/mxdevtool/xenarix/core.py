import os, json, numbers

from numpy.lib.arraysetops import isin
import mxdevtool as mx
import mxdevtool.utils as utils
import numpy as np
#import mxdevtool.termstructures as ts
from mxdevtool.termstructures import *
from mxdevtool.xenarix.pathcalc import *
from mxdevtool.data.repositories.settings import get_repo
from mxdevtool import TimeGrid, TimeEqualGrid, TimeArrayGrid
from typing import List

XENFILE_EXT = 'xen'
XENFILE_SET_EXT = 'xens'
XENBUILDERFILE_EXT = 'xnb'
XENBUILDERFILE_SET_EXT = 'xnbs'
HASHCODES_KEY = 'hashcodes'
XENREPO_RESULTS_DIR = 'results'


# arguments parse from arg name
def get_arg_fromValue(name: str, arg_v, mrk: mx.MarketData, models_calcs):
    arg = None

    # class type case
    if not isinstance(arg_v, (numbers.Number, str, dict, list)):
        return arg_v

    if 'Curve' == name[-len('Curve'):]:
        curve_d = mrk.get_yieldCurve_d(arg_v)
        curveType = curve_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[curveType]
        arg = class_instance.fromDict(curve_d, mrk)

    elif 'volTs' == name or 'VolTs' == name[-len('VolTs'):]:
        volTs_d = mrk.get_volTs_d(arg_v)
        volType = volTs_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[volType]
        arg = class_instance.fromDict(volTs_d, mrk)

    elif 'Para' == name[-len('Para'):]:
        arg = DeterministicParameter.fromDict(arg_v)

    elif utils.NameHelper.getTypeFrom(name) != None:
        arg = utils.NameHelper.toClassArg(name, arg_v)

    elif name in ['ir_pc', 'pc', 'pc1', 'pc2'] and isinstance(arg_v, str):
        if not arg_v in models_calcs:
            raise Exception('model or calc does not exist - {0}, {1}'.format(arg_v, models_calcs.keys()))
        arg = models_calcs[arg_v]

    elif name == 'pc_list':
        for pc in arg_v:
            if not arg_v in models_calcs:
                raise Exception('model or calc does not exist - {0}'.format(arg_v, models_calcs.keys()))
        arg = [models_calcs[pc] for pc in arg_v]

    elif name == 'name' or 'type' == name[-len('type'):].lower():
        arg = arg_v

    elif isinstance(arg_v, numbers.Number):
        arg = arg_v

    else:
        arg = mrk.get_quote_v(arg_v)
        # quote_d = mrk.get_quote_d(arg_v)
        # arg = quote_d['v']

    if arg is None:
        raise Exception('unsupported argument name : {0}'.format(arg_v))

    return arg


def get_args_fromDict(d: dict, mrk: mx.MarketData, models_calcs, parameters):
    args = []
    for name, v in parameters.items():
        if name == 'self':
            continue

        if not name in d and v.default != inspect._empty:
            args.append(v.default)
        else:
            args.append(get_arg_fromValue(name, d[name], mrk, models_calcs))

    return args


# model parse
def parseClassFromDict(d: dict, models_calcs=[], mrk=mx.MarketData()):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')

    classTypeName = d[mx.CLASS_TYPE_NAME]

    if not classTypeName in globals():
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        class_instance = globals()[classTypeName]
        init = getattr(class_instance, "__init__", None)

        #args = get_args_fromDict(d, mrk, models_calcs, inspect.getfullargspec(init).args[1:])
        args = get_args_fromDict(d, mrk, models_calcs, inspect.signature(init).parameters)

        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise


class Rsg(mx.core_Rsg):
    def __init__(self, sampleNum, dimension=365, seed=1, skip=0, isMomentMatching=False, randomType='pseudo', subType='mersennetwister', randomTransformType='boxmullernormal'):

        self._randomType = randomType
        self._subType = subType
        self._randomTransformType = randomTransformType

        mx.core_Rsg.__init__(self, sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Rsg.__name__)

        return parseClassFromDict(d)

        # sampleNum = d['sampleNum']
        # dimension = d['dimension']
        # seed = d['seed']
        # skip = d['skip']
        # isMomentMatching = d['isMomentMatching']
        # randomType = d['randomType']
        # subType = d['subType']
        # randomTransformType = d['randomTransformType']

        # return Rsg(sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['sampleNum'] = self.sampleNum
        res['dimension'] = self.dimension
        res['seed'] = self.seed
        res['skip'] = self.skip
        res['isMomentMatching'] = self.isMomentMatching
        res['randomType'] = self.randomType
        res['subType'] = self.subType
        res['randomTransformType'] = self.randomTransformType

        return res

    randomType = property(lambda self: self._randomType,None,None)
    subType = property(lambda self: self._subType,None,None)
    randomTransformType = property(lambda self: self._randomTransformType,None,None)


class ScenarioBuilder:
    def __init__(self, json_dict: dict = None):
        # defualt
        if json_dict is None:
            self.reset()
        # predefined
        else:
            if 'hashcodes' in json_dict:
                del json_dict['hashcodes']

            self.check_json_dict(json_dict)
            self.__dict__ = json_dict

    @staticmethod
    def fromDict(d: dict):
        return ScenarioBuilder(d)

    def toDict(self):
        import copy
        return copy.deepcopy(self.__dict__)

    def hashCode(self):
        return utils.get_hashCode(self)

    def check_json_dict(self, d: dict):
        keys = ['models', 'calcs', 'timegrid', 'corr', 'rsg', 'filename', 'isMomentMatching']

        for k in keys:
            if not k in d:
                raise Exception("invalid json for scenario building. '{0}' is required\n{1}".format(k, d))

    def build_scenario(self, mrk: mx.MarketData()):
        if mrk is None:
            mrk = mx.MarketData()

        # models
        models_calcs = dict()

        models = []
        for m in self.models:
            model = parseClassFromDict(m, models_calcs, mrk)
            models_calcs[model.name] = model
            models.append(model)

        calcs = []
        for c in self.calcs:
            calc = parseClassFromDict(c, models_calcs, mrk)
            models_calcs[calc.name] = calc
            calcs.append(calc)

        # corr = mx.Matrix(self.corr)
        corr = mx.IdentityMatrix(len(self.models))

        for r, row in enumerate(self.corr):
            for c, v in enumerate(row):
                corr[r][c] = mrk.get_quote_v(v)

        utils.check_correlation(corr.toList())

        if len(models) != corr.rows() or len(models) != corr.columns():
            raise Exception("correlation matrix's rows({0}) and columns({1}) size must be same to model size({2})".format(corr.rows(), corr.columns(), len(models)))

        timegrid = parseClassFromDict(self._toDict(self.timegrid))
        rsg = Rsg.fromDict(self._toDict(self.rsg), mrk)

        return Scenario(models, calcs, corr, timegrid, rsg, self.filename, self.isMomentMatching)

    def reset(self):
        d = dict()

        d['models'] = []
        d['calcs'] = []
        d['corr'] = mx.IdentityMatrix(1).toList()
        d['timegrid'] = mx.TimeEqualGrid().toDict()
        d['rsg'] = Rsg(sampleNum=1000).toDict()
        d['filename'] = 'temp.npz'
        d['isMomentMatching'] = False

        self.__dict__ = d

    def _makeDictFromArgs(self, clsnm: str, name: str, **kwargs):
        d = dict()

        class_instance = globals()[clsnm]
        utils.check_args_in_dict(class_instance, clsnm, d, True)

        if name is not None:
            d['name'] = name

        d[mx.CLASS_TYPE_NAME] = clsnm
        d = { **d, **self._toDictArgs(kwargs)}

        # default arguments which does not exist in kwargs ( for serialize)

        init = getattr(class_instance, "__init__", None)

        for k, v in inspect.signature(init).parameters.items():
            if not k in d and v.default != inspect._empty:
                d[k] = v.default

        return d

    def _toDict(self, v):
        toDict = getattr(v, "toDict", None)

        if isinstance(v, dict):
            return v
        elif toDict is not None:
            return v.toDict()
        else:
            raise Exception('dict or serializable is required - {0}'.format(v))

    def _toDictArgs(self, d: dict):
        res = dict()

        for k, v in d.items():
            toDict = getattr(v, "toDict", None)

            if toDict is None:
                res[k] = utils.NameHelper.toDictArg(k, v)
            else:
                res[k] = v.toDict()

        return res

    def getModel(self, name):
        for m in self.models:
            if m.name == name:
                return m

    def addModel(self, clsnm: str, name: str, **kwargs):
        self.models.append(self._makeDictFromArgs(clsnm, name, **kwargs))
        self.resetCorrelation()

    def removeModel(self, name: str):
        self.models.remove(self.getModel(name))
        self.resetCorrelation()

    def getCalc(self, name):
        for c in self.calcs:
            if c['name'] == name:
                return c

    def addCalc(self, clsnm: str, name: str, **kwargs):
        self.calcs.append(self._makeDictFromArgs(clsnm, name, **kwargs))

    def removeCalc(self, name: str):
        self.calcs.remove(self.getCalc(name))

    def setTimeGrid(self, clsnm: str, **kwargs):
        self.timegrid = self._makeDictFromArgs(clsnm, None, **kwargs)

    def setTimeGridCls(self, tg):
        if isinstance(tg, (mx.TimeGrid, mx.TimeArrayGrid, mx.TimeEqualGrid)):
            self.timegrid = tg.toDict()
        else:
            raise Exception('TimeGrid type is required - {0}'.format(tg))

    def setRsg(self, clsnm: str, **kwargs):
        self.rsg = self._makeDictFromArgs(clsnm, None, **kwargs)

    def setRsgCls(self, rsg):
        if isinstance(rsg, Rsg):
            self.rsg = rsg.toDict()
        else:
            raise Exception('Rsg type is required - {0}'.format(rsg))

    def setCorrelationMatrix(self, m):
        if isinstance(m, mx.Matrix):
            self.corr = m.toList()
        elif isinstance(m, np.matrixlib.matrix):
            self.corr = m.tolist()
        else:
            raise Exception('Matrix type is required - {0}'.format(m))

    def resetCorrelation(self):
        dim = len(self.models)
        self.corr = np.identity(dim).tolist()
        # (mx.IdentityMatrix(len(self.models)).toList()).tolist()


# class Scenario(mx.core_ScenarioGenerator2):
class Scenario:
    def __init__(self, models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
        _corr = mx.Matrix(corr)

        # _dimension = (len(timegrid) - 1) * len(models)
        # _rsg = Rsg(rsg.sampleNum, _dimension, rsg.seed, rsg.skip, rsg.isMomentMatching, rsg.randomType, rsg.subType, rsg.randomTransformType)

        self.models = models
        self.calcs = calcs
        self.corr = _corr
        self.timegrid = timegrid
        self.rsg = rsg
        self.filename = filename
        self.isMomentMatching = isMomentMatching

        # set jsonStr for generation

    @staticmethod
    def fromDict(d: dict, mrk: mx.MarketData = None):
        if not isinstance(d, dict):
            raise Exception('dictionary type is required')

        sjb = ScenarioBuilder(d)

        if mrk == None:
            mrk = mx.MarketData()

        return sjb.build_scenario(mrk)
        # args = sjb.build_scenario(mrk)
        # return Scenario(*args)

    def toDict(self):
        res = dict()

        res['models'] = [ m.toDict() for m in self.models]
        res['calcs'] = [ c.toDict() for c in self.calcs]
        res['corr'] = self.corr.toList()
        res['timegrid'] = self.timegrid.toDict()
        res['rsg'] = self.rsg.toDict()
        res['filename'] = self.filename
        res['isMomentMatching'] = self.isMomentMatching

        return res

    def hashCode(self):
        return utils.get_hashCode(self)

    def clone(self, **kwargs):
        try:
            _dimension = (len(self.timegrid) - 1) * len(self.models)
            _rsg = Rsg(self.rsg.sampleNum, _dimension, self.rsg.seed, self.rsg.skip, self.rsg.isMomentMatching,
                       self.rsg.randomType, self.rsg.subType, self.rsg.randomTransformType)

            models = kwargs['models'] if 'models' in kwargs else self.models
            calcs = kwargs['calcs'] if 'calcs' in kwargs else self.calcs
            corr = kwargs['corr'] if 'corr' in kwargs else self.corr
            timegrid = kwargs['timegrid'] if 'timegrid' in kwargs else self.timegrid
            rsg = kwargs['rsg'] if 'rsg' in kwargs else _rsg
            filename = kwargs['filename'] if 'filename' in kwargs else self.filename
            isMomentMatching = kwargs['isMomentMatching'] if 'isMomentMatching' in kwargs else self.isMomentMatching

            if not filename[-4:] == '.npz':
                filename += '.npz'

            scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)

            return scen

        except Exception as e:
            if len(e.args) >= 1:
                e.args = (e.args[0] + '\nscenario inputs: {0}'.format((self.models, self.calcs, self.corr, self.timegrid,
                        self.rsg, self.filename, self.isMomentMatching)),) + e.args[1:]
            raise

    def getModel(self, name) -> mx.core_ProcessModel:
        model = [m for m in self.models if m.name == name]

        if len(self.models) == 0:
            raise Exception('empty models')

        if len(model) == 0:
            names = [m.name for m in self.models]
            raise Exception('model does not exist - {0} in {1}'.format(name, names))

        return model[0]

    def getCalc(self, name, default=None):
        calc = [c for c in self.calcs if c.name == name]
        if len(calc) == 0:
            return default
        return calc[0]

    def _write_log(self, scen):
        # logging and generation history
        from mxdevtool.data.repositories.settings import get_repo
        get_repo().logging_scen(scen)

        results = np.load(scen.filename)
        d = {
            **results,
            'input_json': utils.toJsonStr(scen)
        }

        np.savez(scen.filename, **d)


    def generate(self):
        hashCode = utils.get_hashCode(self) # for logging

        _dimension = (len(self.timegrid) - 1) * len(self.models)
        _rsg = Rsg(self.rsg.sampleNum, _dimension, self.rsg.seed, self.rsg.skip, self.rsg.isMomentMatching,
                       self.rsg.randomType, self.rsg.subType, self.rsg.randomTransformType)

        core = mx.core_ScenarioGenerator2(self.models, self.calcs, self.corr, self.timegrid, _rsg, self.filename, self.isMomentMatching, hashCode)
        core.generate()

        self._write_log(self)

        return ScenarioResults(self.filename)


    def generate_clone(self, **kwargs):
        scen = self.clone(**kwargs)
        hashCode = utils.get_hashCode(scen) # for logging

        core = mx.core_ScenarioGenerator2(scen.models, scen.calcs, scen.corr, scen.timegrid, scen.rsg, scen.filename, scen.isMomentMatching, hashCode)
        core.generate()

        self._write_log(scen)

        return ScenarioResults(scen.filename)

    def report(self, **kwargs):
        from mxdevtool.view.reports import report_scen
        report_scen(self, **kwargs)

    def getResults(self):
        return ScenarioResults(self.filename)


class ScenarioResults(mx.core_ScenarioResult):
    def __init__(self, filename):
        mx.core_ScenarioResult.__init__(self, filename)
        self.shape = (self.simulNum, self.assetNum, self.timegridNum)
        self.names_idx_d = dict()
        self.idx_names_d = dict()

        self.scen = None

        for info in self.genInfo:
            self.names_idx_d[info[1]] = int(info[0])
            self.idx_names_d[int(info[0])] = info[1]

    def toNumpyArr(self) -> np.ndarray:
        npz = np.load(self.filename)
        arr = npz['data']
        arr.reshape(self.shape) # (scenario, asset, time)

        return arr

    def assetPath(self, idx_or_name):
        if isinstance(idx_or_name, int): return self._assetPath(idx_or_name)
        elif isinstance(idx_or_name, str): return self._assetPath(self.names_idx_d[idx_or_name])
        else: raise Exception('int or str is required - {0}'.format(idx_or_name))

    def nameList(self):
        return [k for k in self.names_idx_d.keys()]

    def getAssetIndex(self, name):
        if not name in self.names_idx_d:
            raise Exception("scenario path does not exist - {0} in {1}".format(name, self.names_idx_d))
        return self.names_idx_d[name]

    def __getitem__(self, scenCount):
        if not isinstance(scenCount, int):
            raise Exception('ScenCount is required - {0}'.format(scenCount))

        return self._multiPath(scenCount)

    # def assetPath(self, assetIdx):
    #     return self._assetPath() _multiPathAllTPos(t_pos)

    def tPosSlice(self, t_pos, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPos(t_pos)
        else:
            return self._multiPathTPos(scenCount, t_pos)

    def timeSlice(self, time, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateTime(time)
        else:
            return self._multiPathTPosInterpolateTime(scenCount, time)

    def dateSlice(self, date, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateDate(date)
        else:
            return self._multiPathTPosInterpolateDate(scenCount, date)

    def getScenario(self):
        if self.scen is None:
            # json_str = get_repo().get_scen_log(self.hashCode) # now files
            # d = json.loads(json_str)
            # sb = ScenarioBuilder(d)

            npz = np.load(self.filename)
            json_str = npz['input_json']
            d = json.loads(str(json_str))
            self.scen = Scenario.fromDict(d)

        return self.scen

    def show(self):
        import mxdevtool.utils as mx_u
        mx_u.npzee_view(self)

    def report(self, typ='html'):
        from mxdevtool.view.reports import report_scen

        report_scen(self, typ)

    nameList = property(nameList,None,None)


class CompositeScenarioResults(ScenarioResults):
    def __init__(self, scen_res_d, basescen_name, **kwargs):
        self.scen_res_d = scen_res_d
        self.basescen_name = basescen_name

        # check exist
        # if not basescen_name in self.scen_res_d:
        #     raise Exception('scenario results does not exist -{0}'.format(basescen_name))

        self.basescen_res = self.scen_res_d[basescen_name]

        ScenarioResults.__init__(self, self.basescen_res.filename)

        # (asset_name, asset_idx, scen_name)
        self.replace_tuples = [(k, self.getAssetIndex(k), v) for k, v in kwargs.items()]
        self.replace_d = kwargs # (asset_name, scen_name)

        self.check_timegrid([res.timegrid for res in self.scen_res_d.values()])

    def toDict(self):
        d = dict()

        d[mx.CLASS_TYPE_NAME] = CompositeScenarioResults.__name__
        _scen_res_d = dict()

        for k, v in self.scen_res_d.items():
            _scen_res_d[k] = v.filename

        d['scen_res_d'] = _scen_res_d
        d['basescen_name'] = self.basescen_name
        d['replace_d'] = self.replace_d

        return d

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, CompositeScenarioResults.__name__)

        kwargs = d['replace_d']
        scen_res_d = dict()

        for k, v in d['scen_res_d'].items():
            scen_res_d[k] = ScenarioResults(v)

        basescen_name = d['basescen_name']
        csr = CompositeScenarioResults(scen_res_d, basescen_name, **kwargs)

        return csr

    def check_timegrid(self, timegrid_list):
        if len(timegrid_list) == 0:
            raise Exception('items is empty')

        # refdate
        refDates = [tg.refDate() for tg in timegrid_list]
        if len(set(refDates)) != 1:
            raise Exception('refDate is not same - {0}'.format(refDates))

        # size
        sizes = [ len(tg) for tg in timegrid_list ]
        if len(set(sizes)) != 1:
            raise Exception('size is not same - {0}'.format(sizes))

        # dates..?

    def toNumpyArr(self) -> np.ndarray:
        arr = super().toNumpyArr()

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            arr[:,idx,:] = res._assetPath(idx)

        return arr

    def assetPath(self, idx_or_name):
        idx = idx_or_name

        if isinstance(idx_or_name, int): idx = idx_or_name
        elif isinstance(idx_or_name, str): idx = self.getAssetIndex(idx_or_name)
        else: raise Exception('int or str is required - {0}'.format(idx_or_name))

        if idx in [_idx for _, _idx, _ in self.replace_tuples]:
            res = self. scen_res_d[self.idx_names_d[idx]]
            return res._assetPath(idx)
        else:
            return self._assetPath(idx)

    def __getitem__(self, scenCount):
        if not isinstance(scenCount, int):
            raise Exception('ScenCount is required - {0}'.format(scenCount))

        arr = super()._multiPath(scenCount)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            arr[idx] = res._multiPath(scenCount)[idx]

        return arr

    def analytic_multiPath(self):
        arr = super().analytic_multiPath(self)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            replace_arr = res.analytic_multiPath(idx)
            arr[idx] = replace_arr[idx]

        return arr

    def average_multiPath(self):
        arr = super().analytic_multiPath(self)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            replace_arr = res.average_multiPath(idx)
            arr[idx] = replace_arr[idx]

        return arr

    def tPosSlice(self, t_pos, scenCount=None):
        arr = super().tPosSlice(t_pos, scenCount)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            replace_arr = res.tPosSlice(t_pos, scenCount)
            arr[idx] = replace_arr[idx]

        return arr

    def timeSlice(self, time, scenCount=None):
        arr = super().timeSlice(time, scenCount)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            replace_arr = res.timeSlice(time, scenCount)
            arr[idx] = replace_arr[idx]

        return arr

    def dateSlice(self, date, scenCount=None):
        arr = super().dateSlice(date, scenCount)

        for asset_name, idx, scen_name in self.replace_tuples:
            res = self.scen_res_d[scen_name]
            replace_arr = res.dateSlice(date, scenCount)
            arr[idx] = replace_arr[idx]

        return arr

    def getScenario(self):
        raise Exception('not support.')

    def show(self):
        import mxdevtool.utils as mx_u
        mx_u.npzee_view(self.toNumpyArr())



class XenarixFileManager(mx.ManagerBase):
    def __init__(self, config: dict):
        mx.ManagerBase.__init__(self, config)

        self.location = config['location']
        self.results_dir = os.path.join(self.location, XENREPO_RESULTS_DIR)

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)


    def _build_dict(self, scen: Scenario):
        scen_d = scen.toDict()
        hashcodes_d = dict()

        hashcodes_d['base'] = scen.hashCode()

        scen_d[HASHCODES_KEY] = hashcodes_d

        return scen_d

    def _save(self, name: str, ext: str, arg):
        json_str = None
        path = os.path.join(self.location, name + '.' + ext)

        utils.save_file(path, arg, self._build_dict)

    def _saves(self, name: str, ext: str, **kwargs):
        json_str = None
        path = os.path.join(self.location, name + '.' + ext)

        utils.saves_file(path, kwargs, self._build_dict)

    def _load(self, name: str, ext: str):
        path = os.path.join(self.location, name + '.' + ext)
        f = open(path, "r")
        json_str = f.read()
        scen_input = json.loads(json_str)

        scen = None

        if ext == XENFILE_EXT:
            sb = ScenarioBuilder(scen_input)
            scen = sb.build_scenario(mrk=None)
        elif ext == XENBUILDERFILE_EXT:
            scen = ScenarioBuilder(scen_input)
        else:
            raise Exception('unknown type file - {0}' - ext)

        return scen

    def _loads(self, name: str, ext: str):
        path = os.path.join(self.location, name + '.' + ext)
        f = open(path, "r")
        json_str = f.read()
        scen_d = json.loads(json_str)

        res = dict()

        for k, v in scen_d.items():
            if ext == XENFILE_SET_EXT:
                sb = ScenarioBuilder(v)
                res[k] = sb.build_scenario(mrk=None)
            elif ext == XENBUILDERFILE_SET_EXT:
                res[k] = ScenarioBuilder(v)
            else:
                raise Exception('unknown type file - {0}' - ext)

        return res

    # xen -----------------------
    def save_xen(self, name: str, scen: Scenario):
        if not isinstance(scen, Scenario):
            raise Exception('Scenario type is required - {0}'.format(scen))

        self._save(name, XENFILE_EXT, scen)

    def save_xens(self, name: str, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, Scenario):
                raise Exception('Scenario type is required - {0}, {1}'.format(k, v))

        self._saves(name, XENFILE_SET_EXT, **kwargs)

    def load_xen(self, name: str):
        return self._load(name, XENFILE_EXT)

    def load_xens(self, name: str):
        return self._loads(name, XENFILE_SET_EXT)

    # xnb -----------------------
    def save_xnb(self, name: str, sb: ScenarioBuilder):
        if not isinstance(sb, ScenarioBuilder):
            raise Exception('ScenarioBuilder type is required - {0}'.format(sb))

        self._save(name, XENBUILDERFILE_EXT, sb)

    def save_xnbs(self, name: str, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, ScenarioBuilder):
                raise Exception('ScenarioBuilder type is required - {0}, {1}'.format(k, v))

        self._saves(name, XENBUILDERFILE_SET_EXT, **kwargs)

    def load_xnb(self, name: str):
        return self._load(name, XENBUILDERFILE_EXT)

    def load_xnbs(self, name: str):
        return self._load(name, XENBUILDERFILE_SET_EXT)

    # inspector
    def _get_file_list(self, *args):
        file_names = [os.path.splitext(fn)[0] for fn in os.listdir(self.location)
            if any(fn.endswith(ext) for ext in args)]

        return file_names

    def scenList(self):
        return self._get_file_list(XENFILE_EXT)

    def scenBuilderList(self):
        return self._get_file_list(XENBUILDERFILE_EXT)

    # generation
    def generate_xen(self, name: str):
        scen = self.load_xen(name)
        filename = os.path.join(self.results_dir, name + '.npz')
        return scen.generate_clone(filename=filename)

    def generate_xens(self, name: str):
        scen_d = self.load_xens(name)
        results = dict()

        for k, scen in scen_d.items():
            filename = os.path.join(self.results_dir, name, k + '.npz')
            results[k] = scen.generate_clone(filename=filename)

        return results

    def generate_xnb(self, name: str, mrk: mx.MarketData):
        sb = self.load_xnb(name)
        results = []

        filename = os.path.join(self.results_dir, name + '.npz')
        scen = sb.build_scenario(mrk)
        return scen.generate_clone(filename=filename)

    def generate_xnbs(self, name: str, mrk: mx.MarketData):
        sb_d = self.load_xnbs(name)
        results = []

        for k, sb in sb_d.items():
            filename = os.path.join(self.results_dir, name, k + '.npz')
            scen = sb.build_scenario(mrk)
            results.append(scen.generate_clone(filename=filename))

        return results

    def _load_results(self, name: str):
        filename = os.path.join(self.results_dir, name + '.npz')
        return ScenarioResults(filename=filename)

    def _loads_results(self, name: str):
        #scen_d = self._load(name, ext)
        path = os.path.join(self.results_dir, name + '.npz')

        results = []
        #for k in scen_d.keys():
        for f in os.listdir(path):
            filename = os.path.join(self.results_dir, name, f)
            results.append(ScenarioResults(filename=filename))

        return results

    def load_results_xen(self, name: str):
        return self._load_results(name)

    def load_results_xens(self, name: str):
        return self._loads_results(name)

    def load_results_xnb(self, name: str):
        return self._load_results(name)

    def load_results_xnbs(self, name: str):
        return self._loads_results(name)


def generate1d(model, calcs, timegrid, rsg, filename: str, isMomentMatching = False):
    _calcs = calcs

    if calcs is None:
        _calcs = []

    corr = mx.IdentityMatrix(1)

    scen = Scenario([model], _calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    get_repo().logging_scen(scen)

    return ScenarioResults(filename)


def generate(models, calcs, corr, timegrid, rsg, filename: str, isMomentMatching = False):
    if calcs is None:
        calcs = []

    scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    get_repo().logging_scen(scen)

    return ScenarioResults(filename)

