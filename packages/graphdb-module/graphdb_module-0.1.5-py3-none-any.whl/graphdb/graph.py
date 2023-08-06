from typing import ClassVar, List, Dict, Any

from gremlin_python.process.graph_traversal import __
from pandas import DataFrame

from graphdb.connection.graph_connection import GraphDbConnection
from graphdb.interface.node_create_constraint_iface import NodeCreateConstraintInterface
from graphdb.interface.node_create_iface import NodeCreateInterface
from graphdb.interface.node_create_index_iface import NodeCreateIndexInterface
from graphdb.interface.node_dataframe_iface import NodeDataframeInterface
from graphdb.interface.node_delete_iface import NodeDeleteInterface
from graphdb.interface.node_search_iface import NodeSearchInterface
from graphdb.interface.node_update_iface import NodeUpdateInterface
from graphdb.interface.rel_create_iface import RelationshipCreateInterface
from graphdb.interface.rel_delete_iface import RelationshipDeleteInterface
from graphdb.schema import Node, Relationship
from graphdb.utils import log_execution_time


class GraphDb(NodeCreateInterface, NodeSearchInterface, NodeUpdateInterface, NodeDeleteInterface,
              RelationshipCreateInterface, RelationshipDeleteInterface,
              NodeCreateConstraintInterface,
              NodeCreateIndexInterface,
              NodeDataframeInterface):
    """This will inherit to child class
    and sure you can create another method to support your application"""

    def __init__(
            self,
            connection: GraphDbConnection,
            path_data: str = None
    ):
        self.connection = connection
        self.path_data = path_data
        NodeCreateInterface.__init__(self)
        NodeSearchInterface.__init__(self)
        NodeUpdateInterface.__init__(self)
        NodeDeleteInterface.__init__(self)
        RelationshipCreateInterface.__init__(self)
        RelationshipDeleteInterface.__init__(self)
        NodeCreateConstraintInterface.__init__(self)
        NodeCreateIndexInterface.__init__(self)

    @classmethod
    def from_connection(
            cls,
            connection: GraphDbConnection,
    ) -> ClassVar:
        """Create class object from object connection class
        :param connection: string connection uru
        :return: current object class
        """
        return cls(connection)

    @log_execution_time
    def load_from_csv(
            self,
            path_data: str
    ) -> DataFrame:
        """Load data into dataframe from csv file
        :param path_data: string path data where it is stores
        :return: none
        """
        raise NotImplementedError

    @log_execution_time
    def create_index(
            self,
            node: Node,
            index_name: str,
    ) -> bool:
        """Create new constraint based on specified properties
        :param node: object node
        :param index_name: string index name
        :return: boolean true or false
        """
        raise NotImplementedError

    @log_execution_time
    def create_constraint(
            self,
            node: Node,
            properties: List[str],
            is_unique: bool = False,
            not_null: bool = False,
    ) -> bool:
        """Create new constraint based on specified properties
        :param node: object node
        :param properties: list of property
        :param is_unique: is constraint is unique
        :param not_null: is constraint is not null
        :return: boolean true or false
        """
        raise NotImplementedError

    @log_execution_time
    def find_node(
            self,
            node: Node,
            limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Find node with specified parameters
        :param node: object node
        :param limit: default limit query
        :return: list of dictionary
        """
        s = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                s.property(k, v)

        s_node = self.connection.driver.V(s.toList())
        return [{prop.label: prop.value} for prop in s_node.properties()]

    @log_execution_time
    def create_node(
            self,
            node: Node
    ) -> bool:
        """Create new node with label and properties if set in node class
        it will search node, if exists then update that node only
        :param node: object node
        :return: boolean
        """
        s = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                s.property(k, v)

        s_node = s.toList()
        if len(s_node) == 0:
            n_node = self.connection.driver.addV(node.label)
            for k, v in node.properties.items():
                n_node.property(k, v)
            n_node.iterate()

        return True

    @log_execution_time
    def create_multi_node(
            self,
            nodes: List[Node]
    ) -> List[bool]:
        """Create multiple node with label and properties if set in node class,
        this will doing upsert value
        :param nodes: list of object node
        :return: list of boolean
        """
        return list(map(self.create_node, nodes))

    @log_execution_time
    def update_node_property(
            self,
            node: Node,
            update_query: Dict[str, Any]
    ) -> bool:
        """Update node with specified properties
        :param node: object class node
        :param update_query: dictionary filter query
        :return: boolean
        """
        s = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                s.property(k, v)

        for k, v in update_query.items():
            s.property(k, v)

        s.iterate()
        return True

    @log_execution_time
    def replace_node_property(
            self,
            node: Node,
            update_query: Dict[str, Any]
    ) -> bool:
        """Replace node properties with new properties
        :param node: object class node
        :param update_query: dictionary filter query
        :return: boolean
        """
        node_id = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                node_id.property(k, v)

        # get node id
        node_id = node_id.next().id
        # remove properties
        self.connection.driver.V(node_id).properties().drop().iterate()

        # assign new property
        new_prop = self.connection.driver.V(node_id)
        for k, v in update_query.items():
            new_prop.property(k, v)

        new_prop.iterate()
        return True

    @log_execution_time
    def remove_node_property(
            self,
            node: Node,
            properties: List[str]
    ) -> bool:
        """Remove specified property from node
        :param node: object node
        :param properties: list of property you want to remove from this node
        :return: boolean
        """
        s = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                s.property(k, v)

        s.properties(*properties).drop().iterate()
        return True

    @log_execution_time
    def remove_all_node_property(
            self,
            node: Node
    ) -> bool:
        """Remove all property from this node
        :param node: object node
        :return: boolean
        """
        s = self.connection.driver.V().hasLabel(node.label)
        if node.properties:
            for k, v in node.properties.items():
                s.property(k, v)

        s.properties().drop().iterate()
        return True

    @log_execution_time
    def delete_node_with_relationship(
            self,
            node: Node
    ) -> bool:
        """Delete for specified node object, please note this will remove node with all relationship on it
        :param node: object node that we want to delete
        :return: bool
        """
        return self.delete_node(node)

    @log_execution_time
    def delete_node(
            self,
            node: Node
    ) -> bool:
        """Delete for specified node object, it will leave relationship as it is
        :param node: object node that we want to delete
        :return: bool
        """
        s = self.connection.driver.V().hasLabel(node.label)
        for k, v in node.properties.items():
            s.property(k, v)
        s.drop().iterate()
        return True

    @log_execution_time
    def create_relationship(
            self,
            node_from: Node,
            node_to: Node,
            rel: Relationship
    ) -> bool:
        """Create new relationship between 2 nodes
        :param node_from: object node from
        :param node_to: object node to
        :param rel: object relationship with name
        :return: boolean
        """
        # get node from id
        f = self.connection.driver.V().hasLabel(node_from.label)
        if node_from.properties:
            for k, v in node_from.properties.items():
                f.property(k, v)
        n_f = f.next().id

        # get node to id
        t = self.connection.driver.V().hasLabel(node_to.label)
        if node_to.properties:
            for k, v in node_to.properties.items():
                t.property(k, v)
        n_t = t.next().id

        # create new edge between vertex
        self.connection.driver.V(n_f).addE(rel.relationship_name).to(__.V(n_t)).next()
        return True

    @log_execution_time
    def delete_relationship(
            self,
            node_from: Node,
            node_to: Node,
            rel: Relationship
    ) -> bool:
        """ Delete only relationship from specified node
        :param node_from: object node from
        :param node_to: object node to
        :param rel: object relationship with name
        :return: boolean
        """
        # get node from id
        f = self.connection.driver.V().hasLabel(node_from.label)
        if node_from.properties:
            for k, v in node_from.properties.items():
                f.property(k, v)
        n_f = f.next().id

        # get node to id
        t = self.connection.driver.V().hasLabel(node_to.label)
        if node_to.properties:
            for k, v in node_to.properties.items():
                t.property(k, v)
        n_t = t.next().id

        self.connection.driver.V(n_f).outE(). \
            hasLabel(rel.relationship_name).where(__.V().hasId(n_t)).drop().iterate()
        return True
