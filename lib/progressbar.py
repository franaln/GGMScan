import sys
import time

class ProgressBar:

    def __init__(self, total):
        self.start_time = time.time()
        self.total = total
        self.barlength = 100
        self.increment = int(total/self.barlength)
        self.current_progress = 0

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

        rate = self.get_rate(event, elapsed_time)
        remaining_time = self.get_remaining_time(event, elapsed_time)

        bar = '['
        for i in xrange(self.barlength):
            if i < self.current_progress:
                bar += '='
            else:
                bar += ' '

        perc = event/float(self.total) * 100

        bar += "] %i of %i " % (event, self.total)
        bar += " (%i%%) | %s | %s remaining"  %  (perc, rate, remaining_time)

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
            return "--"

        rate = event/elapsed_time
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
            rate_str += "GHz";

        return rate_str

    def get_remaining_time(self, event, elapsed_time):

        if event == 0:
            return "--"

        remaining_time = float(self.total)/event - 1
        remaining_time *= elapsed_time

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
    pb = ProgressBar(500)
    for i in xrange(500):
        time.sleep(0.1)
        pb.print_bar(i+1)

if __name__ == '__main__':
    test()
