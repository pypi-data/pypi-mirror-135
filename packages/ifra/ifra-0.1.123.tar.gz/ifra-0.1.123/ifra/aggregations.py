from typing import List
from ruleskit import RuleSet
import logging

logger = logging.getLogger(__name__)


class Aggregation:
    """Abstract class for aggregating node models."""

    # noinspection PyUnresolvedReferences
    def __init__(self, central_server: "CentralServer"):  # Do not import CentralServer to avoid recursive import
        """
        Parameters
        ----------
        central_server: CentralServer
            `ifra.central_server.CentralServer` object
        """
        self.central_server = central_server
    
    def aggregate(self, rulesets: List[RuleSet]) -> str:
        """To be implemented in daughter class. Must modify inplace `ifra.central_server.CentralServer` *ruleset*.
        
        Parameters
        ----------
        rulesets: List[RuleSet]
            New rulesets provided by the nodes.
        
        Returns
        -------
        str\n
          * "updated" if central model was updates\n
          * "pass" if no new rules were found but learning should continue\n
          * "stop" otherwise. Will stop learning.\n
        """
        pass


class AdaBoostAggregation(Aggregation):
    """Among all rules generated by the nodes in the current iteration, will keep only the most recurent rule(s).

    Can be used by giving *adaboost_aggregation* as *aggregation* argument when creating a
    `ifra.central_server.CentralServer`

    Those rules will be added to  the given ruleset, returned by the function,
    and the points in each node's data activated by it will be ignored in order to find other relevant rules.
    In order not to remove too many points, a maximum of coverage is imposed.

    If among the rules extracted from the nodes, none are new compared to the current state of the model, nodes are
    not updated. If no new rules are found but each nodes had new data, learning is finished.
    """
    
    def aggregate(self, rulesets: List[RuleSet]) -> str:
        logger.info("Aggregating fit results using AdaBoost method...")
        all_rules = []
        n_nodes = len(self.central_server.nodes)

        for rs in rulesets:
            all_rules += rs.rules
        if len(all_rules) == 0:
            logger.info("... no rules found")
            if len(rulesets) == n_nodes:
                logger.info("No new rules were found, despite all nodes having provided a new model : learning is over")
                return "stop"
            return "pass"
        occurences = {r: all_rules.count(r) for r in set(all_rules)
                      if r.coverage < self.central_server.central_configs.max_coverage}
        if len(occurences) == 0:
            logger.warning("No rules matched coverage criterion")
            if len(rulesets) == n_nodes:
                logger.info("No new rules were found, despite all nodes having provided a new model : learning is over")
                return "stop"
            return "pass"
        max_occurences = max(list(occurences.values()))
        if self.central_server.ruleset is None:
            self.central_server.ruleset = RuleSet(
                [r for r in occurences if occurences[r] == max_occurences],
                remember_activation=False,
                stack_activation=False,
            )
        else:
            new_rules = [
                r for r in occurences if occurences[r] == max_occurences and r not in self.central_server.ruleset
            ]
            if len(new_rules) == 0:
                logger.warning("No new rules found")
                if len(rulesets) == n_nodes:
                    logger.info(
                        "No new rules were found, despite all nodes having provided a new model" " : learning is over"
                    )
                    return "stop"
                return "pass"
            self.central_server.ruleset += RuleSet(
                new_rules,
                remember_activation=False,
                stack_activation=False,
            )
        logger.info("... fit results aggregated")
        return "updated"
