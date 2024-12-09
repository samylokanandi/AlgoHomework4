
def binary_search(packages, boxes):
    packages.sort()
    total_package_size = sum(packages)
    min_wasted_space = float('inf')

    def upper_bound(arr, value):
        low, high = 0, len(arr)
        while low < high:
            mid = (low + high) // 2
            if arr[mid] <= value:
                low = mid + 1
            else:
                high = mid
        return low

    for supplier in boxes:
        supplier.sort()
        if supplier[-1] < packages[-1]:
            continue

        waste = 0
        last_index = 0

        for box in supplier:
            current_index = upper_bound(packages, box)
            waste += (current_index - last_index) * box
            last_index = current_index
            if last_index == len(packages):
                break

        min_wasted_space = min(min_wasted_space, waste - total_package_size)

    return min_wasted_space if min_wasted_space != float('inf') else -1
