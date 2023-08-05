# -*- coding: utf-8 -*-

import os
import re
import logging
import datetime
import traceback
import threading
import multiprocessing
from logging import handlers
from inspect import getframeinfo, stack


class GorLogger:
    logDir = ''
    loggerName = ''
    logFileName = ''
    log_level = 'info'
    logInstance = None
    logger_queue = None

    def __init__(self):
        self.logger = None

    def _log_format(self, level, f_name, line_no, func_name, msg):

        log_msg = ""
        try:
            if getattr(logging, level) < getattr(logging, GorLogger.log_level.upper()):
                return log_msg

            "Date Time Format: 2022-01-10 18:16:40,954"
            dt_now = datetime.datetime.now()
            _dt = dt_now.strftime("%Y-%m-%d %H:%M:%S,%f")

            log_msg = f"{_dt} - {level} - {os.path.basename(f_name)} - [{func_name}:{line_no}] - {msg}"

            GorLogger.logger_queue.put(log_msg)

        except Exception as e:
            traceback.print_exc()

        return log_msg

    def get_log_info(self):
        try:
            caller = getframeinfo(stack()[2][0])
            return caller.filename, caller.lineno, caller.function
        except:
            traceback.print_exc()
            return "", "", ""

    def debug(self, msg: str = ""):
        try:
            f_name, line_no, func_name = self.get_log_info()
            log_msg = self._log_format("DEBUG", f_name, line_no, func_name, msg)

        except Exception as e:
            traceback.print_exc()

    def info(self, msg: str = ""):
        try:
            f_name, line_no, func_name = self.get_log_info()
            log_msg = self._log_format("INFO", f_name, line_no, func_name, msg)

        except Exception as e:
            traceback.print_exc()

    def warning(self, msg: str = ""):
        try:
            f_name, line_no, func_name = self.get_log_info()
            log_msg = self._log_format("WARNING", f_name, line_no, func_name, msg)

        except Exception as e:
            traceback.print_exc()

    def error(self, msg: str = ""):
        try:
            f_name, line_no, func_name = self.get_log_info()
            log_msg = self._log_format("ERROR", f_name, line_no, func_name, msg)

        except Exception as e:
            traceback.print_exc()

    def critical(self, msg: str = ""):
        try:
            f_name, line_no, func_name = self.get_log_info()
            log_msg = self._log_format("CRITICAL", f_name, line_no, func_name, msg)

        except Exception as e:
            traceback.print_exc()

    def logs_dump(self):
        while True:
            try:

                logs = GorLogger.logger_queue.get()
                level = getattr(logging, GorLogger.log_level.upper())

                self.logger.log(level, logs)

            except Exception as e:
                traceback.print_exc()

    def create_logger(self):
        logger = logging.getLogger(GorLogger.loggerName)
        level = getattr(logging, GorLogger.log_level.upper())
        logger.setLevel(level)
        formatter = logging.Formatter('%(message)s')
        if not logger.handlers:
            if not os.path.exists(GorLogger.logDir):
                os.makedirs(GorLogger.logDir)
            handler = logging.handlers.TimedRotatingFileHandler(os.path.join(GorLogger.logDir + GorLogger.logFileName),
                                                                when='midnight', backupCount=14)
            handler.suffix = "%Y-%m-%d"
            handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def loggerInit(self, loggerName, fileName, logDirName, LOG_LEVEL):
        GorLogger.logFileName = fileName
        GorLogger.loggerName = loggerName
        GorLogger.log_level = LOG_LEVEL
        GorLogger.logger_queue = multiprocessing.Queue()
        t = threading.Thread(target=self.logs_dump)
        t.start()

        if len(str(logDirName).strip()) == 0:
            GorLogger.logDir = './'
        elif not str(logDirName).strip().endswith('/'):
            GorLogger.logDir = logDirName + "/"
        else:
            GorLogger.logDir = logDirName
        self.logger = self.create_logger()

    def getInstance(self, loggerName, fileName, logDirName, LOG_LEVEL):
        if GorLogger.logInstance is None:
            self.loggerInit(loggerName, fileName, logDirName, LOG_LEVEL)
            GorLogger.logInstance = GorLogger()

        return GorLogger.logInstance
