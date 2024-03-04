def searchInsert(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return left

# Custom Judge
nums = [1, 3, 5, 6]
target = 5
expectedOutput = 2

output = searchInsert(nums, target)
assert output == expectedOutput

print("Output:", output)