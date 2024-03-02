def is_palindrome(x):
    if x < 0:
        return False
    reversed_x = int(str(x)[::-1])
    return x == reversed_x

# Test the function
x = 12321
print(is_palindrome(x))  # Output: True

x = 12345
print(is_palindrome(x))  # Output: False