class TrapChange:
    ENTER_AREA = True
    LEAVE_AREA = False


class Trap:
    def __init__(self, channel, inside_checker):
        self.objects_inside = set()
        self.channel = channel
        self.is_inside = inside_checker

    def start_visiting(self):
        self.visited_objects = set()

    def visit(self, obj):
        if self.is_inside(obj):
            self.visited_objects.add(obj)

    def end_visiting(self):
        from pycook.sleep import send_channel

        entered_objects = self.visited_objects.difference(self.objects_inside)
        escaped_objects = self.objects_inside.difference(self.visited_objects)
        self.objects_inside = self.visited_objects
        for obj in escaped_objects:
            send_channel(
                self.channel, (TrapChange.LEAVE_AREA, obj.type, obj.id)
            )

        for obj in entered_objects:
            send_channel(
                self.channel, (TrapChange.ENTER_AREA, obj.type, obj.id)
            )
