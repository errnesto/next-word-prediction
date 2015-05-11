'''Adapter super Class'''

from kivy.event import EventDispatcher

class SuperAdapter(EventDispatcher):

  def __init__(self, **kwargs):
    '''Register 'on_signal' event'''
    self.register_event_type('on_signal')
    super(SuperAdapter, self).__init__(**kwargs)

  @staticmethod
  def is_available():
    '''Return Boolean weather the inputDevice is available'''
    raise NotImplementedError("Please Implement this method")

  def signal_dispatcher(self, *args):
    '''Map events from the input device to the apps own signals

    This should dispatch all the required signals in the form:
    self.dispatch('on_signal', 'signal_name')

    Required Signals are:
    'left'
    'right'
    'enter'

    Optional Signals are:
    'close'
    '''
    raise NotImplementedError("Please Implement this method")

  def on_signal(self, *args):
    '''Default Handler for 'on_signal' event

    This is required by kivy and called on every 'on_signal' event
    '''
    pass