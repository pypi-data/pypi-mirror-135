"""Quala Quasi-Newton algorithms"""
from __future__ import annotations
import _quala
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "AndersonAccel",
    "AndersonAccelParams",
    "BroydenGood",
    "BroydenGoodParams",
    "LBFGS",
    "LBFGSParams",
    "LBFGSParamsCBFGS"
]


class AndersonAccel():
    """
    C++ documentation: :cpp:class:`quala::AndersonAccel`
    """
    @typing.overload
    def __init__(self, params: AndersonAccelParams) -> None: ...
    @typing.overload
    def __init__(self, params: AndersonAccelParams, n: int) -> None: ...
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, params: dict, n: int) -> None: ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray[numpy.float64, _Shape[m, 1]], r_k: numpy.ndarray[numpy.float64, _Shape[m, 1]]) -> numpy.ndarray[numpy.float64, _Shape[m, 1]]: ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray[numpy.float64, _Shape[m, 1]], r_k: numpy.ndarray[numpy.float64, _Shape[m, 1]], x_k_aa: numpy.ndarray[numpy.float64, _Shape[m, 1]]) -> None: ...
    def current_history(self) -> int: ...
    def initialize(self, g_0: numpy.ndarray[numpy.float64, _Shape[m, 1]], r_0: numpy.ndarray[numpy.float64, _Shape[m, 1]]) -> None: ...
    def reset(self) -> None: ...
    def resize(self, n: int) -> None: ...
    @property
    def params(self) -> AndersonAccelParams:
        """
        :type: AndersonAccelParams
        """
    pass
class AndersonAccelParams():
    """
    C++ documentation: :cpp:class:`quala::AndersonAccelParams`
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def memory(self) -> int:
        """
        :type: int
        """
    @memory.setter
    def memory(self, arg0: int) -> None:
        pass
    pass
class BroydenGood():
    """
    C++ documentation: :cpp:class:`quala::BroydenGood`
    """
    @typing.overload
    def __init__(self, params: BroydenGoodParams) -> None: ...
    @typing.overload
    def __init__(self, params: BroydenGoodParams, n: int) -> None: ...
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, params: dict, n: int) -> None: ...
    def apply(self, arg0: numpy.ndarray[numpy.float64, _Shape[m, 1]]) -> bool: 
        """
        q
        """
    def current_history(self) -> int: ...
    def reset(self) -> None: ...
    def resize(self, n: int) -> None: ...
    def update(self, xk: numpy.ndarray[numpy.float64, _Shape[m, 1]], xkp1: numpy.ndarray[numpy.float64, _Shape[m, 1]], pk: numpy.ndarray[numpy.float64, _Shape[m, 1]], pkp1: numpy.ndarray[numpy.float64, _Shape[m, 1]], forced: bool = False) -> bool: ...
    def update_sy(self, sk: numpy.ndarray[numpy.float64, _Shape[m, 1]], yk: numpy.ndarray[numpy.float64, _Shape[m, 1]], forced: bool = False) -> bool: ...
    @property
    def params(self) -> BroydenGoodParams:
        """
        :type: BroydenGoodParams
        """
    pass
class BroydenGoodParams():
    """
    C++ documentation: :cpp:class:`quala::BroydenGoodParams`
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def force_pos_def(self) -> bool:
        """
        :type: bool
        """
    @force_pos_def.setter
    def force_pos_def(self, arg0: bool) -> None:
        pass
    @property
    def memory(self) -> int:
        """
        :type: int
        """
    @memory.setter
    def memory(self, arg0: int) -> None:
        pass
    @property
    def min_div_abs(self) -> float:
        """
        :type: float
        """
    @min_div_abs.setter
    def min_div_abs(self, arg0: float) -> None:
        pass
    @property
    def restarted(self) -> bool:
        """
        :type: bool
        """
    @restarted.setter
    def restarted(self, arg0: bool) -> None:
        pass
    pass
