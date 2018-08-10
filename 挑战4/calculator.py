#!/usr/bin/env python3

import csv
import sys
from multiprocessing import Process, Queue


class Args(object):
    def __init__(self, args):
        self.args = args
        self.configfile = self._get_file('-c')
        self.userdatafile = self._get_file('-d')
        self.outfile = self._get_file('-o')

    def _get_file(self, param):
        index = self.args.index(param)
        return self.args[index+1]


class Config(object):
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = self._read_config()

    def _read_config(self):
        config = {}
        with open(self.configFile) as file:
            for line in file.readlines():
                data = line.strip()
                if len(data) <= 0:
                    continue
                else:
                    data = data.split("=")
                    config[data[0].strip()] = float(data[1].strip())
        return config
        

class UserData(Process):
    def __init__(self, userFile, q):
        self.userFile = userFile
        # self.userData = self._read_user_data()
        self.queue_userdata = q
        super().__init__()


    def _read_user_data(self):
        # userdata = []
        with open(self.userFile) as file:
            for line in file.readlines():
                userinfo = line.strip()
                if len(userinfo) <= 0:
                    continue
                else:
                    id, wage = line.strip().split(',')
                    print(id, wage)
                    # self.queue_userdata.put(userinfo)
                    yield (int(id), int(wage))

    def run(self):
        for item in self._read_user_data():
            self.queue_userdata.put(item)


class IncomeTaxCalculator(Process):
    def __init__(self, config, q1, q2):
        self.config = config
        self.queue_userdata = q1
        self.queue_info = q2
        super().__init__()

    def _get_insu(self, wage):
        all_sum = sum(self.config.values()) - self.config["JiShuL"] -self.config["JiShuH"]
        if wage < self.config["JiShuL"]:
            wage = self.config["JiShuL"]
        elif wage > self.config["JiShuH"]:
            wage = self.config["JiShuH"]

        return wage * all_sum

    def _get_tax(self, wage, insu):
        T_income = wage - insu
        if T_income <= 3500:
            return 0
        else:
            T_income = wage - 3500 - insu
            if T_income < 1500:
                x = 0.03
                n = 0
            elif T_income < 4500:
                x = 0.1
                n = 105
            elif T_income < 9000:
                x = 0.2
                n = 555
            elif T_income < 35000:
                x = 0.25
                n = 1005
            elif T_income < 55000:
                x = 0.3
                n = 2755
            elif T_income < 80000:
                x = 0.35
                n = 5505
            else:
                x = 0.45
                n = 13505
            return T_income * x - n


    def calc_for_all_userdata(self):
        # all_data = []
        try:
            userdata = self.queue_userdata.get(timeout=1)
        except Exception as e:
            print(e + "get end")
        print(userdata)
        userid = userdata[0]
        wage = float(userdata[1])
        insu = float(self._get_insu(wage))
        tax = float(self._get_tax(wage, insu))
        info = list("{0},{1:.0f},{2:.2f},{3:.2f},{4:.2f}".format(userid, wage, insu, tax, (wage - insu -tax)).split(','))
        self.queue_info.put(info)
        print(info)
    def run(self):
        while True:
            self.calc_for_all_userdata()

class Write_info():
    def __init__(self, outfile, q2):
        self.queue_info = q2
        super().__init__()

    def write_info_to_file(self):
        try:
            info = self.queue_info.get(timeout=1)
        except Exception as e:
            print(e + "get write info end!")

        print(info)
        with open(outfile, "a") as file:
            writer = csv.writer(file)
            writer.writerow(info)

    def run(self):
        while True:
            self.write_info_to_file()

if __name__ == "__main__":
    args = Args(sys.argv[1:])
    configfile = args.configfile
    userdata = args.userdatafile
    outfile = args.outfile
    
    cfg = Config(configfile)
    config = cfg.config
    # print(config)

    q1 = Queue()
    q2 = Queue()

    P_userdata = Process(target=UserData, args=(userdata, q1))
    # P_income = Process(target=IncomeTaxCalculator, args=(config, q1, q2))
    # P_write_info = Process(target=Write_info, args=(outfile, q2))

    P_userdata.start()
    # P_income.start()
    # P_write_info.start()

    P_userdata.join()
    # P_income.join()
    # P_write_info.join()
