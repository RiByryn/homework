def removeElement(nums, val):
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    
    return k

# Custom Judge
nums = [3, 2, 2, 3]
val = 3
expectedNums = [2, 2]

k = removeElement(nums, val)

assert k == len(expectedNums)
for i in range(k):
    assert nums[i] == expectedNums[i]

print("All assertions passed.")