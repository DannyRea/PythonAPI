from pydantic import BaseModel

from starlette.routing import Route

from sql_app.database import Base


class Publish(BaseModel):
    channel: str
    message: str


def setupChannels(app):
    for route in app.routes:
        print(route)


# for table_name in Base.metadata.tables.keys():
