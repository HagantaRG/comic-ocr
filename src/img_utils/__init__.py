import numpy as np

def __compare_regions(
        r1: list[int],
        r2: list[int],
        padding: int = 0,
) -> bool:
    ef_r1: list[int] = [r1[0]-padding, r1[1]+padding, r1[2]-padding, r1[3]+padding]
    ef_r2: list[int] = [r2[0]-padding, r2[1]+padding, r2[2]-padding, r2[3]+padding]
    return (ef_r1[1] > ef_r2[0] and ef_r1[0] < ef_r2[1]) and (ef_r1[3] > ef_r2[2] and ef_r1[2] < ef_r2[3])

def __merge_regions(
        r1: list[int],
        r2: list[int],
) -> list[int]:
    y_cords: list[int] = [r1[2], r2[2], r1[3], r2[3]]
    x_cords: list[int] = [r1[0], r2[0], r1[1], r2[1]]
    x_max: int = max(x_cords)
    x_min: int = min(x_cords)
    y_max: int = max(y_cords)
    y_min: int = min(y_cords)
    new_region: list[int] = [x_min, x_max, y_min, y_max]
    return new_region

def merge_textboxes_easyocr(
        region_list: list[list[int]],
        padding: int = 0
) -> list[list[int]]:
    """
    :param padding: Leniency for region merging. Larger number means more regions likely to be merged.
    :param region_list: A list of regions where text is detected from easyOCR. This takes the form
    [x_min, x_max, y_min, y_max]
    :return: A list where close/overlapping regions have been merged into a larger box.
    """
    """
    How am I going to do this?
    First, comparing any two regions (r1 and r2). To see if the regions overlap, I will have to:
    Check if any of the lines intersect.
    Line segments:
    
    if xmax_r1 > xmin_r2 and xmin_r1 < xmax_r2
    AND ymax_r1 > ymin_r2 and ymin_r1 < ymax_r2

    """
    all_merged: bool = False
    last_region_list: list[list[int]] = region_list
    merged_regions: list[list[int]] = []
    while not all_merged:
        region_created: bool = False
        for counter_1 in range(len(last_region_list)):
            r1 = last_region_list[counter_1]
            for counter_2 in range(len(last_region_list)):
                if counter_2 == counter_1:
                    continue
                r2 = last_region_list[counter_2]
                if __compare_regions(r1, r2, padding):
                    new_region: list[int] = __merge_regions(r1, r2)
                    merged_regions.append(new_region)
                    leftover_regions: list[list[int]] = [
                        region for index, region in enumerate(last_region_list) if index not in [counter_1, counter_2]
                    ]
                    merged_regions += leftover_regions
                    last_region_list = merged_regions
                    merged_regions = []
                    region_created = True
                    break
            if region_created:
                break
        if not region_created:
            all_merged = True

    return last_region_list
