from kivy import kivy_data_dir
from types import ModuleType
import os, sys
import pytest

from simulation import Simulator

lib_path = os.path.abspath(os.path.join('..', 'next-word-predictor'))
sys.path.append(lib_path)


@pytest.fixture
def simulator(request):
        from main import MainApp
        application = MainApp()
        simulator = Simulator(application)

        def fin():
                simulator.clean_queue()

        request.addfinalizer(fin)
        return simulator
