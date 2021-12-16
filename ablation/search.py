"""A script to search best configurations for the given setting."""
import json
import logging
import pathlib
import pprint
import re
from copy import deepcopy
from typing import *

import click

HERE = pathlib.Path(__file__).parent
RESULTS = HERE.joinpath("results")


logger = logging.getLogger(__name__)


def _flatten_dict(
    dic: Any,
    prefix: Sequence[str] = tuple(),
) -> Iterable[Tuple[Tuple[str, ...], float]]:
    if not isinstance(dic, dict):
        yield prefix, dic
        return

    for k, v in dic.items():
        yield from _flatten_dict(dic=v, prefix=prefix + (k,))


def flatten_dict(dic: Mapping[str, Any], prefix=None):
    if prefix is None:
        prefix = tuple()
    if isinstance(prefix, str):
        prefix = (prefix,)
    return dict(
        (".".join(k), v)
        for k, v in _flatten_dict(
            dic,
            prefix=prefix,
        )
    )


def iterate_studies_from_hpo_directory(
    directory: pathlib.Path,
) -> Iterable[Mapping[str, Any]]:
    study_path = directory.joinpath("study.json")
    if not study_path.is_file():
        logger.warning(f"missing study path: {directory}")
        return

    hpo_config_path = directory.joinpath("hpo_config.json")
    if not hpo_config_path.is_file():
        logger.warning(f"missing hpo config: {directory}")
        return

    with study_path.open() as file:
        study = json.load(file)

    with directory.joinpath("best_pipeline", "pipeline_config.json").open() as file:
        ppc = json.load(file)
    study.update(flatten_dict(dic=ppc, prefix=("pipeline_config",)))

    if "create_inverse_triples" not in study:
        study["create_inverse_triples"] = ppc["pipeline"]["dataset_kwargs"][
            "create_inverse_triples"
        ]
    with hpo_config_path.open() as file:
        hpo_config = json.load(file)

    study.setdefault("create_inverse_triples", False)
    study["searcher"] = hpo_config["optuna"]["sampler"]
    study.update(flatten_dict(dic=hpo_config, prefix=("hpo",)))

    # Get replicates directory
    for replicate_results_path in directory.rglob("results.json"):
        yv: MutableMapping[str, Any] = deepcopy(study)
        yv["replicate"] = int(replicate_results_path.parent.name.split("-")[1])
        with replicate_results_path.open() as file:
            replicate_results = json.load(file)
        del replicate_results["losses"]
        yv.update(flatten_dict(replicate_results, prefix="results"))
        with replicate_results_path.with_name("metadata.json").open() as file:
            yv.update(flatten_dict(json.load(file), prefix="metadata"))
        yield yv


def _match_dictionary(
    dic: Mapping[str, Any], patterns: Mapping[str, Optional[re.Pattern]]
) -> bool:
    for key, pattern in patterns.items():
        if pattern is None:
            continue
        if not pattern.search(dic[key]):
            return False
    return True


def _iter_results(
    **kwargs: Mapping[str, Optional[str]],
) -> Iterable[Mapping[str, Any]]:
    patterns = {
        key: None if value is None else re.compile(value)
        for key, value in kwargs.items()
    }
    for study_path in RESULTS.rglob(pattern="study.json"):
        for study in iterate_studies_from_hpo_directory(study_path.parent):
            if _match_dictionary(study, patterns=patterns):
                yield study


@click.command()
@click.option("-d", "--dataset", type=str, default=None)
@click.option("-m", "--model", type=str, default=None)
def main(
    dataset: Optional[str] = None,
    model: Optional[str] = None,
):
    """Search best configuration for the given setting."""
    logging.basicConfig(level=logging.INFO)
    pprint.pprint(
        max(
            _iter_results(dataset=dataset, model=model),
            key=lambda study: study.get("metadata.best_trial_evaluation"),
        ),
        sort_dicts=True,
    )


if __name__ == "__main__":
    main()
