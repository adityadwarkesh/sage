r"""
Rigged Configurations of `\mathcal{B}(\infty)`

AUTHORS:

- Travis Scrimshaw (2013-04-16): Initial version
"""

#*****************************************************************************
#       Copyright (C) 2013 Travis Scrimshaw <tscrim@ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.lazy_attribute import lazy_attribute
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.parent import Parent
from sage.categories.highest_weight_crystals import HighestWeightCrystals
from sage.combinat.root_system.cartan_type import CartanType
from sage.combinat.rigged_configurations.rigged_configuration_element import (
     RiggedConfigurationElement, RCNonSimplyLacedElement)
from sage.combinat.rigged_configurations.rigged_configurations import RiggedConfigurationOptions

# Note on implementation, this class is used for simply-laced types only
class InfinityCrystalOfRiggedConfigurations(Parent, UniqueRepresentation):
    r"""
    Class of rigged configurations modeling `\mathcal{B}(\infty)`.

    INPUT:

    - ``cartan_type`` -- a Cartan type
    """
    @staticmethod
    def __classcall_private__(cls, cartan_type):
        r"""
        Normalize the input arguments to ensure unique representation.

        EXAMPLES::

            sage: RC1 = InfinityCrystalOfRiggedConfigurations(CartanType(['A',3]))
            sage: RC2 = InfinityCrystalOfRiggedConfigurations(['A',3])
            sage: RC2 is RC1
            True
        """
        cartan_type = CartanType(cartan_type)
        if not cartan_type.is_simply_laced():
            vct = cartan_type.as_folding()
            return InfinityCrystalOfNonSimplyLacedRC(vct)

        return super(InfinityCrystalOfRiggedConfigurations, cls).__classcall__(cls, cartan_type)

    def __init__(self, cartan_type):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['A',3])
            sage: TestSuite(RC).run()
        """
        self._cartan_type = cartan_type
        Parent.__init__(self, category=HighestWeightCrystals())
        # We store the cartan matrix for the vacancy number calculations for speed
        self._cartan_matrix = self._cartan_type.cartan_matrix()
        self.module_generators = (self.element_class(self, rigging_list=[[]]*cartan_type.rank()),)

    global_options = RiggedConfigurationOptions

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: InfinityCrystalOfRiggedConfigurations(['A',3])
            The infinity crystal of rigged configurations of type ['A', 3]
        """
        return "The infinity crystal of rigged configurations of type {}".format(self._cartan_type)

    def _element_constructor_(self, lst=None, **options):
        """
        Construct an element of ``self`` from ``lst``.
        """
        return self.element_class(self, lst, **options)

    def _calc_vacancy_number(self, partitions, a, i, **options):
        r"""
        Calculate the vacancy number of the `i`-th row of the `a`-th rigged
        partition.

        This assumes that `\gamma_a = 1` for all `a` and `(\alpha_a \mid
        \alpha_b ) = A_{ab}`.

        INPUT:

        - ``partitions`` -- the list of rigged partitions we are using

        - ``a`` -- the rigged partition index

        - ``i`` -- the row index of the `a`-th rigged partition

        TESTS::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['A', 4, 1])
            sage: elt = RC(partition_list=[[1], [1], [], []])
            sage: RC._calc_vacancy_number(elt.nu(), 1, 0)
            0
        """
        row_len = partitions[a][i]
        vac_num = 0
        for b, value in enumerate(self._cartan_matrix.row(a)):
            vac_num -= value * partitions[b].get_num_cells_to_column(row_len)

        return vac_num

    class Element(RiggedConfigurationElement):
        """
        A rigged configuration in `\mathcal{B}(\infty)` in simply-laced types.

        EXAMPLES:

        Type `A_n^{(1)}` examples::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['A', 4, 1])
            sage: RC(partition_list=[[2], [2, 2], [2], [2]])
            <BLANKLINE>
            0[ ][ ]0
            <BLANKLINE>
            -2[ ][ ]-2
            -2[ ][ ]-2
            <BLANKLINE>
            2[ ][ ]2
            <BLANKLINE>
            -2[ ][ ]-2
            <BLANKLINE>

            sage: RC = InfinityCrystalOfRiggedConfigurations(['A', 4, 1])
            sage: RC(partition_list=[[], [], [], []])
            <BLANKLINE>
            (/)
            <BLANKLINE>
            (/)
            <BLANKLINE>
            (/)
            <BLANKLINE>
            (/)
            <BLANKLINE>

        Type `D_n^{(1)}` examples::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['D', 4, 1])
            sage: RC(partition_list=[[3], [3,2], [4], [3]])
            <BLANKLINE>
            -1[ ][ ][ ]-1
            <BLANKLINE>
            1[ ][ ][ ]1
            0[ ][ ]0
            <BLANKLINE>
            -3[ ][ ][ ][ ]-3
            <BLANKLINE>
            -1[ ][ ][ ]-1
            <BLANKLINE>

            sage: RC = InfinityCrystalOfRiggedConfigurations(['D', 4, 1])
            sage: RC(partition_list=[[1], [1,1], [1], [1]])
            <BLANKLINE>
            1[ ]1
            <BLANKLINE>
            0[ ]0
            0[ ]0
            <BLANKLINE>
            0[ ]0
            <BLANKLINE>
            0[ ]0
            <BLANKLINE>
            sage: RC(partition_list=[[1], [1,1], [1], [1]], rigging_list=[[0], [0,0], [0], [0]])
            <BLANKLINE>
            1[ ]0
            <BLANKLINE>
            0[ ]0
            0[ ]0
            <BLANKLINE>
            0[ ]0
            <BLANKLINE>
            0[ ]0
            <BLANKLINE>

        TESTS::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['A', 4, 1])
            sage: elt = RC(partition_list=[[1], [1], [], []], rigging_list=[[-1], [0], [], []]); elt
            <BLANKLINE>
            -1[ ]-1
            <BLANKLINE>
            0[ ]0
            <BLANKLINE>
            (/)
            <BLANKLINE>
            (/)
            <BLANKLINE>
            sage: TestSuite(elt).run()
        """
        def weight(self):
            """
            Return the weight of ``self``.
            """
            P = self.parent().weight_lattice_realization()
            alpha = list(P.simple_roots())
            return sum(sum(x) * alpha[i] for i,x in enumerate(self))

