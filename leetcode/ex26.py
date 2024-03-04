def removeDuplicates(nums):
    if not nums:
        return 0
    
    k = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            nums[k] = nums[i]
            k += 1
    
    return k

# Custom Judge
nums = [1, 1, 2, 2, 3, 4, 4, 5]
expectedNums = [1, 2, 3, 4, 5]

k = removeDuplicates(nums)

assert k == len(expectedNums)
for i in range(k):
    assert nums[i] == expectedNums[i]

print("All assertions passed.")