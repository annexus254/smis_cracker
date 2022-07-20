import colorama
import cursor


class ProgressBar:
    """
    This class defines a simple, lightweight and generic progress bar.
    """

    def __init__(self, total):
        self.total = total
        self.color_below_half = colorama.Fore.RED
        self.color_above_half = colorama.Fore.YELLOW
        self.color_above_eighty_percent = colorama.Fore.GREEN

    def print(self, progress):
        cursor.hide()

        print(self.getProgessBarString(progress) , end='\r')

        if progress == self.total:
            print(colorama.Fore.RESET)
            cursor.show()
            
        return self

    def getProgessBarString(self, progress):
        no_of_bars = int((progress)/self.total * 100)
        no_of_dashes = 100 - no_of_bars

        if no_of_bars < 50:
            return self.color_below_half + '\r|{0}{1}| {2}%'.format(
                '█' * no_of_bars, '-' * no_of_dashes, round(float((progress)/self.total * 100), 2))
        elif no_of_bars < 80:
            return self.color_above_half + '\r|{0}{1}| {2}%'.format(
                '█' * no_of_bars, '-' * no_of_dashes, round(float((progress)/self.total * 100), 2))
        else:
            return self.color_above_eighty_percent + '\r|{0}{1}| {2}%'.format(
                '█' * no_of_bars, '-' * no_of_dashes, round(float((progress)/self.total * 100), 2))

    def resetTotal(self, total):
        self.total = total
        return self

    def resetColors(self, color_below_half=colorama.Fore.RED, color_above_half=colorama.Fore.YELLOW, color_above_eighty_percent=colorama.Fore.GREEN):
        self.color_below_half = color_below_half
        self.color_above_half = color_above_half
        self.color_above_eighty_percent = color_above_eighty_percent
        return self

    def __del__(self):
        print(colorama.Fore.RESET)
        del self.total
