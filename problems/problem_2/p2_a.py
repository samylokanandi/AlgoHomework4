# Problem 2 a 

def linear_search(packages, boxes):
    packages.sort()
    min_wasted_space = float('inf')

    for supplier_boxes in boxes:
        supplier_boxes.sort()
        if supplier_boxes[-1] < packages[-1]:
            continue

        total_waste, i = 0, 0
        for box in supplier_boxes:
            while i < len(packages) and packages[i] <= box:
                total_waste += box - packages[i]
                i += 1
            if i == len(packages):
                break

        min_wasted_space = min(min_wasted_space, total_waste)

    return min_wasted_space if min_wasted_space < float('inf') else -1