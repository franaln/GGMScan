import sys
import time

class ProgressBar:

    def __init__(self, total, done=0):
        self.start_time = time.time()
        self.total = total
        self.done = done
        self.barlength = 100
        self.increment = int(total/self.barlength)
        self.increment_n = 1
        self.current_progress = 0

        if self.increment == 0:
            self.increment = 1
            self.barlength = total

        for i in xrange(done):
            if i % self.increment == 0:
                self.current_progress += 1

    def print_bar(self, event):

        if event > self.total:
            event = event % self.total

        if event % self.increment == 0:
            self.current_progress += 1
        elif event % 10 == 0:
            pass
        else:
            return

        elapsed_time = time.time() - self.start_time

        self.last_time = time.time()
        self.last_event = event

        rate = self.get_rate(event, elapsed_time)
        remaining_time = self.get_remaining_time(event, rate)

        unit = 0
        while (rate >= 1.e3 and unit < 3):
            rate /= 1.e3
            unit += 1
        rate_str = '%.2f ' % rate
        if unit == 0:
            rate_str += "Hz"
        elif unit == 1:
            rate_str += "kHz"
        elif unit == 2:
            rate_str += "MHz"
        elif unit == 3:
            rate_str += "GHz"

        bar = '['
        for i in xrange(self.barlength):
            if i < self.current_progress:
                bar += '='
            else:
                bar += ' '

        perc = event/float(self.total) * 100

        bar += "] %i of %i " % (event, self.total)
        bar += " (%i%%) | %s | %s remaining"  %  (perc, rate_str, remaining_time)

        # Add new line (only for last line in fancy draw mode)
        if event == self.total:
            bar += '\n'

        # Print to screen
        self.clear_line()
        sys.stdout.write(bar)
        sys.stdout.flush()

    def clear_line(self):
        sys.stdout.write('\r')
        sys.stdout.flush()

    def get_rate(self, event, elapsed_time):

        if event == 0:
            return 0

        rate = (event-self.done)/elapsed_time

        return rate

    def get_remaining_time(self, event, rate):

        if event == 0:
            return "--"

        remaining_events = self.total - event

        try:
            remaining_time = remaining_events / rate
        except ZeroDivisionError:
            return '--'

        # remaining_time = float(self.total-self.done)/(event-self.done) - 1
        # remaining_time *= elapsed_time

        unit = 0
        while (remaining_time > 60 and unit < 2):
            remaining_time /= 60
            unit += 1

        remaining_time_str = '%.2f ' % remaining_time

        if unit == 0:
            remaining_time_str += "sec";
        elif unit == 1:
            remaining_time_str += "min";
        elif unit == 2:
            remaining_time_str += "hour";

        return remaining_time_str


def test():
    import sys

    if len(sys.argv) > 2:
        total = int(sys.argv[1])
        done = int(sys.argv[2])
    elif len(sys.argv) > 1:
        total = int(sys.argv[1])
        done = 0
    else:
        total = 100
        done = 0

    pb = ProgressBar(total, done)
    for i in xrange(done, total):
        time.sleep(0.1)
        pb.print_bar(i+1)

if __name__ == '__main__':
    test()
