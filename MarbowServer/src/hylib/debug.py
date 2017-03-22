#-*- coding: utf-8 -*-
 
import time
import inspect

from hybase import *

class HYDebug(HYBase):
    dbg_flags = {
        'INFO':1,
        'ERR':1,
        'WARN':1,
        'NOTI':1,
        'ALERT':1,
        'DEBUG':1,
        'VERB':1
    }

    def dbg_flag_vaild(self, flag):
        return self.dbg_flags[flag]

    def dbg_dump(self, level, flag, str):
        if self.dbg_flags[flag] & self.dbg_flags[level]:
            tstr = time.strftime('%y/%m/%d %H:%M:%S', time.localtime())

            dstr = "%s [%s]%s.%s: %s" % (tstr, self.modid, level, flag, str)

            print dstr

    def dbg_flag_add(self, flag, default):
        self.dbg_flags[flag] = default

    def dbg_info(self, flag, str):
        self.dbg_dump("INFO", flag, str)

    def dbg_err(self, flag, str):
        self.dbg_dump("ERR", flag, str)

    def dbg_warn(self, flag, str):
        self.dbg_dump("WARN", flag, str)

    def dbg_noti(self, flag, str):
        self.dbg_dump("NOTI", flag, str)

    def dbg_alert(self, flag, str):
        self.dbg_dump("ALERT", flag, str)

    def dbg_debug(self, flag, str):
        self.dbg_dump("DEBUG", flag, str)

    def dbg_verb(self, flag, str):
        self.dbg_dump("VERB", flag, str)

    def dbg_on(self, flag):
        self.dbg_flags[flag] = 1

    def dbg_off(self, flag):
        self.dbg_flags[flag] = 0

    def dbg_flags_dump(self):
        for key in self.dbg_flags:
            state = "off"
            if self.dbg_flags[key] == 1:
                state = "on"
            print "%6s: %s" % (key, state)
            
    def help_debug(self):  
        print "  debug [FLAG] [on|off]"

    def do_debug(self, line):  
        argv = line.split()
        argc = len(argv)

        if argc == 0:
            self.dbg_flags_dump()
        elif argc == 2:
            if argv[1] == "on":
                self.dbg_on(argv[0])
            elif argv[1] == "off":
                self.dbg_off(argv[0])
            else:
                self.help_debug()
        else:
            self.help_debug()

#End of file
