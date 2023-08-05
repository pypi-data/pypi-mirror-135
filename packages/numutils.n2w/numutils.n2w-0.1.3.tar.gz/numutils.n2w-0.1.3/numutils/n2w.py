from os.path import exists
import logging
from os import path
import yaml

DEBUG_LEVEL = logging.INFO


class n2w:
    def __init__(self, n, lang="en"):

        self.number = n
        self.data = self.__data(lang=lang)
        self.conjunction = self.data["conjunction"]

        @property
        def number(self):
            return self._number

        @number.setter
        def number(self, n):
            if not isinstance(n, int):
                raise Exception("Value must be an int")
            self._number = n

        # Logging
        self.logger = logging.getLogger()
        self.logger.setLevel(level=DEBUG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter
        ("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.debug(f"Number = {self.number}")

    def val(self):
        self.logger.debug("In get()")
        return self.number

    def words(self):
        self.logger.debug("In words()")
        return self.__number_as_words().replace("  ", " ").rstrip()

    def __number_as_words(self):
        self.logger.debug("In __number_as_words()")
        number_length = len(str(self.number))

        self.logger.debug(f"Number length = {number_length}")

        if number_length < 3:
            return self.__process_less_than_a_hundred(self.number)

        elif number_length == 3:
            return self.__process_three_digit_number(self.number)

        elif number_length > 3 and number_length < 7:
            start = str(self.number)[:-3]
            end = str(self.number)[-3:]

            first_part = ""
            joiner = ""
            last_part = ""

            if int(start) < 100:
                first_part = self.__process_less_than_a_hundred(start)
            else:
                first_part = self.__process_three_digit_number(start)

            if int(end) > 0 and int(end) < 100:
                joiner = " " + self.data["000"] + " " + self.conjunction + " "
            else:
                joiner = " " + self.data["000"] + " "

            if int(end) > 0 and int(end) < 100:
                last_part = self.__process_less_than_a_hundred(end)
            elif int(end) > 99:
                last_part = self.__process_three_digit_number(end)

            return first_part + joiner + last_part

        else:
            return "Only numbers < 1_000_000 dealt with at the moment"

    def __process_less_than_a_hundred(self, n):
        self.logger.debug("__process_less_than_a_hundred()")
        n = int(n)
        number_length = len(str(n))

        if number_length == 1:
            return self.data[str(n)]

        elif number_length == 2:
            if n < 21:
                return self.data[str(n)]
            else:
                return self.__process_tens(n)

    def __process_three_digit_number(self, n):
        h = str(n)[0]
        tu = str(n)[1:]

        if tu == "":
            return tu

        hundreds = self.__process_hundreds(h)

        if int(tu) == 0:
            return hundreds
        else:
            return hundreds + " " + self.conjunction + " " + self.__process_tens(tu)

    def __process_hundreds(self, x):
        h = str(x)[0]
        return self.data[str(h)] + " " + self.data["00"]

    def __process_tens(self, tu):
        tu = int(tu)
        if tu < 21:
            return self.data[str(tu)]

        t = str(tu)[0]
        u = str(tu)[1]

        if t == "0":
            tens = ""
        else:
            tens = self.data[t + "0"]

        units = self.data[u]

        if u == "0":
            return tens
        else:
            return tens + " " + units

    def __data(self, lang="en"):
        path_to_file = path.join(path.dirname(__file__), f"config/{lang}.yaml")
        if not exists(path_to_file):
            raise ValueError(
                f"Language '{lang}' not yet supported. Can't find \
        configuration file at {path_to_file}"
            )

        with open(path_to_file, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        return data
