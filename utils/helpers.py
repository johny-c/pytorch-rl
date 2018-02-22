from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from collections import namedtuple

import cv2
import numpy as np


def loggerConfig(log_file, verbose=2):
    logger = logging.getLogger()
    formatter = logging.Formatter('[%(levelname)-8s] (%(processName)-11s) %(message)s')
    fileHandler = logging.FileHandler(log_file, 'w')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    if verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif verbose >= 1:
        logger.setLevel(logging.INFO)
    else:
        # NOTE: we currently use this level to log to get rid of visdom's info printouts
        logger.setLevel(logging.WARNING)
    return logger


# This is to be understood as a transition: Given `state0`, performing `action`
# yields `reward` and results in `state1`, which might be `terminal`.
# NOTE: used as the return format for Env(), and as the format to push into replay memory for off-policy methods (DQN)
# NOTE: when return from Env(), state0 is always None
Experience = namedtuple('Experience', 'state0, action, reward, state1, terminal1')
# NOTE: used for on-policy methods for collect experiences over a rollout of an episode
# NOTE: policy_vb & value0_vb for storing output Variables along a rollout # NOTE: they should not be detached from the graph!
A3C_Experience = namedtuple('A3C_Experience',
                            'state0, action, reward, state1, terminal1, policy_vb, sigmoid_vb, value0_vb')
ACER_On_Policy_Experience = namedtuple('ACER_On_Policy_Experience',
                                       'state0, action, reward, state1, terminal1, policy_vb, q0_vb,      value0_vb, detached_avg_policy_vb, detached_old_policy_vb')
# # NOTE: used as the format to push into the replay memory for ACER; when sampled, used to get ACER_On_Policy_Experience
ACER_Off_Policy_Experience = namedtuple('ACER_Off_Policy_Experience',
                                        'state0, action, reward,                                                                              detached_old_policy_vb')


def preprocessAtari(frame):
    frame = frame[34:34 + 160, :160]
    frame = cv2.resize(frame, (80, 80))
    frame = cv2.resize(frame, (42, 42))
    frame = frame.mean(2)
    frame = frame.astype(np.float32)
    frame *= (1. / 255.)
    return frame


# TODO: check the order rgb to confirm
def rgb2gray(rgb):
    gray_image = 0.2126 * rgb[..., 0]
    gray_image[:] += 0.0722 * rgb[..., 1]
    gray_image[:] += 0.7152 * rgb[..., 2]
    return gray_image


# TODO: check the order rgb to confirm
def rgb2y(rgb):
    y_image = 0.299 * rgb[..., 0]
    y_image[:] += 0.587 * rgb[..., 1]
    y_image[:] += 0.114 * rgb[..., 2]
    return y_image


def scale(image, hei_image, wid_image):
    return cv2.resize(image, (wid_image, hei_image),
                      interpolation=cv2.INTER_LINEAR)


def one_hot(n_classes, labels):
    one_hot_labels = np.zeros(labels.shape + (n_classes,))
    for c in range(n_classes):
        one_hot_labels[labels == c, c] = 1
    return one_hot_labels
