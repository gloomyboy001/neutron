# Copyright 2015 HuaWei Technologies.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron.db import db_base_plugin_v2
from neutron.db import models_v2
from neutron.db import standard_attr
from neutron.objects import base as base_obj
from neutron.services import service_base
from neutron.services.timestamp import timestamp_db as ts_db


class TimeStampPlugin(service_base.ServicePluginBase,
                      ts_db.TimeStamp_db_mixin):
    """Implements Neutron Timestamp Service plugin."""

    supported_extension_aliases = ['standard-attr-timestamp']

    def __init__(self):
        super(TimeStampPlugin, self).__init__()
        self.register_db_events()
        rs_model_maps = standard_attr.get_standard_attr_resource_model_map()
        for rsmap, model in rs_model_maps.items():
            db_base_plugin_v2.NeutronDbPluginV2.register_dict_extend_funcs(
                rsmap, [self.extend_resource_dict_timestamp])
            db_base_plugin_v2.NeutronDbPluginV2.register_model_query_hook(
                model, "change_since_query", None, None,
                self._change_since_result_filter_hook)
        # TODO(jlibosva): Move this to register_model_query_hook
        base_obj.register_filter_hook_on_model(
            models_v2.SubnetPool, ts_db.CHANGED_SINCE)

    @classmethod
    def get_plugin_type(cls):
        return 'timestamp'

    def get_plugin_description(self):
        return "Adds timestamps to Neutron resources with standard attributes"
