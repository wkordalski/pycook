class BaseLevel:
    def __init__(self):
        self.run_kill = None
        
    def init_killer(self):
        import stackless
        import pycook.sleep

        def killer():
            def setter(trigger):
                self.run_kill = trigger

            pycook.sleep.wait_for_signal(setter)
            pycook.sleep.kill()

            # kill all other tasklets...

        stackless.tasklet(killer)()

    def kill(self):
        self.run_kill()