from pycook.levels import BaseLevel
from pycook.robot import Robot


class Level(BaseLevel):
    def __init__(self):
        self.running = True

    def start(self, engine):
        import pycook.sleep
        import stackless

        self.init_killer()

        robot = Robot((130, 130))
        engine.objects.append(robot)

        def robot_controller():
            print("START ROBOT CONTROLLER")
            pycook.sleep.sleep(1000)
            robot.rotate(240)
            robot.forward(240)
            robot.rotate(90)
            robot.forward(130)
            robot.rotate(-30)
            robot.forward(120)
            print("EXIT ROBOT CONTROLLER")

        stackless.tasklet(robot_controller)()

        print("RUNNING LOGIC")
        pycook.sleep.init()
        stackless.run()
        print("FINISH RUNNING")
