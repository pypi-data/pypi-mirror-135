from typing import ClassVar

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process import anonymous_traversal

from graphdb.interface.connection_iface import GraphDbConnectionInterface


class GraphDbConnection(GraphDbConnectionInterface):

    def __init__(
            self,
            connection_uri: str,
    ):
        self.connection_uri = connection_uri
        self.driver = anonymous_traversal.traversal().withRemote(DriverRemoteConnection(connection_uri, "g"))

    def get_connection(
            self,
    ) -> DriverRemoteConnection:
        """Get aws neptune connection object
        :return: object aws neptune driver connection
        """
        return self.driver

    @classmethod
    def from_uri(
            cls,
            connection_uri: str,
    ) -> ClassVar:
        """Create object connection from connection uri only
        :param connection_uri: string connection uru
        :return: current object class
        """
        return cls(connection_uri)
