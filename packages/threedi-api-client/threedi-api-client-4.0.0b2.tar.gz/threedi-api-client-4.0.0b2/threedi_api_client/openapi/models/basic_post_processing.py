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

class BasicPostProcessing(object):
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
        'simulation': 'str',
        'scenario_name': 'str',
        'process_basic_results': 'bool',
        'result_uuid': 'str'
    }

    attribute_map = {
        'simulation': 'simulation',
        'scenario_name': 'scenario_name',
        'process_basic_results': 'process_basic_results',
        'result_uuid': 'result_uuid'
    }

    def __init__(self, simulation=None, scenario_name=None, process_basic_results=None, result_uuid=None, local_vars_configuration=None):  # noqa: E501
        """BasicPostProcessing - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._simulation = None
        self._scenario_name = None
        self._process_basic_results = None
        self._result_uuid = None
        self.discriminator = None

        if simulation is not None:
            self.simulation = simulation
        if scenario_name is not None:
            self.scenario_name = scenario_name
        if process_basic_results is not None:
            self.process_basic_results = process_basic_results
        if result_uuid is not None:
            self.result_uuid = result_uuid

    @property
    def simulation(self):
        """Gets the simulation of this BasicPostProcessing.  # noqa: E501


        :return: The simulation of this BasicPostProcessing.  # noqa: E501
        :rtype: str
        """
        return self._simulation

    @simulation.setter
    def simulation(self, simulation):
        """Sets the simulation of this BasicPostProcessing.


        :param simulation: The simulation of this BasicPostProcessing.  # noqa: E501
        :type: str
        """

        self._simulation = simulation

    @property
    def scenario_name(self):
        """Gets the scenario_name of this BasicPostProcessing.  # noqa: E501

        Scenario name for saving the results  # noqa: E501

        :return: The scenario_name of this BasicPostProcessing.  # noqa: E501
        :rtype: str
        """
        return self._scenario_name

    @scenario_name.setter
    def scenario_name(self, scenario_name):
        """Sets the scenario_name of this BasicPostProcessing.

        Scenario name for saving the results  # noqa: E501

        :param scenario_name: The scenario_name of this BasicPostProcessing.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                scenario_name is not None and len(scenario_name) > 128):
            raise ValueError("Invalid value for `scenario_name`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scenario_name is not None and len(scenario_name) < 1):
            raise ValueError("Invalid value for `scenario_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._scenario_name = scenario_name

    @property
    def process_basic_results(self):
        """Gets the process_basic_results of this BasicPostProcessing.  # noqa: E501


        :return: The process_basic_results of this BasicPostProcessing.  # noqa: E501
        :rtype: bool
        """
        return self._process_basic_results

    @process_basic_results.setter
    def process_basic_results(self, process_basic_results):
        """Sets the process_basic_results of this BasicPostProcessing.


        :param process_basic_results: The process_basic_results of this BasicPostProcessing.  # noqa: E501
        :type: bool
        """

        self._process_basic_results = process_basic_results

    @property
    def result_uuid(self):
        """Gets the result_uuid of this BasicPostProcessing.  # noqa: E501


        :return: The result_uuid of this BasicPostProcessing.  # noqa: E501
        :rtype: str
        """
        return self._result_uuid

    @result_uuid.setter
    def result_uuid(self, result_uuid):
        """Sets the result_uuid of this BasicPostProcessing.


        :param result_uuid: The result_uuid of this BasicPostProcessing.  # noqa: E501
        :type: str
        """

        self._result_uuid = result_uuid

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
        if not isinstance(other, BasicPostProcessing):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BasicPostProcessing):
            return True

        return self.to_dict() != other.to_dict()
