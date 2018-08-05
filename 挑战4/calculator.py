#!/usr/bin/env python3

import csv
import sys
from multiprocessing import Process, Queue

queue_userdata = Queue()
queue_info = Queue()

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
        

class UserData(object):
    def __init__(self, userFile):
        self.userFile = userFile
        self.userData = self._read_user_data()

    def _read_user_data(self):
        userdata = []
        with open(self.userFile) as file:
            for line in file.readlines():
                userinfo = line.strip()
                if len(userinfo) <= 0:
                    continue
                else:
                    userinfo = tuple(line.strip().split(','))
                    # print(userinfo)
                    queue_userdata.put(userinfo)
                    userdata.append(userinfo)
            # print("put done!!")
            # print(userdata)


class IncomeTaxCalculator(object):
    def __init__(self, config):
        self.config = config
        self.run()

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
        all_data = []
        try:
            userdata = queue_userdata.get()
        except Exception as e:
            print(e + "get end")

        userid = userdata[0]
        wage = float(userdata[1])
        insu = float(self._get_insu(wage))
        tax = float(self._get_tax(wage, insu))
        info = list("{0},{1:.0f},{2:.2f},{3:.2f},{4:.2f}".format(userid, wage, insu, tax, (wage - insu -tax)).split(','))
        queue_info.put(info)
        # print(info)
    def run(self):
        while True:
            self.calc_for_all_userdata()

class Write_info():
    def __init__(self, outfile):
        self.run()

    def write_info_to_file(self):
        try:
            info = queue_info.get()
        except Exception as e:
            print(e + "get write info end!")

        # if len(info) <= 0:
        #     continue
        # else:
        # print(info)
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

    P_userdata = Process(target=UserData, args=(userdata,)).start()
    P_income = Process(target=IncomeTaxCalculator, args=(config, )).start()
    P_write_info = Process(target=Write_info, args=(outfile, )).start()



