#!/usr/bin/env python

import unittest
from autosubmitAPIwu.components.representations.tree import TreeRepresentation
from autosubmitAPIwu.job.job_common import Status

class TestTreeRepresentation(unittest.TestCase):
  def setUp(self):
      pass
      
  def tearDown(self):
      pass
  
  # def test_load(self):    
  #   tree = TreeRepresentation("a3zk") 
  #   tree.setup()
  #   tree._distribute_into_date_member_groups()
  #   for key, jobs in tree._date_member_distribution.items():
  #     print(key)
  #     for job in jobs:
  #       print(job.name)
  #       print(job.do_print())
  #   print("Others:")
  #   for job in tree._no_date_no_member_jobs:
  #     print(job.name)
    

  # def test_gen_dm_folders(self):
  #   tree = TreeRepresentation("a29z") 
  #   tree.setup()
  #   tree._distribute_into_date_member_groups()
    # tree._distribute_into_date_member_groups()
  
  def test_generate_complete(self):
    tree = TreeRepresentation("a29z")
    tree.setup()
    tree.perform_calculations()              
    for job in tree.joblist_loader.jobs:      
      if job.status == Status.COMPLETED:
        self.assertTrue(job.out_path_local.startswith("/esarchive/"))
        self.assertTrue(job.err_path_local.startswith("/esarchive/"))
      #   print(job.out_path_local)
      #   print(job.err_path_local)
      # else:
      #   print(job.name)
    # self.assertTrue(self.test_graph.edge_count == edge_count)

if __name__ == '__main__':
  unittest.main()
  

