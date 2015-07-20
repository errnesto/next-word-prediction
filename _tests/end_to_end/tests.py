# coding=utf-8
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
    simulator.assert_count("//Root//ActButton", 3)

@pytest.mark.parametrize("params", [{}])
@simulate
def test_back_button(simulator):
    simulator.tap("//Root//CathegoryList//StandardButton[1]")
    simulator.assert_count("//Root//WordList", 1)
    simulator.tap("//Root//WordList//ActButton//Button[@text="Menu"]")
    simulator.assert_count("//Root//CathegoryList", 1)

@pytest.mark.parametrize("params", [{}])
@simulate
def test_selecting_a_word(simulator):
    simulator.tap("//Root//CathegoryList//StandardButton[1]")
    button_selector = "//Root//WordList//StandardButton[1]"
    # test are called in a queue. This means when we try to acces something from the state, we have to do this with callbacks 
    def cb(button):
        simulator.tap(button_selector)
        simulator.assert_text("//Root//Label", " " + button.text)

    simulator.get_node(button_selector, cb)


@pytest.mark.parametrize("params", [{}])
@simulate
def test_delete_button(simulator):
    simulator.tap("//Root//CathegoryList//StandardButton[1]")
    button_selector = "//Root//WordList//StandardButton[1]"
    # test are called in a queue so when we get somthing from the state we have to do this with callbacks 
    def cb(button):
        simulator.tap(button_selector)
        simulator.tap(button_selector) # same selector but now this is a different button
        simulator.tap(u"//Root//WordList//ActButton//Button[@text="löschen"]")
        simulator.assert_text("//Root//Label", button.text)
        
    simulator.get_node(button_selector, cb)