from typing import Any

from gdsclient.model.trained_model import TrainedModel

from ..graph.graph_object import Graph
from ..query_runner.query_runner import QueryResult


class NCPredictionPipeline(TrainedModel):
    def _query_prefix(self) -> str:
        return "CALL gds.alpha.ml.pipeline.nodeClassification.predict."

    def predict_write(self, G: Graph, **config: Any) -> QueryResult:
        query = f"{self._query_prefix()}write($graph_name, $config)"
        config["modelName"] = self.name()
        params = {"graph_name": G.name(), "config": config}

        return self._query_runner.run_query(query, params)
