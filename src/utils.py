# -*- coding: utf-8 -*-

"""Utilities for collating experimental results."""

from typing import Any, Mapping, Optional, Type, Union

from pykeen.datasets import DataSet, get_dataset
from pykeen.losses import Loss, get_loss_cls
from pykeen.models import get_model_cls
from pykeen.models.base import Model
from pykeen.regularizers import Regularizer, get_regularizer_cls
from pykeen.triples import TriplesFactory
from pykeen.utils import resolve_device

__all__ = [
    'get_model_size',
]


def get_model_size(  # noqa: C901
    *,
    dataset: Union[None, str, Type[DataSet]] = None,
    dataset_kwargs: Optional[Mapping[str, Any]] = None,
    training_triples_factory: Optional[TriplesFactory] = None,
    testing_triples_factory: Optional[TriplesFactory] = None,
    validation_triples_factory: Optional[TriplesFactory] = None,
    model: Union[str, Type[Model]],
    model_kwargs: Optional[Mapping[str, Any]] = None,
    loss: Union[None, str, Type[Loss]] = None,
    loss_kwargs: Optional[Mapping[str, Any]] = None,
    regularizer: Union[None, str, Type[Regularizer]] = None,
    regularizer_kwargs: Optional[Mapping[str, Any]] = None,
    **_kwargs,
) -> int:
    """Make a model instance, similarly to how the pipelin is started, then return the model size."""
    device = resolve_device('cpu')
    training_triples_factory, testing_triples_factory, validation_triples_factory = get_dataset(
        dataset=dataset,
        dataset_kwargs=dataset_kwargs,
        training_triples_factory=training_triples_factory,
        testing_triples_factory=testing_triples_factory,
        validation_triples_factory=validation_triples_factory,
    )

    if model_kwargs is None:
        model_kwargs = {}

    if regularizer is not None:
        regularizer_cls = get_regularizer_cls(regularizer)
        model_kwargs['regularizer'] = regularizer_cls(
            device=device,
            **(regularizer_kwargs or {}),
        )

    if loss is not None:
        loss_cls = get_loss_cls(loss)
        model_kwargs['loss'] = loss_cls(**(loss_kwargs or {}))

    model = get_model_cls(model)
    model_instance: Model = model(
        random_seed=0,
        preferred_device=device,
        triples_factory=training_triples_factory,
        **model_kwargs,
    )
    return model_instance.num_parameter_bytes
