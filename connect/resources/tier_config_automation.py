# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta
import logging

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import function_log
from connect.models.activation_template_response import ActivationTemplateResponse
from connect.models.activation_tile_response import ActivationTileResponse
from connect.models.param import Param
from connect.models.tier_config_request import TierConfigRequest
from .automation_engine import AutomationEngine


class TierConfigAutomation(AutomationEngine):
    """ This is the automation engine for the Tier Config Request API.  If you want to process
    Tier Config requests, subclass this and implement the ``process_request`` method,
    which receives a :py:class:`connect.models.TierConfigRequest` request as argument and must
    return an :py:class:`connect.models.ActivationTemplateResponse` or
    :py:class:`connect.models.ActivationTileResponse` object in case the request has to be approved.

    In other case, you must raise one of these exceptions:

    - :py:class:`connect.exceptions.InquireRequest`: Inquire for more information.
    - :py:class:`connect.exceptions.FailRequest`: Causes the request to fail.
    - :py:class:`connect.exceptions.SkipRequest`: Skips processing the request.

    Create an instance of your subclass and call its ``process`` method to begin processing.

    For an example on how to use this class, see :ref:`tier_config_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'tier/config-requests'
    model_class = TierConfigRequest
    logger = logging.getLogger('Tier.logger')

    def filters(self, status='pending', **kwargs):
        """ Returns the default set of filters for Tier Config request, plus any others that you
        might specify. The allowed filters are:

        - type
        - status
        - id
        - configuration__id
        - configuration__tier_level
        - configuration__account__id
        - configuration__product__id
        - assignee__id
        - unassigned (bool)
        - configuration__account__external_uid

        :param str status: Status of the requests. Default: ``'pending'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        filters = super(TierConfigAutomation, self).filters(status=status, **kwargs)
        if self.config.products:
            filters['configuration__product__id'] = ','.join(self.config.products)
        return filters

    @function_log(custom_logger=logger)
    def dispatch(self, request):
        # type: (TierConfigRequest) -> str
        try:
            self._set_custom_logger(request.id, request.configuration.id,
                                    request.configuration.account.id)

            if self.config.products \
                    and request.configuration.product.id not in self.config.products:
                return 'Invalid product'

            self.logger.info(
                'Start tier config request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                self.logger.info('Method `process_request` did not return result')
                return ''

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'template': {'representation': result.tile}}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template': {'id': result.template_id}}

            self.approve(request.id, params)

        except InquireRequest as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FailRequest as fail:
            return self.fail(request.id, reason=str(fail))

        except SkipRequest as skip:
            return skip.code

        except NotImplementedError:
            raise

        except Exception as ex:
            self.logger.warning('Skipping request {} because an exception was raised: {}'
                                .format(request.id, ex))
            return ''

        return ''

    @function_log(custom_logger=logger)
    def update_parameters(self, pk, params):
        """ Sends a list of Param objects to Connect for updating.

        :param str pk: Id of the request.
        :param list[Param] params: List of parameters to update.
        :return: The server response.
        :rtype: str
        """
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self._api.put(
            path=pk,
            json={'params': list_dict},
        )[0]
