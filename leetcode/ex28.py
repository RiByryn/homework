def strStr(haystack, needle):
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i+len(needle)] == needle:
            return i
    
    return -1

# Custom Judge
haystack = "sadbutsad"
needle = "sad"
expectedOutput = 0

output = strStr(haystack, needle)
assert output == expectedOutput

print("Output:", output)