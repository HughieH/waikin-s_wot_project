
def romanToInt(s):
        """
        :type s: str
        :rtype: int
        """
        roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        sum = 0
        
        for char_index in range(len(s)):
            if ((char_index + 1) == len(s)):
                sum += roman[s[char_index]]
                print(sum)
            elif (roman[s[char_index]] >=  roman[s[char_index + 1]]):
                sum += roman[s[char_index]]
                print(sum)
            elif (roman[s[char_index]] <  roman[s[char_index + 1]]):
                sum -= roman[s[char_index]]
                print(sum)
        
        return sum

print(romanToInt("III"))