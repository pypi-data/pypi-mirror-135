from typing import List, Optional
from dataclasses import dataclass
from enum import EnumMeta


class DataType(EnumMeta):
    Text = "Text"
    Integer = "Integer"
    RealNumber = "RealNumber"
    Boolean = "Boolean"
    Spacial = "Spacial"
    Binary = "Binary"
    Timestamp = "Timestamp"
    DateTime = "DateTime"
    Complex = "Complex"
    Unknown = "Unknown"


@dataclass
class SchemaColumn:
    name: Optional[str] = None
    description: Optional[str] = None
    dataType: Optional[DataType] = None
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    isUnique: Optional[bool] = None
    default: Optional[str] = None
    nullable: Optional[bool] = None


@dataclass
class DataResourceSchema:
    type: str
    name: str
    description: str
    fileFormat: str
    columns: Optional[List[SchemaColumn]] = None
