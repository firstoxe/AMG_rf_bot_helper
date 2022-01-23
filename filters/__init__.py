from .Trigger_f import TriggerCheck
from loader import dp
from .forward_from_rf_bot import ForwardFromRfBot
from .energy_cap import energyCap
from .echo_item import EchoItem
from .amplifier import AmplifierCheck
from .work_check import WorkCheck
from .is_creator import CreatorFilter

if __name__ == "filters":
    dp.filters_factory.bind(TriggerCheck)
    dp.filters_factory.bind(ForwardFromRfBot)
    dp.filters_factory.bind(energyCap)
    dp.filters_factory.bind(EchoItem)
    dp.filters_factory.bind(AmplifierCheck)
    dp.filters_factory.bind(WorkCheck)
    dp.filters_factory.bind(CreatorFilter)
