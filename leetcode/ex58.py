def lengthOfLastWord(s):
    words = s.split()
    if words:
        return len(words[-1])
    return 0

# Test cases
test_cases = ["Hello World", "   fly me   to   the moon  ", "luffy is still joyboy"]
for s in test_cases:
    print(f"Input: '{s}'")
    print("Output:", lengthOfLastWord(s))
    print()