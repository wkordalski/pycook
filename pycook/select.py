import random
from stackless import channel, tasklet, getcurrent

from .sleep import sleep


def _proxy_task(channel_in, channel_out, tasklets):
    v = channel_in.receive()

    for t in tasklets:
        if t != getcurrent():
            t.kill()

    channel_out.send(v)


def _timeout_task(timeout_msec, channel_out, tasklets):
    sleep(timeout_msec)

    for t in tasklets:
        if t != getcurrent():
            t.kill()

    channel_out.send(None)


def select(*channels, timeout=None, shuffle=False):
    """
    Timeout - wait for any message for this amount of milliseconds.
    Returns pair (channel, value) or None if timeout exceeded
    """
    if shuffle:
        random.shuffle(channels)

    if len(channels) == 0:
        if timeout is None:
            return None
        else:
            sleep(timeout)

    if len(channels) == 1 and timeout is None:
        value = channels[0].receive()
        return (channels[0], value)

    output = channel()

    tls = [tasklet(_proxy_task) for c in channels]
    tar = [c for c in channels]
    if timeout is not None:
        tls.append(tasklet(_timeout_task))
        tar.append(timeout)

    for tl, arg in zip(tls, tar):
        tl(arg, output, tls)

    return output.receive()
