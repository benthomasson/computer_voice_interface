
# A finite state machine that listens for the spoken command "computer".
# When it hears computer it will change state to "computer" and then
# list for further commmands.


class StateMachine(object):

    def __init__(self, states, initial_state):
        self.states = states
        self.state = initial_state
        self.state.enter()

    def transition(self, text):
        new_state = self.state.transition(text)
        if new_state is not None:
            self.state.exit()
            self.state = new_state
            self.state.enter()

    def run(self, text):
        self.transition(text)


class State(object):

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def init(self, transitions):
        self.transitions = transitions

    def enter(self):
        print("Entering state", self.name)

    def exit(self):
        print("Exiting state", self.name)

    def transition(self, text):
        if text in self.transitions:
            return self.transitions[text]
        else:
            return None


class InitialState(State):

    def __init__(self, states):
        super().__init__("initial", states)

    def init(self):
        super().init({"computer": self.states["computer"]})


class ComputerState(State):

    def __init__(self, states):
        super().__init__("computer", states)

    def init(self):
        super().init({"exit": self.states["initial"],
                      "shutdown": self.states["shutdown"]})

    def transition(self, text):
        next_state = super().transition(text)
        if next_state is None:
            print("Computer heard:", text)
        return next_state


class ShutdownState(State):

    def __init__(self, states):
        super().__init__("shutdown", states)

    def init(self):
        super().init({})

    def enter(self):
        super().enter()
        print("Shutting down")


class ComputerFSM(StateMachine):

    def __init__(self):
        self.states = {}
        self.states.update({"shutdown": ShutdownState(self.states)})
        self.states.update({"computer": ComputerState(self.states)})
        self.states.update({"initial": InitialState(self.states)})
        super().__init__(self.states, self.states["initial"])
        for state in self.states.values():
            state.init()

    def run(self, text):
        print("Input:", text)
        super().run(text)
