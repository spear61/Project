def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    # return True
    # if bottom_b < bottom_a:
    #     print('bottom')
    #     return 'bottom'
    # elif top_b > top_a:
    #     print('top')
    #     return 'top'
    # elif left_b < left_a:
    #     print('left')
    #     return 'left'
    # elif right_b > right_a:
    #     print('right')
    #     return 'right'

    return True

