import sys
import time
import threading
import tkinter
import traceback

import crawler
import qlearningAgents_student

class Application(object):
    def __init__(self, win, max_steps):
        self.ep = 0
        self.ga = 2
        self.al = 2
        self.stepCount = 0
        self.max_steps = max_steps
        self.exit_status = 0

        # Init Gui
        self.__initGUI(win)

        self.robot = crawler.CrawlingRobot(self.canvas)
        self.robotEnvironment = crawler.CrawlingRobotEnvironment(self.robot)

        # Init Agent
        simulationFn = lambda agent: simulation.SimulationEnvironment(self.robotEnvironment, agent)
        actionFn = lambda state: self.robotEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents_student.QLearningAgent(actionFn=actionFn)

        self.learner.setEpsilon(self.epsilon)
        self.learner.setLearningRate(self.alpha)
        self.learner.setDiscount(self.gamma)

        # Start GUI
        self.running = True
        self.stopped = False
        self.stepsToSkip = 0
        self.thread = threading.Thread(target = self._run_wrapper)
        self.thread.start()

    def sigmoid(self, x):
        return 1.0 / (1.0 + 2.0 ** (-x))

    def incrementSpeed(self, inc):
        self.tickTime *= inc
        # self.epsilon = min(1.0, self.epsilon)
        # self.epsilon = max(0.0,self.epsilon)
        # self.learner.setSpeed(self.epsilon)
        self.speed_label['text'] = 'Step Delay: %.5f' % (self.tickTime)

    def incrementEpsilon(self, inc):
        self.ep += inc
        self.epsilon = self.sigmoid(self.ep)
        self.learner.setEpsilon(self.epsilon)
        self.epsilon_label['text'] = 'Epsilon: %.3f' % (self.epsilon)

    def incrementGamma(self, inc):
        self.ga += inc
        self.gamma = self.sigmoid(self.ga)
        self.learner.setDiscount(self.gamma)
        self.gamma_label['text'] = 'Discount: %.3f' % (self.gamma)

    def incrementAlpha(self, inc):
        self.al += inc
        self.alpha = self.sigmoid(self.al)
        self.learner.setLearningRate(self.alpha)
        self.alpha_label['text'] = 'Learning Rate: %.3f' % (self.alpha)

    def __initGUI(self, win):
        # Window
        self.win = win

        # Initialize Frame
        win.grid()
        self.dec = -0.5
        self.inc = 0.5
        self.tickTime = 0.05

        # Epsilon Button + Label
        self.setupSpeedButtonAndLabel(win)

        self.setupEpsilonButtonAndLabel(win)

        # Gamma Button + Label
        self.setUpGammaButtonAndLabel(win)

        # Alpha Button + Label
        self.setupAlphaButtonAndLabel(win)

        # Exit Button
        # self.exit_button = tkinter.Button(win,text='Quit', command=self.exit)
        # self.exit_button.grid(row=0, column=9)

        # Simulation Buttons
        # self.setupSimulationButtons(win)

        # Canvas
        self.canvas = tkinter.Canvas(root, height=200, width=1000)
        self.canvas.grid(row=2, columnspan=10)

    def setupAlphaButtonAndLabel(self, win):
        self.alpha_minus = tkinter.Button(win, text="-", command=(lambda: self.incrementAlpha(self.dec)))
        self.alpha_minus.grid(row=1, column=3, padx=10)

        self.alpha = self.sigmoid(self.al)
        self.alpha_label = tkinter.Label(win, text='Learning Rate: %.3f' % (self.alpha))
        self.alpha_label.grid(row=1, column=4)

        self.alpha_plus = tkinter.Button(win, text="+", command=(lambda: self.incrementAlpha(self.inc)))
        self.alpha_plus.grid(row=1, column=5, padx=10)

    def setUpGammaButtonAndLabel(self, win):
        self.gamma_minus = tkinter.Button(win, text="-", command=(lambda: self.incrementGamma(self.dec)))
        self.gamma_minus.grid(row=1, column=0, padx=10)

        self.gamma = self.sigmoid(self.ga)
        self.gamma_label = tkinter.Label(win, text='Discount: %.3f' % (self.gamma))
        self.gamma_label.grid(row=1, column=1)

        self.gamma_plus = tkinter.Button(win, text="+",command=(lambda: self.incrementGamma(self.inc)))
        self.gamma_plus.grid(row=1, column=2, padx=10)

    def setupEpsilonButtonAndLabel(self, win):
        self.epsilon_minus = tkinter.Button(win, text="-",command=(lambda: self.incrementEpsilon(self.dec)))
        self.epsilon_minus.grid(row=0, column=3)

        self.epsilon = self.sigmoid(self.ep)
        self.epsilon_label = tkinter.Label(win, text='Epsilon: %.3f' % (self.epsilon))
        self.epsilon_label.grid(row=0, column=4)

        self.epsilon_plus = tkinter.Button(win, text="+",command=(lambda: self.incrementEpsilon(self.inc)))
        self.epsilon_plus.grid(row=0, column=5)

    def setupSpeedButtonAndLabel(self, win):
        self.speed_minus = tkinter.Button(win, text="-",command=(lambda: self.incrementSpeed(0.5)))
        self.speed_minus.grid(row=0, column=0)

        self.speed_label = tkinter.Label(win, text='Step Delay: %.5f' % (self.tickTime))
        self.speed_label.grid(row=0, column=1)

        self.speed_plus = tkinter.Button(win, text="+",command=(lambda: self.incrementSpeed(2)))
        self.speed_plus.grid(row=0, column=2)

    def skip5kSteps(self):
        self.stepsToSkip = 5000

    def exit(self):
        self.running = False

        if (self.thread is not None):
            self.thread.join()
            self.thread = None

        if (self.win is not None):
            self.win.destroy()
            self.win = None

    def step(self):
        self.stepCount += 1

        state = self.robotEnvironment.getCurrentState()
        actions = self.robotEnvironment.getPossibleActions(state)

        if len(actions) == 0.0:
            self.robotEnvironment.reset()
            state = self.robotEnvironment.getCurrentState()
            actions = self.robotEnvironment.getPossibleActions(state)
            print('Reset!')

        action = self.learner.getAction(state)
        if action == None:
            raise Exception('None action returned: Code Not Complete')

        nextState, reward = self.robotEnvironment.doAction(action)
        self.learner.observeTransition(state, action, nextState, reward)

    # Run on a different thread.
    def _run_wrapper(self):
        try:
            self.run()
        except Exception as ex:
            self.exit_status = 10
            traceback.print_exc()
            self.win.quit()

        self.running = False
        self.stopped = True

        self.win.quit()

    # Run on a different thread.
    def run(self):
        self.stepCount = 0
        self.learner.startEpisode()

        while True:
            minSleep = 0.01
            tm = max(minSleep, self.tickTime)
            time.sleep(tm)
            self.stepsToSkip = int(tm / self.tickTime) - 1

            if not self.running:
                break

            for i in range(self.stepsToSkip):
                self.step()

            self.stepsToSkip = 0
            self.step()

            if (self.max_steps is not None and self.stepCount >= self.max_steps):
                break

        self.learner.stopEpisode()

    def start(self):
        self.win.mainloop()

def run(max_steps = None):
    global root
    root = tkinter.Tk(baseName = 'crawler')
    root.title('Crawler GUI')
    root.resizable(0, 0)

    app = Application(root, max_steps = max_steps)

    def update_gui():
        if (app.running):
            app.robot.draw(app.stepCount, app.tickTime)
            root.after(10, update_gui)
    update_gui()

    root.protocol('WM_DELETE_WINDOW', app.exit)
    app.start()
    app.exit()

    return app.exit_status
