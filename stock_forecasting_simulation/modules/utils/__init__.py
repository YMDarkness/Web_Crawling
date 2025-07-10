
# modules/utils/__init__.py
# 

from .Amazon import Amazon
from .AMD import AMD
from .Apple import Apple

from .BerkshireHathaway import BerkshireHathaway
from .BTC import BTC

from .COMEXGold import COMEXgold

from .Dxy import DXY

from .Google import Google

from .HanwhaAerospace import HanwhaAerospace
from .Hyundai import Hyundai

from .IXIC import IXIC

from .Kakao import Kakao
from .Kia import Kia
from .Kospi import Kospi

from .LGensol import LGensol

from .Market import Market
from .Meta import Meta
from .Microsoft import Microsoft

from .Naver import Naver
from .Netflix import Netflix
from .Nvidia import Nvidia

from .PoscoHoldings import PoscoHoldings

from .SamsungBioLogics import SamsungBioLogics
from .SamsungElectronics import SamsungElectronics
from .SKHynix import SKHynix
from .SP500 import GSPC

from .Tesla import Tesla

from .US10Y import US10Y

from .Vix import VIX

from .Wti import WTI

domestics = [
    SamsungElectronics,
    SamsungBioLogics,
    SKHynix, 
    Hyundai,
    Naver, 
    Kakao, 
    Kia,
    HanwhaAerospace, 
    PoscoHoldings,
    LGensol
]

worlds = [
    Apple, 
    Amazon, 
    AMD, 
    BerkshireHathaway, 
    Microsoft, 
    Meta, 
    Google, 
    Netflix, 
    Nvidia, 
    Tesla
]

goldoil = [
    COMEXgold, 
    WTI
]

etc = [
    Market, 
    Dxy, 
    US10Y, 
    BTC, 
    IXIC, 
    GSPC, 
    Kospi, 
    VIX
]