class InfinityCrystalOfNonSimplyLacedRC(InfinityCrystalOfRiggedConfigurations):
    r"""
    Rigged configurations for `\mathcal{B}(\infty)` in non-simply-laced types.
    """
    def __init__(self, vct):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['C',2,1]); RC
            Rigged configurations of type ['C', 2, 1]
         """
        self._folded_ct = vct
        InfinityCrystalOfRiggedConfigurations.__init__(self, vct._cartan_type)

    @lazy_attribute
    def virtual(self):
        """
        Return the corresponding virtual crystal.

        EXAMPLES::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['C',2])
            sage: RC
            B infinity rigged configurations of type ['C', 3]
            sage: RC.virtual
            B infinity rigged configurations of type ['A', 3]
        """
        return InfinityCrystalOfRiggedConfigurations(self._folded_ct._folding)

    def to_virtual(self, rc):
        """
        Convert ``rc`` into a rigged configuration in the virtual crystal.

        INPUT:

        - ``rc`` -- a rigged configuration element

        EXAMPLES::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['C',2])
            sage: elt = RC(partition_list=[[3],[2]]); elt
            <BLANKLINE>
            0[ ][ ][ ]0
            <BLANKLINE>
            0[ ][ ]0
            sage: velt = RC.to_virtual(elt); velt
            <BLANKLINE>
            0[ ][ ][ ]0
            <BLANKLINE>
            0[ ][ ][ ][ ]0
            <BLANKLINE>
            0[ ][ ][ ]0
            sage: velt.parent()
            B infinity rigged configurations of type ['A', 3]
        """
        gamma = map(int, self._folded_ct.scaling_factors())
        sigma = self._folded_ct._orbit
        n = self._folded_ct._folding.rank()
        vindex = self._folded_ct._folding.index_set()
        partitions = [None] * n
        riggings = [None] * n
        vac_nums = [None] * n
        # -1 for indexing
        for a, rp in enumerate(rc):
            for i in sigma[a]:
                k = vindex.index(i)
                partitions[k] = [row_len*gamma[a] for row_len in rp._list]
                riggings[k] = [rig_val*gamma[a] for rig_val in rp.rigging]
                vac_nums[k] = [vac_num*gamma[a] for vac_num in rp.vacancy_numbers]
        return self.virtual.element_class(self.virtual, partition_list=partitions,
                            rigging_list=riggings,
                            vacancy_numbers_list=vac_nums)

    def from_virtual(self, vrc):
        """
        Convert ``vrc`` in the virtual crystal into a rigged configution of
        the original Cartan type.

        INPUT:

        - ``vrc`` -- a virtual rigged configuration

        EXAMPLES::

            sage: RC = InfinityCrystalOfRiggedConfigurations(['C',2])
            sage: elt = RC(partition_list=[[3],[2]])
            sage: vrc_elt = RC.to_virtual(elt)
            sage: ret = RC.from_virtual(vrc_elt); ret
            <BLANKLINE>
            0[ ][ ][ ]0
            <BLANKLINE>
            0[ ][ ]0
            sage: ret == elt
            True
        """
        gamma = list(self._folded_ct.scaling_factors()) #map(int, self._folded_ct.scaling_factors())
        sigma = self._folded_ct._orbit
        n = self._cartan_type.rank()
        partitions = [None] * n
        riggings = [None] * n
        vac_nums = [None] * n
        vindex = self._folded_ct._folding.index_set()
        # TODO: Handle special cases for A^{(2)} even and its dual?
        for a in range(n):
            index = vindex.index(sigma[a][0])
            partitions[a] = [row_len // gamma[a] for row_len in vrc[index]._list]
            riggings[a] = [rig_val / gamma[a] for rig_val in vrc[index].rigging]
            vac_nums[a] = [vac_val / gamma[a] for vac_val in vrc[index].vacancy_numbers]
        return self.element_class(self, partition_list=partitions,
                                  rigging_list=riggings, vacancy_numbers_list=vac_nums)

    class Element(RCNonSimplyLacedElement):
        """
        A rigged configuration in `\mathcal{B}(\infty)` in
        non-simply-laced types.

        TESTS::
        """
        def weight(self):
            """
            Return the weight of ``self``.
            """
            P = self.parent().weight_lattice_realization()
            alpha = list(P.simple_roots())
            return sum(sum(x) * alpha[i] for i,x in enumerate(self))

class InfinityCrystalOfRCA2Even(InfinityCrystalOfNonSimplyLacedRC):
    """
    Infinity crystal of rigged configurations for type `A_{2n}^{(2)}`.
    """
    def to_virtual(self, rc):
        """
        Convert ``rc`` into a rigged configuration in the virtual crystal.

        INPUT:

        - ``rc`` -- a rigged configuration element

        EXAMPLES::

            sage: from sage.combinat.rigged_configurations.rc_infinity import InfinityCrystalOfRCA2Even
            sage: RC = InfinityCrystalOfRCA2Even(CartanType(['A',4,2]).as_folding())
            sage: elt = RC(partition_list=[[1],[1]]); elt
            <BLANKLINE>
            -1[ ]-1
            <BLANKLINE>
            1[ ]1
            <BLANKLINE>
            sage: velt = RC.to_virtual(elt); velt
            <BLANKLINE>
            -1[ ]-1
            <BLANKLINE>
            2[ ]2
            <BLANKLINE>
            -1[ ]-1
            <BLANKLINE>
            sage: velt.parent()
            Rigged configurations of type ['A', 3, 1] and factor(s) ((2, 2), (2, 2))
        """
        gamma = self._folded_ct.scaling_factors()
        sigma = self._folded_ct.folding_orbit()
        n = self._folded_ct._folding.rank()
        partitions = [None] * n
        riggings = [None] * n
        vac_nums = [None] * n
        # +/- 1 for indexing
        for a in range(len(rc)):
            for i in sigma[a]:
                partitions[i] = [row_len for row_len in rc[a]._list]
                riggings[i] = [rig_val*gamma[a] for rig_val in rc[a].rigging]
                vac_nums[i] = [vac_num*gamma[a] for vac_num in rc[a].vacancy_numbers]
        return self.virtual.element_class(self.virtual, partition_list=partitions,
                            rigging_list=riggings,
                            vacancy_numbers_list=vac_nums)

    def from_virtual(self, vrc):
        """
        Convert ``vrc`` in the virtual crystal into a rigged configution of
        the original Cartan type.

        INPUT:

        - ``vrc`` -- a virtual rigged configuration element

        EXAMPLES::

            sage: from sage.combinat.rigged_configurations.rc_infinity import InfinityCrystalOfRCA2Even
            sage: RC = InfinityCrystalOfRCA2Even(CartanType(['A',4,2]).as_folding())
            sage: elt = RC(partition_list=[[1],[1]])
            sage: velt = RC.to_virtual(elt)
            sage: ret = RC.from_virtual(velt); ret
            <BLANKLINE>
            -1[ ]-1
            <BLANKLINE>
            1[ ]1
            <BLANKLINE>
            sage: ret == elt
            True
        """
        gamma = self._folded_ct.scaling_factors()
        sigma = self._folded_ct.folding_orbit()
        n = self._cartan_type.rank()
        partitions = [None] * n
        riggings = [None] * n
        vac_nums = [None] * n
        # +/- 1 for indexing
        for a in range(n):
            index = sigma[a][0]
            partitions[index] = [row_len for row_len in vrc[index]._list]
            riggings[index] = [rig_val//gamma[a] for rig_val in vrc[index].rigging]
            vac_nums[a] = [vac_val//gamma[a] for vac_val in vrc[index].vacancy_numbers]
        return self.element_class(self, partition_list=partitions,
                                  rigging_list=riggings, vacancy_numbers_list=vac_nums)

