from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from core.model import Model


class EmptyModel(Model):
    def __init__(self, args):
        super(EmptyModel, self).__init__(args)

        self._reset()

    def _init_weights(self):
        pass

    def print_model(self):
        self.logger.warning("<-----------------------------------> Model")
        self.logger.warning(self)

    def _reset(self):  # NOTE: should be called at each child's __init__
        self._init_weights()
        self.type(self.dtype)  # put on gpu if possible
        self.print_model()

    def forward(self, input):
        pass
