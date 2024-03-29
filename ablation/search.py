"""A script to search best configurations for the given setting."""
import json
import logging
import pathlib
import pprint
import re
from copy import deepcopy
from typing import *

import click
import pandas

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
        if not pattern.search(str(dic[key])):
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


def _filter_dictionaries(
    dics: Iterable[Mapping[str, Any]],
    keep_keys: Sequence[str],
    exclude_keys: Sequence[str],
) -> Iterable[Mapping[str, Any]]:
    keep_pattern = re.compile(pattern="|".join(keep_keys)) if keep_keys else None
    exclude_pattern = (
        re.compile(pattern="|".join(exclude_keys)) if exclude_keys else None
    )
    for dic in dics:
        if exclude_pattern:
            dic = {
                key: value
                for key, value in dic.items()
                if not exclude_pattern.search(key)
            }
        if keep_pattern:
            dic = {key: value for key, value in dic.items() if keep_pattern.search(key)}
        yield dic


@click.command()
@click.option("-a", "--at-most", type=int, default=None)
@click.option("-c", "--create-inverse-triples", type=str, default=None)
@click.option("-d", "--dataset", type=str, default=None)
@click.option("-e", "--exclude-keys", type=str, multiple=True, default=None)
@click.option("-k", "--keep-keys", type=str, multiple=True, default=None)
@click.option("-l", "--loss", type=str, default=None)
@click.option("-m", "--model", type=str, default=None)
@click.option("-o", "--output-path", type=pathlib.Path, default=None)
@click.option("-t", "--training-loop", type=str, default=None)
def main(
    at_most: Optional[int],
    dataset: Optional[str],
    create_inverse_triples: Optional[str],
    exclude_keys: Sequence[str],
    keep_keys: Sequence[str],
    loss: Optional[str],
    model: Optional[str],
    output_path: Optional[pathlib.Path],
    training_loop: Optional[str],
):
    """Search best configuration for the given setting."""
    logging.basicConfig(level=logging.INFO)
    at_most = at_most or 1
    best_configs = list(
        _filter_dictionaries(
            sorted(
                _iter_results(
                    dataset=dataset,
                    model=model,
                    create_inverse_triples=create_inverse_triples,
                    loss=loss,
                    training_loop=training_loop,
                ),
                key=lambda study: study.get("metadata.best_trial_evaluation"),
                reverse=True,
            ),
            keep_keys=keep_keys,
            exclude_keys=exclude_keys,
        )
    )[:at_most]

    if output_path:
        output_path.parent.mkdir(exist_ok=True, parents=True)
        pandas.DataFrame.from_records(best_configs).to_csv(output_path, sep="\t")
        print(f"Written to {output_path.as_posix()}")
        exit(0)

    for i, best in enumerate(best_configs):
        print("=" * 30 + f" {i} " + "=" * 30)
        pprint.pprint(best, sort_dicts=True)


if __name__ == "__main__":
    main()
