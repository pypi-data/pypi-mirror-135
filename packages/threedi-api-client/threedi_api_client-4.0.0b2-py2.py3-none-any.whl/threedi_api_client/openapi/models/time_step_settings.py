# coding: utf-8

"""
    3Di API

    3Di simulation API (latest stable version: v3)   Framework release: 2.11.1   3Di core release: 2.2.3  deployed on:  02:06PM (UTC) on January 13, 2022  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: info@nelen-schuurmans.nl
    Generated by: https://openapi-generator.tech
"""


import logging
import pprint
import re  # noqa: F401

import six

from threedi_api_client.openapi.configuration import Configuration

logger = logging.getLogger(__name__)

class TimeStepSettings(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'int',
        'simulation_id': 'int',
        'time_step': 'float',
        'min_time_step': 'float',
        'max_time_step': 'float',
        'use_time_step_stretch': 'bool',
        'output_time_step': 'float'
    }

    attribute_map = {
        'id': 'id',
        'simulation_id': 'simulation_id',
        'time_step': 'time_step',
        'min_time_step': 'min_time_step',
        'max_time_step': 'max_time_step',
        'use_time_step_stretch': 'use_time_step_stretch',
        'output_time_step': 'output_time_step'
    }

    def __init__(self, id=None, simulation_id=None, time_step=None, min_time_step=None, max_time_step=None, use_time_step_stretch=None, output_time_step=None, local_vars_configuration=None):  # noqa: E501
        """TimeStepSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._simulation_id = None
        self._time_step = None
        self._min_time_step = None
        self._max_time_step = None
        self._use_time_step_stretch = None
        self._output_time_step = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if simulation_id is not None:
            self.simulation_id = simulation_id
        self.time_step = time_step
        self.min_time_step = min_time_step
        self.max_time_step = max_time_step
        self.use_time_step_stretch = use_time_step_stretch
        self.output_time_step = output_time_step

    @property
    def id(self):
        """Gets the id of this TimeStepSettings.  # noqa: E501


        :return: The id of this TimeStepSettings.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TimeStepSettings.


        :param id: The id of this TimeStepSettings.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def simulation_id(self):
        """Gets the simulation_id of this TimeStepSettings.  # noqa: E501


        :return: The simulation_id of this TimeStepSettings.  # noqa: E501
        :rtype: int
        """
        return self._simulation_id

    @simulation_id.setter
    def simulation_id(self, simulation_id):
        """Sets the simulation_id of this TimeStepSettings.


        :param simulation_id: The simulation_id of this TimeStepSettings.  # noqa: E501
        :type: int
        """

        self._simulation_id = simulation_id

    @property
    def time_step(self):
        """Gets the time_step of this TimeStepSettings.  # noqa: E501

        Size of the simulation time step in seconds.  # noqa: E501

        :return: The time_step of this TimeStepSettings.  # noqa: E501
        :rtype: float
        """
        return self._time_step

    @time_step.setter
    def time_step(self, time_step):
        """Sets the time_step of this TimeStepSettings.

        Size of the simulation time step in seconds.  # noqa: E501

        :param time_step: The time_step of this TimeStepSettings.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and time_step is None:  # noqa: E501
            raise ValueError("Invalid value for `time_step`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                time_step is not None and time_step < 1E-14):  # noqa: E501
            raise ValueError("Invalid value for `time_step`, must be a value greater than or equal to `1E-14`")  # noqa: E501

        self._time_step = time_step

    @property
    def min_time_step(self):
        """Gets the min_time_step of this TimeStepSettings.  # noqa: E501

        Minimum size of the simulation time step in seconds. Suitable default is 0.001.  # noqa: E501

        :return: The min_time_step of this TimeStepSettings.  # noqa: E501
        :rtype: float
        """
        return self._min_time_step

    @min_time_step.setter
    def min_time_step(self, min_time_step):
        """Sets the min_time_step of this TimeStepSettings.

        Minimum size of the simulation time step in seconds. Suitable default is 0.001.  # noqa: E501

        :param min_time_step: The min_time_step of this TimeStepSettings.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and min_time_step is None:  # noqa: E501
            raise ValueError("Invalid value for `min_time_step`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                min_time_step is not None and min_time_step < 1E-14):  # noqa: E501
            raise ValueError("Invalid value for `min_time_step`, must be a value greater than or equal to `1E-14`")  # noqa: E501

        self._min_time_step = min_time_step

    @property
    def max_time_step(self):
        """Gets the max_time_step of this TimeStepSettings.  # noqa: E501

        Only in combination with use_time_step_stretch=True.  # noqa: E501

        :return: The max_time_step of this TimeStepSettings.  # noqa: E501
        :rtype: float
        """
        return self._max_time_step

    @max_time_step.setter
    def max_time_step(self, max_time_step):
        """Sets the max_time_step of this TimeStepSettings.

        Only in combination with use_time_step_stretch=True.  # noqa: E501

        :param max_time_step: The max_time_step of this TimeStepSettings.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                max_time_step is not None and max_time_step < 1E-14):  # noqa: E501
            raise ValueError("Invalid value for `max_time_step`, must be a value greater than or equal to `1E-14`")  # noqa: E501

        self._max_time_step = max_time_step

    @property
    def use_time_step_stretch(self):
        """Gets the use_time_step_stretch of this TimeStepSettings.  # noqa: E501

        Permit the time step to increase automatically, when the flow allows it.  # noqa: E501

        :return: The use_time_step_stretch of this TimeStepSettings.  # noqa: E501
        :rtype: bool
        """
        return self._use_time_step_stretch

    @use_time_step_stretch.setter
    def use_time_step_stretch(self, use_time_step_stretch):
        """Sets the use_time_step_stretch of this TimeStepSettings.

        Permit the time step to increase automatically, when the flow allows it.  # noqa: E501

        :param use_time_step_stretch: The use_time_step_stretch of this TimeStepSettings.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and use_time_step_stretch is None:  # noqa: E501
            raise ValueError("Invalid value for `use_time_step_stretch`, must not be `None`")  # noqa: E501

        self._use_time_step_stretch = use_time_step_stretch

    @property
    def output_time_step(self):
        """Gets the output_time_step of this TimeStepSettings.  # noqa: E501

        The interval in seconds in which results are saved to disk.  # noqa: E501

        :return: The output_time_step of this TimeStepSettings.  # noqa: E501
        :rtype: float
        """
        return self._output_time_step

    @output_time_step.setter
    def output_time_step(self, output_time_step):
        """Sets the output_time_step of this TimeStepSettings.

        The interval in seconds in which results are saved to disk.  # noqa: E501

        :param output_time_step: The output_time_step of this TimeStepSettings.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and output_time_step is None:  # noqa: E501
            raise ValueError("Invalid value for `output_time_step`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                output_time_step is not None and output_time_step < 1E-14):  # noqa: E501
            raise ValueError("Invalid value for `output_time_step`, must be a value greater than or equal to `1E-14`")  # noqa: E501

        self._output_time_step = output_time_step

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TimeStepSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TimeStepSettings):
            return True

        return self.to_dict() != other.to_dict()
