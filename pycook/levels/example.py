from random import randint

from pycook.levels import BaseLevel
from pycook.robot import Robot
from pycook.trap import Trap
from pycook.floor import SolidColor
import pycook.collision as collision


class Level(BaseLevel):
    def __init__(self):
        self.running = True

    def start(self, engine):
        import pycook.sleep
        import stackless

        from stackless import channel

        #import pdb
        #pdb.set_trace()

        print("RUN INIT_KILLER")
        self.init_killer()

        trap_channel = channel()

        robot1 = Robot("r1", (350, 250))
        engine.objects.append(robot1)

        robot2 = Robot("r2", (300, 350))
        engine.objects.append(robot2)

        floor = SolidColor((255, 0, 0), (500, 200, 200, 200))
        engine.floor.append((0, floor))

        trap_collider = collision.Rectangle(500, 200, 200, 200)
        trap = Trap(
            trap_channel,
            lambda obj: collision.contains(trap_collider, obj.collision)
        )

        engine.traps.append(trap)

        def robot_controller(robot):
            print("START ROBOT CONTROLLER")
            # pycook.sleep.sleep(1000)
            # robot.rotate(randint(-360, 360))
            # robot.forward(240)
            # robot.rotate(90)
            # robot.forward(130)
            # robot.rotate(-30)
            # robot.forward(120)
            robot.rotate(-90)
            robot.forward(300)
            print("EXIT ROBOT CONTROLLER")

        stackless.tasklet(robot_controller)(robot1)
        stackless.tasklet(robot_controller)(robot2)

        def trap_action():
            pc = 0
            counter = 0
            while True:
                into, typ, ide = trap_channel.receive()
                print(into, typ, ide)
                if into:
                    counter += 1
                else: 
                    counter -= 1
                if pc != counter:
                    if counter > 1:
                        floor.color = (0, 255, 0)
                    elif counter > 0:
                        floor.color = (255, 255, 0)
                    else:
                        floor.color = (255, 0, 0)
                    pc = counter

        stackless.tasklet(trap_action)()

        print("RUNNING LOGIC")
        pycook.sleep.init()
        stackless.run()
        print("FINISH RUNNING")
