#!/usr/bin/env python
import os
import pickle
import time
import datetime
import math
import numpy as np
from collections import namedtuple
from bscearth.utils.date import date2str
from dateutil.relativedelta import *
from typing import List

class JobSection:
  SIM = "SIM"
  POST = "POST"
  TRANSFER_MEMBER = "TRANSFER_MEMBER"
  TRANSFER = "TRANSFER"
  CLEAN_MEMBER = "CLEAN_MEMBER"
  CLEAN = "CLEAN"

THRESHOLD_OUTLIER = 2
SECONDS_IN_ONE_HOUR = 3600
SECONDS_IN_A_DAY = 86400

PklJob = namedtuple('PklJob', ['name', 'id', 'status', 'priority', 'section', 'date', 'member', 'chunk', 'out_path_local', 'err_path_local', 'out_path_remote', 'err_path_remote'])

def tostamp(string_date):
  # type: (str) -> int
  """
  String datetime to timestamp
  """
  if string_date and len(string_date) > 0:
      return int(time.mktime(datetime.datetime.strptime(string_date,
                                                        "%Y-%m-%d %H:%M:%S").timetuple()))
  else:
      return 0

def parse_number_processors(processors_str):
  # type: (str) -> int  
  components = processors_str.split(":")
  processors = int(sum(
      [math.ceil(float(x) / 36.0) * 36.0 for x in components]))
  return processors

def get_jobs_with_no_outliers(jobs):
  """ Detects outliers and removes them from the returned list """
  # type: (List[Job]) -> List[Job]
  new_list = []
  data_run_times = [job.run_time for job in jobs]
  # print(data_run_times)
  if len(data_run_times) == 0:
    return jobs  
  
  mean = np.mean(data_run_times)
  std = np.std(data_run_times)
  
  # print("mean {0} std {1}".format(mean, std))
  if std == 0:
    return jobs

  for job in jobs:
    z_score = (job.run_time - mean) / std
    # print("{0} {1} {2}".format(job.name, np.abs(z_score), job.run_time))
    if np.abs(z_score) <= THRESHOLD_OUTLIER and job.run_time > 0:
      new_list.append(job)
    # else:
    #   print(" OUTLIED {0} {1} {2}".format(job.name, np.abs(z_score), job.run_time))  
  return new_list

def date_plus(date, chunk_unit, chunk, chunk_size=1):
  previous_date = date
  if chunk is not None and chunk_unit is not None:
      chunk_previous = (chunk - 1) * (chunk_size)
      chunk = chunk * chunk_size
      if (chunk_unit == "month"):
          date = date + relativedelta(months=+chunk)
          previous_date = previous_date + \
              relativedelta(months=+chunk_previous)
      elif (chunk_unit == "year"):
          date = date + relativedelta(years=+chunk)
          previous_date = previous_date + \
              relativedelta(years=+chunk_previous)
      elif (chunk_unit == "day"):
          date = date + datetime.timedelta(days=+chunk)
          previous_date = previous_date + \
              datetime.timedelta(days=+chunk_previous)
      elif (chunk_unit == "hour"):
          date = date + datetime.timedelta(days=+int(chunk / 24))
          previous_date = previous_date + \
              datetime.timedelta(days=+int(chunk_previous / 24))
  return _date_to_str_space(date2str(previous_date)), _date_to_str_space(date2str(date))

def _date_to_str_space(date_str):
  if (len(date_str) == 8):
      return str(date_str[0:4] + " " + date_str[4:6] + " " + date_str[6:])
  else:
      return ""

def get_average_total_time(jobs):
  # type: (List[object]) -> float
  """ Job has attribute total_time (See JobFactory)"""
  if len(jobs):
    average = sum(job.total_time for job in jobs)/ len(jobs)
    return round(average, 4)
  return 0.0

def parse_version_number(str_version):
  # type : (str) -> Tuple[int, int]
  if len(str_version.strip()) > 0:
    version_split = str_version.split('.')
    main = int(version_split[0])
    secondary = int(version_split[1])
    return (main, secondary)
  return (0, 0)

def is_version_historical_ready(str_version):
  main, secondary = parse_version_number(str_version)
  if (main >= 3 and secondary >= 13) or (main >= 4): # 3.13 onwards.
    return True
  return False

def get_current_timestamp():
  # type: () -> int
  return int(time.time())