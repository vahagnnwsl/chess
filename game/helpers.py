def sort_moves(moves):
    array = []
    for i in range(0, len(moves), 2):

        str = moves[i]['san'] + ' - '
        if i + 1 < len(moves):
            str += moves[i + 1]['san']
        array.append(str)
    return array
