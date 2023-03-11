text = "w w w o r l d g g g g r e a t t e c c h e m g g p w w"
chars = text.split()
word_start = 0
current_symbol = chars[0]
result = []

for i in range(1, len(chars)):
    if chars[i] != current_symbol:
        result.append([current_symbol] * (i - word_start))
        current_symbol = chars[i]
        word_start = i
result.append([current_symbol] * (len(chars) - word_start))
print(result)