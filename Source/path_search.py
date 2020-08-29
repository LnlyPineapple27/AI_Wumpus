from Point import Point


def is_in_map(map_size, cur_pos: Point):
    if 0 <= cur_pos.x < map_size and 0 <= cur_pos.y < map_size:
        return True
    return False


def tracePath(list_of_dict, start_pos: Point, goal_pos: Point):
    # list_of_dict must be valid to give correct result
    path = []
    tracing = goal_pos
    if list_of_dict:
        for i in range(len(list_of_dict), 0, -1):
            cur = list_of_dict[i - 1]
            if cur["Point"] == tracing:
                path.append(cur["Point"])
                tracing = cur["Parent"]
                if cur["Point"] == start_pos:
                    break
    path.reverse()  # to get path from start to goal
    return path


def BFS(map, start_pos: Point, goal_pos: Point):
    expanded = []
    expanded_with_parent = []
    frontier = []
    size = len(map)
    # dict format: { "Node": 2, "Parent": 1 },
    init = {"Point": start_pos, "Parent": None}
    frontier.append(init)
    # return nothing if goal is start
    if start_pos == goal_pos:
        return [goal_pos]

    while frontier:
        current_node = frontier.pop(0)
        node = current_node["Point"]
        if node not in expanded:
            neighbours = []
            p_up = node.up()
            p_down = node.down()
            p_left = node.left()
            p_right = node.right()
            if is_in_map(size, p_up) and map[p_up.x][p_up.y]:
                neighbours.append(p_up)
            if is_in_map(size, p_down) and map[p_down.x][p_down.y]:
                neighbours.append(p_down)
            if is_in_map(size, p_left) and map[p_left.x][p_left.y]:
                neighbours.append(p_left)
            if is_in_map(size, p_right) and map[p_right.x][p_right.y]:
                neighbours.append(p_right)

            for neighbour in neighbours:
                if neighbour == goal_pos:
                    expanded.append(node)
                    expanded.append(goal_pos)
                    expanded_with_parent.append(current_node)
                    expanded_with_parent.append({"Point": goal_pos, "Parent": node})

                    path_to_node = tracePath(expanded_with_parent, start_pos, neighbour)
                    return path_to_node
                else:
                    new_node = {"Point": neighbour, "Parent": node}
                    frontier.append(new_node)
            expanded.append(node)
            expanded_with_parent.append(current_node)

    return None


def dir_from_path(path):
    if not path:
        return []
    else:
        res = []
        prev = path.pop(0)
        for cur in path:
            horizontal = prev.x - cur.x
            vertical = prev.y - cur.y
            if horizontal == 1:
                res.append("Up")
            elif horizontal == -1:
                res.append("Down")
            elif vertical == 1:
                res.append("Left")
            elif vertical == -1:
                res.append("Right")
            else:
                res.append("???")
            prev = cur
        return res

if __name__ == "__main__":
    mat = [[True, False, True, True, True, True, False, True, True, True],
            [True, False, True, False, True, True, True, False, True, True],
            [True, True, True, False, True, True, False, True, False, True],
            [False, False, False, False, True, False, False, False, False, True],
            [True, True, True, False, True, True, True, False, True, False],
            [True, False, True, True, True, True, False, True, False, False],
            [True, False, False, False, False, False, False, False, False, True],
            [True, False, True, True, True, True, False, True, True, True],
            [True, True, False, False, False, False, True, False, False, True]]
    Source = Point(0, 0)
    Destination = Point(0, 0);

    path = BFS(mat, Source, Destination)
    for i in path:
        print(i)
    dir_path = dir_from_path(path)
    print(dir_path)