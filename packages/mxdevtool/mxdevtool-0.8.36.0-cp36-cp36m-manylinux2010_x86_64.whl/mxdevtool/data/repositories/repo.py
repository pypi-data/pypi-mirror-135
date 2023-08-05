import mxdevtool as mx
import mxdevtool.utils as utils
import os, json


class Repository:
    def logging_scen(self, scenario):
        pass

    def addHolidays(self, cal, dates):
        pass

    def removeHolidays(self, cal, dates):
        pass

    def get_scen_log(self, hashCode: str) -> str:
        pass


class DefaultRepository(Repository):
    def __init__(self):
        self.scen_log = dict()

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    def logging_scen(self, scenario):
        hashCode = utils.get_hashCode(scenario)
        jsonStr = json.dumps(scenario.toDict())

        # print('DefaultRepository logging', hashCode, len(self.scen_log))

        self.scen_log[hashCode] = jsonStr


class FolderRepository(Repository):
    def __init__(self, config):
        if isinstance(config, str):
            self.config = {'location': config}
        else:
            self.config = config

        self.paths = dict()
        self.xenarix_manager = None
        self.shock_manager = None

        self.initialize()

    def initialize(self):
        from mxdevtool.xenarix import XenarixFileManager
        from mxdevtool.shock import ShockFileManager

        repo_path = self.config['location']

        def make_dir_not_exist(path, name):
            if not os.path.exists(path):
                os.makedirs(path)
            self.paths[name] = path            

        # xenarix 
        xen_path = os.path.join(repo_path, 'xenarix')
        make_dir_not_exist(xen_path, 'xenarix')
        xfm_config = { 'location': xen_path }
        self.xenarix_manager = XenarixFileManager(xfm_config)

        # shock
        shock_path = os.path.join(repo_path, 'shock')
        make_dir_not_exist(shock_path, 'shock')
        sfm_config = { 'location': shock_path }
        self.shock_manager = ShockFileManager(sfm_config)

        # setting
        setting_path = os.path.join(repo_path, 'setting')
        make_dir_not_exist(setting_path, 'setting')

        # setting - calendar
        calendar_path = os.path.join(setting_path, 'calendar')
        make_dir_not_exist(calendar_path, 'calendar')

        # logging
        log_path = os.path.join(repo_path, 'log')
        make_dir_not_exist(log_path, 'log')

    def logging_scen(self, scen):
        hashCode = utils.get_hashCode(scen)
        jsonStr = json.dumps(scen.toDict())
        filename = os.path.join(self.paths['log'], hashCode)
        f = open(filename, "w")
        f.write(jsonStr)
        f.close()

        # print('FolderRepository logging', hashCode)

    def getScenario(self, name: str):
        return self.xenarix_manager.load_xen(name)

    def get_scen_log(self, hashCode: str) -> str:
        log_path = self.paths['log']
        files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]
        
        # if not hashCode in files:
        #     raise Exception('hashcode does not exist - {0}'.format(hashCode))

        for f in files:
            if hashCode == f:
                f = open(os.path.join(log_path, f) , "r")
                json_str = f.read()
                f.close()

                return json_str
        
        raise Exception('scenario log does not exist in {0} - {1}'.format(log_path, hashCode))

    def get_subpath(self, name):
        if name in self.paths:
            return self.paths[name]
        else:
            raise Exception('unknown calendar - {0}'.format(name))
    
    def _action_holiday(self, calendar, line):
        date_act = line.strip('\n').split(',') 
        date = date_act[0] 
        act = date_act[1]
        
        if act == 'add':
            calendar.addHoliday(mx.dateParseISO(date))
        elif act == 'remove':
            calendar.removeHoliday(mx.dateParseISO(date))
        else:
            raise Exception('unknown action of holiday - {0}, {1}'.format(date, act))

    def load_configuration_calendar(self):
        calendar_path = self.get_subpath('calendar')
        items = os.listdir(calendar_path)

        for item in items:
            cal = None
            class_instance = globals()['mx'] .__dict__.get(item)
            if class_instance != None:
                cal = class_instance()
            else:
                cal = mx.UserCalendar(item) # weekend is default holiday

            filename = os.path.join(calendar_path, item)
            f = open(filename, 'r')
            for line in f.readlines():
                self._action_holiday(cal, line)

    def load_configuration(self):
        self.load_configuration_calendar()

    def _save_holidays(self, cal: mx.Calendar, dates: list, value, onlyrepo):
        """[summary]

        Args:
            cal (mx.Calendar): [description]
            dates (list): target dates
            value (str): 'add', 'remove'
        """        

        filename = os.path.join(self.get_subpath('calendar'), str(cal))
        res = []
        res_d = dict()
        
        if os.path.exists(filename):
            f = open(filename, 'r')
            lines = set(f.readlines())
            for line in lines:
                date_act = line.split(',') 
                res_d[date_act[0]] = date_act[1]

            f.close()

        dateStrList = utils.toStrList(dates)
        dateStrList = list(set(dateStrList))

        for dateStr in dateStrList:
            res_d[dateStr] = value
        
        for k, v in res_d.items():
            line = k + ',' + v
            res.append(line)

            if onlyrepo is False:
                self._action_holiday(cal, line)

        f = open(filename, 'w+')
        f.writelines('\n'.join(res))
        #f.writelines(res)
        f.close()

    def addHolidays(self, cal: mx.Calendar, dates: list, onlyrepo=False):
        self._save_holidays(cal, dates, 'add', onlyrepo)

    def removeHolidays(self, cal: mx.Calendar, dates: list, onlyrepo=False):
        self._save_holidays(cal, dates, 'remove', onlyrepo)