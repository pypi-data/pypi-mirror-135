#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Optional

from pyhive import hive  # noqa: F401
from pyhive.sqlalchemy_hive import HiveDate, HiveDecimal, HiveTimestamp

from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.ingestion.source.sql_source import SQLConnectionConfig, SQLSource
from metadata.utils.column_helpers import register_custom_type

register_custom_type(HiveDate, "DATE")
register_custom_type(HiveTimestamp, "TIME")
register_custom_type(HiveDecimal, "NUMBER")


class HiveConfig(SQLConnectionConfig):
    scheme = "hive"
    auth_options: Optional[str] = None
    service_type = "Hive"

    def get_connection_url(self):
        url = super().get_connection_url()
        if self.auth_options is not None:
            return f"{url};{self.auth_options}"
        else:
            return url


class HiveSource(SQLSource):
    def __init__(self, config, metadata_config, ctx):
        super().__init__(config, metadata_config, ctx)

    @classmethod
    def create(cls, config_dict, metadata_config_dict, ctx):
        config = HiveConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)
