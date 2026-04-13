import re
from .base_strategy import PasswordStrategy

class TimeToCrackCalculator(PasswordStrategy):
    def evaluate(self,password:str)->str:
        charset_size=self._calculate_charset_size(password)
        total_combinations=charset_size**len(password)
        
        if len(password) <= 4:
            attempts_per_second = 300 
        elif len(password) <= 7:
            attempts_per_second = 10_000_000 
        else:
            attempts_per_second = 2_000_000_000_000 
            
        seconds=total_combinations/attempts_per_second
        return self._convert_seconds_to_readable_time(seconds)

    def _calculate_charset_size(self,password:str)->int:
        charset_size=0
        if re.search(r"[a-z]",password):
            charset_size += 26
        if re.search(r"[A-Z]",password):
            charset_size += 26
        if re.search(r"[0-9]",password):
            charset_size += 10
        if re.search(r"[^a-zA-Z0-9]",password):
            charset_size+=32
        return charset_size

    import math

    def getNumberWords(self, number: float, twoDP: bool) -> str:
        numberWords = ""
        trillion = 10 ** 12
        billion = 10 ** 9
        million = 10 ** 6
        thousand = 10 ** 4
        hundred = 10 ** 3
        
        while number / trillion >= 1:
            numberWords = " trillion" + numberWords
            number = number / trillion
        while number / billion >= 1:
            numberWords = " billion" + numberWords
            number = number / billion
        while number / million >= 1:
            numberWords = " million" + numberWords
            number = number / million
        while number / thousand >= 1:
            numberWords = " thousand" + numberWords
            number = number / thousand
        while number / hundred >= 1:
            numberWords = " hundred" + numberWords
            number = number / hundred
            
        decimalPoint = 100 if twoDP else 1
        number = round(number * decimalPoint) / decimalPoint
        
        if number == int(number):
            number_str = str(int(number))
        else:
            number_str = str(number)
            
        return number_str + numberWords

    def _convert_seconds_to_readable_time(self, number: float) -> str:
        if number < 0.01:
            if number == 0:
                return "0.00 secs"
            formatted = f"{number:.12f}".rstrip("0")
            if formatted == "0.":
                return f"{number:.2e} secs".replace("e", " x 10^")
            return f"{formatted} secs"
            
        if number < 120:
            return self.getNumberWords(number, True) + " seconds"
            
        hour = 60 * 60
        if number < hour:
            minutes = number / 60
            return self.getNumberWords(minutes, True) + " minutes"
            
        day = hour * 24
        if number < (2 * day):
            hours = number / hour
            return self.getNumberWords(hours, False) + " hours"
            
        month = day * 30
        if number < month:
            days = number / day
            return self.getNumberWords(days, False) + " days"
            
        year = day * 365
        if number < year:
            months = number / month
            return self.getNumberWords(months, False) + " months"
            
        century = year * 100
        if number < century * 10:
            years = number / year
            return self.getNumberWords(years, False) + " years"
            
        if number < century * 100:
            centuries = number / century
            return self.getNumberWords(centuries, False) + " centuries"
            
        years = number / year
        return self.getNumberWords(years, False) + " years"
