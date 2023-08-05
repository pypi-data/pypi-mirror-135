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

class PostProcessingOverview(object):
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
        'username': 'str',
        'metadata_version': 'str',
        'start_time_sim': 'str',
        'end_time_sim': 'str',
        'results': 'Result',
        'settings': 'Settings',
        'model_name': 'str',
        'simulation_name': 'str',
        'scenario_name': 'str',
        'model_id': 'int',
        'model_revision_id': 'str',
        'email': 'str',
        'result_uuid': 'str',
        'organisation_uuid': 'str',
        'simulation': 'int'
    }

    attribute_map = {
        'username': 'username',
        'metadata_version': 'metadata_version',
        'start_time_sim': 'start_time_sim',
        'end_time_sim': 'end_time_sim',
        'results': 'results',
        'settings': 'settings',
        'model_name': 'model_name',
        'simulation_name': 'simulation_name',
        'scenario_name': 'scenario_name',
        'model_id': 'model_id',
        'model_revision_id': 'model_revision_id',
        'email': 'email',
        'result_uuid': 'result_uuid',
        'organisation_uuid': 'organisation_uuid',
        'simulation': 'simulation'
    }

    def __init__(self, username=None, metadata_version='1.2', start_time_sim=None, end_time_sim=None, results=None, settings=None, model_name=None, simulation_name=None, scenario_name=None, model_id=None, model_revision_id=None, email=None, result_uuid=None, organisation_uuid=None, simulation=None, local_vars_configuration=None):  # noqa: E501
        """PostProcessingOverview - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._username = None
        self._metadata_version = None
        self._start_time_sim = None
        self._end_time_sim = None
        self._results = None
        self._settings = None
        self._model_name = None
        self._simulation_name = None
        self._scenario_name = None
        self._model_id = None
        self._model_revision_id = None
        self._email = None
        self._result_uuid = None
        self._organisation_uuid = None
        self._simulation = None
        self.discriminator = None

        if username is not None:
            self.username = username
        if metadata_version is not None:
            self.metadata_version = metadata_version
        if start_time_sim is not None:
            self.start_time_sim = start_time_sim
        if end_time_sim is not None:
            self.end_time_sim = end_time_sim
        self.results = results
        self.settings = settings
        if model_name is not None:
            self.model_name = model_name
        if simulation_name is not None:
            self.simulation_name = simulation_name
        if scenario_name is not None:
            self.scenario_name = scenario_name
        if model_id is not None:
            self.model_id = model_id
        if model_revision_id is not None:
            self.model_revision_id = model_revision_id
        if email is not None:
            self.email = email
        if result_uuid is not None:
            self.result_uuid = result_uuid
        if organisation_uuid is not None:
            self.organisation_uuid = organisation_uuid
        if simulation is not None:
            self.simulation = simulation

    @property
    def username(self):
        """Gets the username of this PostProcessingOverview.  # noqa: E501


        :return: The username of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this PostProcessingOverview.


        :param username: The username of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def metadata_version(self):
        """Gets the metadata_version of this PostProcessingOverview.  # noqa: E501


        :return: The metadata_version of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._metadata_version

    @metadata_version.setter
    def metadata_version(self, metadata_version):
        """Sets the metadata_version of this PostProcessingOverview.


        :param metadata_version: The metadata_version of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._metadata_version = metadata_version

    @property
    def start_time_sim(self):
        """Gets the start_time_sim of this PostProcessingOverview.  # noqa: E501


        :return: The start_time_sim of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._start_time_sim

    @start_time_sim.setter
    def start_time_sim(self, start_time_sim):
        """Sets the start_time_sim of this PostProcessingOverview.


        :param start_time_sim: The start_time_sim of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._start_time_sim = start_time_sim

    @property
    def end_time_sim(self):
        """Gets the end_time_sim of this PostProcessingOverview.  # noqa: E501


        :return: The end_time_sim of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._end_time_sim

    @end_time_sim.setter
    def end_time_sim(self, end_time_sim):
        """Sets the end_time_sim of this PostProcessingOverview.


        :param end_time_sim: The end_time_sim of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._end_time_sim = end_time_sim

    @property
    def results(self):
        """Gets the results of this PostProcessingOverview.  # noqa: E501


        :return: The results of this PostProcessingOverview.  # noqa: E501
        :rtype: Result
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this PostProcessingOverview.


        :param results: The results of this PostProcessingOverview.  # noqa: E501
        :type: Result
        """
        if self.local_vars_configuration.client_side_validation and results is None:  # noqa: E501
            raise ValueError("Invalid value for `results`, must not be `None`")  # noqa: E501

        self._results = results

    @property
    def settings(self):
        """Gets the settings of this PostProcessingOverview.  # noqa: E501


        :return: The settings of this PostProcessingOverview.  # noqa: E501
        :rtype: Settings
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this PostProcessingOverview.


        :param settings: The settings of this PostProcessingOverview.  # noqa: E501
        :type: Settings
        """
        if self.local_vars_configuration.client_side_validation and settings is None:  # noqa: E501
            raise ValueError("Invalid value for `settings`, must not be `None`")  # noqa: E501

        self._settings = settings

    @property
    def model_name(self):
        """Gets the model_name of this PostProcessingOverview.  # noqa: E501


        :return: The model_name of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        """Sets the model_name of this PostProcessingOverview.


        :param model_name: The model_name of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._model_name = model_name

    @property
    def simulation_name(self):
        """Gets the simulation_name of this PostProcessingOverview.  # noqa: E501


        :return: The simulation_name of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._simulation_name

    @simulation_name.setter
    def simulation_name(self, simulation_name):
        """Sets the simulation_name of this PostProcessingOverview.


        :param simulation_name: The simulation_name of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._simulation_name = simulation_name

    @property
    def scenario_name(self):
        """Gets the scenario_name of this PostProcessingOverview.  # noqa: E501

        Scenario name for saving the results  # noqa: E501

        :return: The scenario_name of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._scenario_name

    @scenario_name.setter
    def scenario_name(self, scenario_name):
        """Sets the scenario_name of this PostProcessingOverview.

        Scenario name for saving the results  # noqa: E501

        :param scenario_name: The scenario_name of this PostProcessingOverview.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                scenario_name is not None and len(scenario_name) < 1):
            raise ValueError("Invalid value for `scenario_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._scenario_name = scenario_name

    @property
    def model_id(self):
        """Gets the model_id of this PostProcessingOverview.  # noqa: E501


        :return: The model_id of this PostProcessingOverview.  # noqa: E501
        :rtype: int
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this PostProcessingOverview.


        :param model_id: The model_id of this PostProcessingOverview.  # noqa: E501
        :type: int
        """

        self._model_id = model_id

    @property
    def model_revision_id(self):
        """Gets the model_revision_id of this PostProcessingOverview.  # noqa: E501


        :return: The model_revision_id of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._model_revision_id

    @model_revision_id.setter
    def model_revision_id(self, model_revision_id):
        """Sets the model_revision_id of this PostProcessingOverview.


        :param model_revision_id: The model_revision_id of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._model_revision_id = model_revision_id

    @property
    def email(self):
        """Gets the email of this PostProcessingOverview.  # noqa: E501


        :return: The email of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this PostProcessingOverview.


        :param email: The email of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def result_uuid(self):
        """Gets the result_uuid of this PostProcessingOverview.  # noqa: E501


        :return: The result_uuid of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._result_uuid

    @result_uuid.setter
    def result_uuid(self, result_uuid):
        """Sets the result_uuid of this PostProcessingOverview.


        :param result_uuid: The result_uuid of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._result_uuid = result_uuid

    @property
    def organisation_uuid(self):
        """Gets the organisation_uuid of this PostProcessingOverview.  # noqa: E501


        :return: The organisation_uuid of this PostProcessingOverview.  # noqa: E501
        :rtype: str
        """
        return self._organisation_uuid

    @organisation_uuid.setter
    def organisation_uuid(self, organisation_uuid):
        """Sets the organisation_uuid of this PostProcessingOverview.


        :param organisation_uuid: The organisation_uuid of this PostProcessingOverview.  # noqa: E501
        :type: str
        """

        self._organisation_uuid = organisation_uuid

    @property
    def simulation(self):
        """Gets the simulation of this PostProcessingOverview.  # noqa: E501


        :return: The simulation of this PostProcessingOverview.  # noqa: E501
        :rtype: int
        """
        return self._simulation

    @simulation.setter
    def simulation(self, simulation):
        """Sets the simulation of this PostProcessingOverview.


        :param simulation: The simulation of this PostProcessingOverview.  # noqa: E501
        :type: int
        """

        self._simulation = simulation

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
        if not isinstance(other, PostProcessingOverview):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PostProcessingOverview):
            return True

        return self.to_dict() != other.to_dict()
