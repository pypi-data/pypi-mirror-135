import networkx as nx
from typing import List

from ascend.sdk.definitions import Component, Dataflow


def dataflows_ordered_by_dependency(data_service_id: str, dataflows: List[Dataflow]) -> List[Dataflow]:
  g = nx.DiGraph()
  for dataflow in dataflows:
    g.add_node(dataflow.id)
    for data_feed_connector in dataflow.data_feed_connectors:
      if data_feed_connector.input_data_service_id == data_service_id:
        g.add_edge(dataflow.id, data_feed_connector.input_dataflow_id)

  id_to_dataflow = {dataflow.id: dataflow for dataflow in dataflows}
  return [id_to_dataflow[df_id] for df_id in reversed(list(nx.topological_sort(g)))]