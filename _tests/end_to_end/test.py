import pytest
from tools import simulate

from simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_if_starts_with_cathegory_list(simulator):
    simulator.assert_count("//Root//CathegoryList", 1)
    simulator.assert_count_min("//Root//CathegoryList//StandardButton", 1)

@pytest.mark.parametrize("params", [{}])
@simulate
def test_if_can_select_cathegories(simulator):
    simulator.tap("//Root//CathegoryList//StandardButton[1]")
    simulator.assert_count("//Root//WordList", 1)
    simulator.assert_count_min("//Root//WordList//StandardButton", 1)