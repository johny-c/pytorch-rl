from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from core.env import Env


class LabEnv(Env):
    def __init__(self, args, env_ind=0):
        super(LabEnv, self).__init__(args, env_ind)

        assert self.env_type == "lab"
