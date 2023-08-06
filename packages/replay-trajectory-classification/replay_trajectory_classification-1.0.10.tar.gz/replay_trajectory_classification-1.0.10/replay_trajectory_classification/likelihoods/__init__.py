# flake8: noqa
from .calcium_likelihood import (estimate_calcium_likelihood,
                                 estimate_calcium_place_fields)
from .multiunit_likelihood import (estimate_multiunit_likelihood,
                                   fit_multiunit_likelihood)
from .multiunit_likelihood_gpu import (estimate_multiunit_likelihood_gpu,
                                       fit_multiunit_likelihood_gpu)
from .multiunit_likelihood_gpu_pinned_arrays import (
    estimate_multiunit_likelihood_gpu_pinned_arrays,
    fit_multiunit_likelihood_gpu_pinned_arrays)
from .multiunit_likelihood_gpu_shared import (
    estimate_multiunit_likelihood_gpu_shared,
    fit_multiunit_likelihood_gpu_shared)
from .multiunit_likelihood_integer import (
    estimate_multiunit_likelihood_integer, fit_multiunit_likelihood_integer)
from .multiunit_likelihood_integer_cupy import (
    estimate_multiunit_likelihood_integer_cupy,
    fit_multiunit_likelihood_integer_cupy)
from .multiunit_likelihood_integer_no_dask import (
    estimate_multiunit_likelihood_integer_no_dask,
    fit_multiunit_likelihood_integer_no_dask)
from .multiunit_likelihood_integer_pass_position import (
    estimate_multiunit_likelihood_integer_pass_position,
    fit_multiunit_likelihood_integer_pass_position)
from .spiking_likelihood import (estimate_place_fields,
                                 estimate_spiking_likelihood)

_ClUSTERLESS_ALGORITHMS = {
    'multiunit_likelihood': (
        fit_multiunit_likelihood,
        estimate_multiunit_likelihood),
    'multiunit_likelihood_integer': (
        fit_multiunit_likelihood_integer,
        estimate_multiunit_likelihood_integer),
    'multiunit_likelihood_integer_cupy': (
        fit_multiunit_likelihood_integer_cupy,
        estimate_multiunit_likelihood_integer_cupy),
    'multiunit_likelihood_integer_no_dask_cupy': (
        fit_multiunit_likelihood_integer_no_dask,
        estimate_multiunit_likelihood_integer_no_dask),
    'multiunit_likelihood_integer_pass_position': (
        fit_multiunit_likelihood_integer_pass_position,
        estimate_multiunit_likelihood_integer_pass_position),
    'multiunit_likelihood_gpu': (
        fit_multiunit_likelihood_gpu,
        estimate_multiunit_likelihood_gpu),
    'multiunit_likelihood_gpu_shared': (
        fit_multiunit_likelihood_gpu_shared,
        estimate_multiunit_likelihood_gpu_shared),
    'multiunit_likelihood_gpu_pinned_arrays': (
        fit_multiunit_likelihood_gpu_pinned_arrays,
        estimate_multiunit_likelihood_gpu_pinned_arrays),
}
