class Time:
    def __init__(self, init_time=0):
        self.time = init_time  # time in ingame minutes

    def formated(self):
        time = self.time % (24*60)
        hours = int(time / 60)
        minutes = time % 60
        return f"{hours}:{minutes}"

time = None
