def romanToInt(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev_value = 0
    
    for char in s:
        value = roman_values[char]
        if value > prev_value:
            result += value - 2 * prev_value
        else:
            result += value
        prev_value = value
    
    return result

# Example usage
print(romanToInt("III"))  # Output: 3
print(romanToInt("IV"))   # Output: 4
print(romanToInt("IX"))   # Output: 9
print(romanToInt("LVIII"))  # Output: 58
print(romanToInt("MCMXCIV"))  # Output: 1994