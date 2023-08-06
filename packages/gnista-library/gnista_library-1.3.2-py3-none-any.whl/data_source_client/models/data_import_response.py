import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.data_import_task_config import DataImportTaskConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataImportResponse")


@attr.s(auto_attribs=True)
class DataImportResponse:
    """ """

    data_import_id: str
    data_source_id: str
    created: datetime.datetime
    status: Union[Unset, None, str] = UNSET
    error_details: Union[Unset, None, str] = UNSET
    task_config: Union[Unset, None, DataImportTaskConfig] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        data_import_id = self.data_import_id
        data_source_id = self.data_source_id
        created = self.created.isoformat()

        status = self.status
        error_details = self.error_details
        task_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.task_config, Unset):
            task_config = self.task_config.to_dict() if self.task_config else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dataImportId": data_import_id,
                "dataSourceId": data_source_id,
                "created": created,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if error_details is not UNSET:
            field_dict["errorDetails"] = error_details
        if task_config is not UNSET:
            field_dict["taskConfig"] = task_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_import_id = d.pop("dataImportId")

        data_source_id = d.pop("dataSourceId")

        created = isoparse(d.pop("created"))

        status = d.pop("status", UNSET)

        error_details = d.pop("errorDetails", UNSET)

        _task_config = d.pop("taskConfig", UNSET)
        task_config: Union[Unset, None, DataImportTaskConfig]
        if _task_config is None:
            task_config = None
        elif isinstance(_task_config, Unset):
            task_config = UNSET
        else:
            task_config = DataImportTaskConfig.from_dict(_task_config)

        data_import_response = cls(
            data_import_id=data_import_id,
            data_source_id=data_source_id,
            created=created,
            status=status,
            error_details=error_details,
            task_config=task_config,
        )

        return data_import_response
