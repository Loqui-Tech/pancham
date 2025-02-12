import pandas as pd

from pancham.lifecycle.split_variable import SplitVariableLifecycleEvent
from pancham.lifecycle_event import LifecycleState


class TestSplitVariable:

    def test_handle_no_data(self):
        state = LifecycleState(None, None, None)

        event = SplitVariableLifecycleEvent()

        assert event.process(state, {}) == state

    def test_handle_no_properties(self):
        state = LifecycleState(None, None, pd.DataFrame())

        event = SplitVariableLifecycleEvent()

        assert event.process(state, {}) == state

    def test_valid_event(self):
        config = {
            'func': {
                'split_variable': {
                    'variable_name': 'output',
                    'source_name': 'input',
                    'split_char': ';'
                }
            }
        }

        data = {
            'input': ['a', 'a;b', 'q,a;e']
        }

        state = LifecycleState(None, None, pd.DataFrame(data))

        event = SplitVariableLifecycleEvent()

        assert event.process(state, config) == state
        assert state.data['output'].iloc[0][0] == 'a'

        assert state.data['output'].iloc[1][0] == 'a'
        assert state.data['output'].iloc[1][1] == 'b'

        assert state.data['output'].iloc[2][0] == 'q,a'
        assert state.data['output'].iloc[2][1] == 'e'

    def test_valid_event_with_remove(self):
        config = {
            'func': {
                'split_variable': {
                    'variable_name': 'output',
                    'source_name': 'input',
                    'split_char': ';',
                    'remove_pattern': '\d+'
                }
            }
        }

        data = {
            'input': ['a', 'a;b', 'q,a;e', 'a2;b', 'a;3;b']
        }

        state = LifecycleState(None, None, pd.DataFrame(data))

        event = SplitVariableLifecycleEvent()

        assert event.process(state, config) == state
        assert state.data['output'].iloc[0][0] == 'a'

        assert state.data['output'].iloc[1][0] == 'a'
        assert state.data['output'].iloc[1][1] == 'b'

        assert state.data['output'].iloc[2][0] == 'q,a'
        assert state.data['output'].iloc[2][1] == 'e'

        assert state.data['output'].iloc[3][0] == 'a'
        assert state.data['output'].iloc[3][1] == 'b'
        assert state.data['output'].iloc[4][0] == 'a'
        assert state.data['output'].iloc[4][1] == 'b'
