import database
from app.log.logger import create_logger
from app.utils.printable import Printable
from sqlalchemy import or_, and_

from database.utils import select_func

logger = create_logger(__name__)


class Query(Printable):
    def __init__(self, filter, func=and_) -> None:
        self.func = select_func(func)
        self.filter = filter
        self.results = database.session.query(
            self.filter.cls).filter(func(*self.filter.conditions))
