#!/usr/bin/env python
import os
from autosubmitAPIwu.config.basicConfig import BasicConfig
from autosubmitAPIwu.components.jobs.job_factory import SimJob, Job
from autosubmitAPIwu.config.config_common import AutosubmitConfig
from bscearth.utils.config_parser import ConfigParserFactory
from autosubmitAPIwu.job.job_utils import datechunk_to_year
from abc import ABCMeta, abstractmethod
from autosubmitAPIwu.common.utils import JobSection, parse_number_processors
from typing import List

class ConfigurationFacade:
  """ """
  __metaclass__ = ABCMeta
  
  def __init__(self, expid):
    self.basic_configuration = BasicConfig # type: BasicConfig
    self.basic_configuration.read()
    self.configuration_parser = ConfigParserFactory
    self.expid = expid # type: str    
    self.pkl_path = "" # type: str
    self.tmp_path = "" # type: str
    self.log_path = "" # type: str
    self.structures_path = "" # type: str
    self.chunk_unit = "" # type: str
    self.chunk_size = "" # type: int
    self.current_years_per_sim = 0.0 # type: float
    self.sim_processors = 0  # type: int
    self.warnings = [] # type: List[str] 
    self._process_basic_config()

  def _process_basic_config(self):
    # type: () -> None
    pkl_filename = "job_list_{0}.pkl".format(self.expid)    
    self.pkl_path = os.path.join(self.basic_configuration.LOCAL_ROOT_DIR, self.expid, "pkl", pkl_filename)
    self.tmp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, self.expid, BasicConfig.LOCAL_TMP_DIR)
    self.log_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, self.expid, "tmp", "LOG_{0}".format(self.expid))
    self.structures_path = BasicConfig.STRUCTURES_DIR
    if not os.path.exists(self.pkl_path): raise Exception("Required file {0} not found.".format(self.pkl_path))
    if not os.path.exists(self.tmp_path): raise Exception("Required folder {0} not found.".format(self.tmp_path))
      
  @abstractmethod
  def _process_advanced_config(self):
    """ """

class BasicConfigurationFacade(ConfigurationFacade):
  """ BasicConfig and paths """
  def __init__(self, expid):
    # type : (str) -> None
    super(BasicConfigurationFacade, self).__init__(expid)
  


class AutosubmitConfigurationFacade(ConfigurationFacade):
  """ Autosubmit Configuration includes Basic Config """
  def __init__(self, expid):
    # type: (str) -> None
    super(AutosubmitConfigurationFacade, self).__init__(expid)
    self._process_advanced_config()
  
  def _process_advanced_config(self):
    """ Advanced Configuration from AutosubmitConfig """
    # type: () -> None
    self.autosubmit_conf = AutosubmitConfig(self.expid, BasicConfig, ConfigParserFactory())    
    self.autosubmit_conf.reload()    
    self.chunk_unit = self.autosubmit_conf.get_chunk_size_unit()
    self.chunk_size = self.autosubmit_conf.get_chunk_size()    
    self.current_years_per_sim = datechunk_to_year(self.chunk_unit, self.chunk_size)    
    self.sim_processors = self._get_processors_number(self.autosubmit_conf.get_processors(JobSection.SIM))
  
  def get_main_platform(self):
    return str(self.autosubmit_conf.get_platform())

  def get_section_processors(self, section_name):
    return self._get_processors_number(str(self.autosubmit_conf.get_processors(section_name)))
  
  def get_section_qos(self, section_name):
    return str(self.autosubmit_conf.get_queue(section_name))

  def get_section_platform(self, section_name):
    return str(self.autosubmit_conf.get_job_platform(section_name))

  def get_platform_qos(self, platform_name):
    return str(self.autosubmit_conf.get_platform_queue(platform_name))

  def get_wrapper_qos(self):
    return str(self.autosubmit_conf.get_wrapper_queue())

  def get_section_wallclock(self, section_name):
    return str(self.autosubmit_conf.get_wallclock(section_name))
  
  def get_platform_max_wallclock(self, platform_name):
    return str(self.autosubmit_conf.get_platform_wallclock(platform_name))

  def update_sim_jobs(self, sim_jobs):
    # type: (List[SimJob]) -> None
    """ Update the jobs with the latest configuration values: Processors, years per sim """        
    for job in sim_jobs:
      job.set_ncpus(self.sim_processors)
      job.set_years_per_sim(self.current_years_per_sim)      
  
  def _get_processors_number(self, conf_sim_processors):
    # type: (str) -> int
    num_processors = 0
    try:
        if str(conf_sim_processors).find(":") >= 0:            
            num_processors = parse_number_processors(conf_sim_processors)
            self._add_warning("Parallelization parsing | {0} was interpreted as {1} cores.".format(
                conf_sim_processors, num_processors))
        else:
            num_processors = int(conf_sim_processors)
    except:        
        self._add_warning(
            "CHSY Critical | Autosubmit API could not parse the number of processors for the SIM job.")
        pass        
    return num_processors
  
  def _add_warning(self, message):
    # type: (str) -> None
    self.warnings.append(message)
  



    





