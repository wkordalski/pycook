import heapq
from stackless import channel, schedule, tasklet, TaskletExit
import threading
import time

wake_up_interval = 0.003*10
minimum_sleep_time = 0.001

command_channel = channel(label='sleep_command_channel')
timepoints_queue = []

conditions_lock = threading.Lock()
conditions_counter = 0
conditions_dict = {}

command_processor_tasklet = None
alarm_tasklet = None


def command_processor_task():
    while True:
        msg = command_channel.receive()
        if msg[0] == 'T':
            (cmd, timepoint, response_channel) = msg
            heapq.heappush(timepoints_queue, (timepoint, response_channel))
        elif msg[0] == 'F':
            with conditions_lock:
                (cmd, key, cond, response_channel) = msg
                conditions_dict[key] = (cond, response_channel)


def alarm_task():
    while True:
        moment = time.monotonic()
        while len(timepoints_queue) > 0:
            (timepoint, response_channel) = heapq.heappop(timepoints_queue)
            if timepoint < moment:
                response_channel.send(None)
            else:
                heapq.heappush(timepoints_queue, (timepoint, response_channel))
                break

        items = list(conditions_dict.items())
        for k, (cond, chan) in items:
            if cond():
                del conditions_dict[k]
                chan.send(None)

        # TODO: if there are other tasklets - 
        # schedule - remember to keep the time
        # else - sleep for specified time

        # schedule other taskslets
        schedule()

        # fall asleep if needed, do not fall asleep for less then 1ms
        new_wake_up = time.monotonic()
        if moment + wake_up_interval - minimum_sleep_time > new_wake_up:
            time.sleep(moment + wake_up_interval - new_wake_up)


def sleep(msec):
    try:
        chan = channel()
        timepoint = time.monotonic() + msec / 1000
        command_channel.send(('T', timepoint, chan))
        chan.receive()
    except TaskletExit:
        timepoints_queue.remove((timepoint, chan))
        heapq.heapify(timepoints_queue)
        raise


def wait_for_signal(trigger_placer):
    global conditions_counter
    try:
        chan = channel()
        key = conditions_counter
        conditions_counter += 1
        var = [False]

        command_channel.send(('F', key, lambda: var[0], chan))

        def trigger():
            var[0] = True
        trigger_placer(trigger)

        chan.receive()
    except TaskletExit:
        del conditions_dict[key]
        raise


def init():
    global command_processor_tasklet, alarm_tasklet
    command_processor_tasklet = tasklet(
        command_processor_task, label='sleep_command_processor_task'
    )
    alarm_tasklet = tasklet(
        alarm_task, label='sleep_alarm_task'
    )
    command_processor_tasklet()
    alarm_tasklet()


def kill():
    command_processor_tasklet.kill()
    alarm_tasklet.kill()
