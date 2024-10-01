"""
https://github.com/baeda-polito/portable-app-framework/blob/main/src/portable_app_framework/utils/util_qualify.py
"""

import os
from rdflib import Graph
import pyshacl
from logging import getLogger

logger = getLogger(__name__)


class BasicValidationInterface:
    """
    This class is used to validate a graph using the Brick basic validation as described here:
    https://github.com/gtfierro/shapes/blob/main/verify.py
    """

    def __init__(self, graph: Graph):
        # use the wrapper BrickGraph to initialize the graph
        self.graph = graph
        self.graph.parse(os.path.join(os.path.dirname(__file__), "..", "libraries", "Brick-nightly.ttl"), format='ttl')

    def validate(self) -> bool:
        """
        Validate the graph
        :return: print the validation report
        """
        # validate
        valid, results_graph, report = pyshacl.validate(self.graph,
                                                        shacl_graph=self.graph,
                                                        ont_graph=self.graph,
                                                        inference='rdfs',
                                                        abort_on_first=False,
                                                        allow_infos=False,
                                                        allow_warnings=False,
                                                        meta_shacl=False,
                                                        advanced=False,
                                                        js=False,
                                                        debug=False)

        logger.debug(f"[Brick] Is valid? {valid}")
        if not valid:
            print("-" * 79)
            print(report)
            print("-" * 79)

        return valid