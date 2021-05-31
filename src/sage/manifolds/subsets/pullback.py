r"""
Manifold Subsets Defined as Pullbacks of Subsets under Continuous Maps
"""


# ****************************************************************************
#       Copyright (C) 2021 Matthias Koeppe <mkoeppe@math.ucdavis.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.manifolds.subset import ManifoldSubset

class ManifoldSubsetPullback(ManifoldSubset):

    """
    Manifold subset defined as a pullback of a subset under a continuous map.

    """

    def __init__(self, map, inverse=None, codomain_subset=None, name=None, latex_name=None):

        self._map = map
        self._inverse = inverse
        if codomain_subset is None:
            codomain_subset = map.codomain()
        self._codomain_subset = codomain_subset
        base_manifold = map.domain()
        map_name = map._name or 'f'
        map_latex_name = map._latex_name or map_name
        if latex_name is None:
            if name is None:
                latex_name = map_latex_name + r'^{-1}(' + domain_subset._latex_name + ')'
            else:
                latex_name = name
        if name is None:
            name = map_name + '_inv_' + domain_subset._name
        ManifoldSubset.__init__(self, base_manifold, name, latex_name=latex_name)

    def is_open(self):
        return self._subset.is_open()

    def is_closed(self):
        return self._subset.is_closed()

    def closure(self, name=None, latex_name=None):
        """
        EXAMPLES::

            sage: from sage.manifolds.subsets.pullback import ManifoldSubsetPullback
            sage: M = Manifold(2, 'R^2', structure='topological')
            sage: c_cart.<x,y> = M.chart() # Cartesian coordinates on R^2
            sage: r_squared = M.scalar_field(x^2+y^2)
            sage: r_squared.set_immutable()
            sage: I = RealSet((1, 2)); I
            sage: O = ManifoldSubsetPullback(r_squared, I); O
            sage: O.closure()
        """
        if self.is_closed():
            return self
        try:
            codomain_subset_closure = self._codomain_subset.closure()
        except AttributeError:
            return super().closure()
        closure = ManifoldSubsetPullback(self._map, self._inverse,
                                         codomain_subset_closure,
                                         name=name, latex_name=latex_name)
        closure.declare_superset(self)
        return closure
