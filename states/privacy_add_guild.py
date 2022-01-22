from aiogram.dispatcher.filters.state import StatesGroup, State


class privacySet(StatesGroup):
    wait_add_guild = State()
    wait_add_min_lvl = State()
    wait_add_max_lvl = State()
    wait_add_lvl_up = State()