class LBFGS():
    """
    C++ documentation: :cpp:class:`quala::LBFGS`
    """
    class Sign():
        """
        C++ documentation :cpp:enum:`quala::LBFGS::Sign`

        Members:

          Positive

          Negative
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Negative: _quala.LBFGS.Sign # value = <Sign.Negative: 1>
        Positive: _quala.LBFGS.Sign # value = <Sign.Positive: 0>
        __members__: dict # value = {'Positive': <Sign.Positive: 0>, 'Negative': <Sign.Negative: 1>}
        pass
    @typing.overload
    def __init__(self, params: LBFGSParams) -> None: ...
    @typing.overload
    def __init__(self, params: LBFGSParams, n: int) -> None: ...
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, params: dict, n: int) -> None: ...
    @typing.overload
    def apply(self, q: numpy.ndarray[numpy.float64, _Shape[m, 1]], γ: float) -> bool: ...
    @typing.overload
    def apply(self, q: numpy.ndarray[numpy.float64, _Shape[m, 1]], γ: float, J: typing.List[int]) -> bool: ...
    def current_history(self) -> int: ...
    def reset(self) -> None: ...
    def resize(self, n: int) -> None: ...
    def s(self, arg0: int) -> numpy.ndarray[numpy.float64, _Shape[m, 1]]: ...
    def scale_y(self, factor: float) -> None: ...
    def update(self, xk: numpy.ndarray[numpy.float64, _Shape[m, 1]], xkp1: numpy.ndarray[numpy.float64, _Shape[m, 1]], pk: numpy.ndarray[numpy.float64, _Shape[m, 1]], pkp1: numpy.ndarray[numpy.float64, _Shape[m, 1]], sign: LBFGS.Sign = Sign.Positive, forced: bool = False) -> bool: ...
    def update_sy(self, sk: numpy.ndarray[numpy.float64, _Shape[m, 1]], yk: numpy.ndarray[numpy.float64, _Shape[m, 1]], pkp1Tpkp1: float, forced: bool = False) -> bool: ...
    @staticmethod
    def update_valid(params: LBFGSParams, yᵀs: float, sᵀs: float, pᵀp: float) -> bool: ...
    def y(self, arg0: int) -> numpy.ndarray[numpy.float64, _Shape[m, 1]]: ...
    def α(self, arg0: int) -> float: ...
    def ρ(self, arg0: int) -> float: ...
    @property
    def n(self) -> int:
        """
        :type: int
        """
    @property
    def params(self) -> LBFGSParams:
        """
        :type: LBFGSParams
        """
    Negative: _quala.LBFGS.Sign # value = <Sign.Negative: 1>
    Positive: _quala.LBFGS.Sign # value = <Sign.Positive: 0>
    pass
class LBFGSParams():
    """
    C++ documentation: :cpp:class:`quala::LBFGSParams`
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def cbfgs(self) -> LBFGSParamsCBFGS:
        """
        :type: LBFGSParamsCBFGS
        """
    @cbfgs.setter
    def cbfgs(self, arg0: LBFGSParamsCBFGS) -> None:
        pass
    @property
    def force_pos_def(self) -> bool:
        """
        :type: bool
        """
    @force_pos_def.setter
    def force_pos_def(self, arg0: bool) -> None:
        pass
    @property
    def memory(self) -> int:
        """
        :type: int
        """
    @memory.setter
    def memory(self, arg0: int) -> None:
        pass
    @property
    def min_abs_s(self) -> float:
        """
        :type: float
        """
    @min_abs_s.setter
    def min_abs_s(self, arg0: float) -> None:
        pass
    @property
    def min_div_fac(self) -> float:
        """
        :type: float
        """
    @min_div_fac.setter
    def min_div_fac(self, arg0: float) -> None:
        pass
    pass
class LBFGSParamsCBFGS():
    """
    C++ documentation: :cpp:member:`quala::LBFGSParams::CBFGSParams `
    """
    def __bool__(self) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def α(self) -> float:
        """
        :type: float
        """
    @α.setter
    def α(self, arg0: float) -> None:
        pass
    @property
    def ϵ(self) -> float:
        """
        :type: float
        """
    @ϵ.setter
    def ϵ(self, arg0: float) -> None:
        pass
    pass
__version__ = '0.0.1'
