from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List
from enum import EnumMeta

from .data_resource_schema import DataResourceSchema


class TreeItemType(EnumMeta):
    Folder = "Folder"
    CsvFile = "CsvFile"
    ImageFile = "ImageFile"
    ExcelFile = "ExcelFile"
    TextFile = "TextFile"
    MdFile = "MdFile"
    DataSet = "DataSet"
    DataTable = "DataTable"
    File = "File"
    Notebook = "Notebook"


@dataclass
class TreeItem:
    name: str
    id: Optional[str] = None
    parentId: Optional[str] = None
    path: Optional[str] = None
    type: Optional[TreeItemType] = None
    isFolder: Optional[bool] = False
    children: Optional[List[TreeItem]] = None
    size: Optional[int] = 0
    uri: Optional[str] = None
    metadata: Optional[DataResourceSchema] = None
    digest: Optional[str] = None
    itemCreatedDate: Optional[str] = None
    itemUpdatedDate: Optional[str] = None
