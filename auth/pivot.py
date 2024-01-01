from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from database.base import Base

print("PIVOT")
permission_group = Table(
    'permission_group', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('permission_id', Integer,
           ForeignKey('permission.id'))
)
