# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import numpy as np
import pytest
from PyMPDATA.boundary_conditions import Extrapolated
from PyMPDATA.impl.traversals import Traversals
from PyMPDATA import ScalarField, VectorField, Options

JIT_FLAGS = Options().jit_flags


class TestBoundaryConditionExtrapolated:
    @staticmethod
    @pytest.mark.parametrize("data", (
        np.array([1, 2, 3, 4], dtype=float),
        np.array([1, 2, 3, 4], dtype=complex)
    ))
    def test_1d_scalar(data, n_threads=1, halo=1):
        # arrange
        boundary_conditions = (Extrapolated(),)
        field = ScalarField(data, halo, boundary_conditions)
        traversals = Traversals(
            grid=field.grid, halo=halo, jit_flags=JIT_FLAGS, n_threads=n_threads
        )
        field.assemble(traversals)
        meta_and_data, fill_halos = field.impl
        sut = traversals._code['fill_halos_scalar']  # pylint:disable=protected-access

        # act
        thread_id = 0
        sut(thread_id, *meta_and_data, *fill_halos)

        # assert
        print(field.data)
        # TODO #289

    @staticmethod
    @pytest.mark.parametrize("data", (np.array([1, 2, 3, 4], dtype=float),))
    def test_1d_vector(data, n_threads=1, halo=2):
        # arrange
        boundary_condition = (Extrapolated(),)
        field = VectorField((data,), halo, boundary_condition)
        traversals = Traversals(
            grid=field.grid, halo=halo, jit_flags=JIT_FLAGS, n_threads=n_threads
        )
        field.assemble(traversals)
        meta_and_data, fill_halos = field.impl
        sut = traversals._code['fill_halos_vector']  # pylint:disable=protected-access

        # act
        thread_id = 0
        sut(thread_id, *meta_and_data, *fill_halos)

        # assert
        print(field.data)
        # TODO #289
