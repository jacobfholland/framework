from database.model import Model
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey

permission_group = Table(
    'permission_group', Model.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('permission_id', Integer,
           ForeignKey('permission.id'))
)
