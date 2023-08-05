from copy import deepcopy
from typing import Union, List, Callable, Optional
from ruleskit import RuleSet
from pathlib import Path
from transparentpath import TransparentPath
import logging
from multiprocessing import get_context, cpu_count
from concurrent.futures import ProcessPoolExecutor
from .node import Node, LearningConfig

logger = logging.getLogger(__name__)


class CentralServer:

    """Central server. Can create nodes, pass public_configs to them,
    launch their learning and gather their results."""

    # If True, calling 'fit' of each node is done in parallel.
    PARALLEL_NODES = False

    def __init__(
        self,
        public_configs_path: Union[str, Path, TransparentPath] = None,
        nodes: Union[List[Node], None] = None,
        nnodes: Union[None, int] = None,
        dataprep_method: Callable = None,
    ):
        """Must specify one of public_configs_path and nodes.

        If public_configs_path, will create nnodes using the given learning configurations
        Else, if nodes is passed, assumes that they are compatible and will get the learning configuration of the first
        node.

        Can specify dataprep_method, that each node will execute on its intput data before fit. Must accept x and y has
        arguments and return datapreped x and y.
        """
        if nodes is not None:
            if not isinstance(nodes, list):
                raise TypeError(f"Node argument must be a list, got {type(nodes)}")
            for i, node in enumerate(nodes):
                if not isinstance(node, Node):
                    raise TypeError(f"Node {i} in nodes is not of class Node, but {type(node)}")
            if nnodes is not None:
                logger.warning("Nodes were given to central server, so number of nodes to create will be ignored")

        if public_configs_path is None and nodes is None:
            raise ValueError("At least one of public_configs_path and nodes must be specified")

        if nnodes is not None and not isinstance(nnodes, int):
            raise TypeError(f"nnodes should be a integer, got a {type(nnodes)}")

        self.dataprep_method = dataprep_method

        self.nodes = nodes
        if public_configs_path is not None:
            self.public_configs = LearningConfig(public_configs_path)
            if self.nodes is not None:
                for node in self.nodes:
                    node.public_configs = self.public_configs
                    node.dataprep_method = dataprep_method
            else:
                for i in range(nnodes):
                    self.add_node()
        else:
            if len(self.nodes) == 0:
                raise ValueError("If public_configs_path is not specified, nodes must not be empty")
            self.public_configs = nodes[0].public_configs
            self.dataprep_method = nodes[0].dataprep_method
            for node in self.nodes[1:]:
                node.public_configs = self.public_configs
                node.dataprep_method = self.dataprep_method

        self.rulesets = []
        self.ruleset = None

    def add_node(self, node: Union[Node] = None):
        """Add the node to self, or creates a new one if node is None"""
        if node is not None:
            if not isinstance(node, Node):
                raise TypeError(f"Node is not of class Node, but {type(node)}")
            node.public_configs = self.public_configs
        else:
            node = Node(public_configs=self.public_configs, dataprep_method=self.dataprep_method)
        self.nodes.append(node)

    def aggregate(self) -> bool:
        """Among all rules generated by the nodes in the current iteration, will keep only the most recurent rule(s).

        Those rules will be passed to the node later, and the points associated to them will be ignored in order to find
        other relevant rules. In order not to remove too many points, a maximum of coverage is imposed.

        Returns False if no rules were found by nodes, which will stop the learning iterations.
        """
        logger.info("Aggregating fit results...")
        all_rules = []
        for ruleset in self.rulesets:
            all_rules += ruleset.rules
        if len(all_rules) == 0:
            logger.info("... no more rules found, stopping learning")
            return False
        occurences = {r: all_rules.count(r) for r in set(all_rules) if r.coverage < self.public_configs.max_coverage}
        if len(occurences) == 0:
            logger.warning("No rules matched coverage criterion, stopping learning")
            return False
        max_occurences = max(list(occurences.values()))
        if self.ruleset is None:
            self.ruleset = RuleSet(
                [r for r in occurences if occurences[r] == max_occurences],
                remember_activation=False,
                stack_activation=False,
            )
        else:
            self.ruleset += RuleSet(
                [r for r in occurences if occurences[r] == max_occurences and r not in self.ruleset],
                remember_activation=False,
                stack_activation=False,
            )
        logger.info("... fit results aggregated")
        return True

    def fit(
        self,
        niterations: int,
        make_images: bool = True,
        save_trees: bool = True,
        save_rulesets: bool = True,
        save_path: Optional[Union[str, Path, TransparentPath]] = None,
    ):
        logger.info("Started fit...")
        if len(self.nodes) == 0:
            logger.warning("Zero nodes. Fitting canceled.")
            return

        features_names = self.nodes[0].public_configs.features_names
        for _ in range(niterations):
            if CentralServer.PARALLEL_NODES:
                with ProcessPoolExecutor(max_workers=cpu_count(), mp_context=get_context("spawn")) as executor:
                    results = list(executor.map(Node.fit, self.nodes))
            else:
                results = []
                for node in self.nodes:
                    results.append(node.fit())
            for i, tree_ruleset in enumerate(results):
                tree, ruleset = tree_ruleset
                self.rulesets.append(ruleset)
                if save_path is not None:
                    if type(save_path) == str:
                        save_path = TransparentPath(save_path)
                else:
                    save_path = TransparentPath()

                save_to = save_path / f"node_{i}"
                if make_images:
                    Node.tree_to_graph(save_to / "tree.dot", None, tree, features_names)
                if save_trees:
                    Node.tree_to_joblib(save_to / "tree.joblib", None, tree)
                if save_rulesets:
                    Node.rule_to_file(save_to / "ruleset.csv", None, ruleset)
            if not self.aggregate():
                break
            self.rulesets = []
            for node in self.nodes:
                node.update_from_central(deepcopy(self.ruleset))

            if self.ruleset is not None:
                iteration = 0
                name = TransparentPath(self.public_configs.output_path).stem
                path = TransparentPath(self.public_configs.output_path).parent / f"{name}_{iteration}.csv"
                while path.isfile():
                    iteration += 1
                    path = path.parent / f"{name}_{iteration}.csv"
                self.ruleset.save(self.public_configs.output_path)
                self.ruleset.save(path)

        logger.info("...fit finished")
