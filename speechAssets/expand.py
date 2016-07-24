def expand(a):
    if type(a[0]) is list:
        route_set = []
        for first in a[0]:
            if len(a) == 1:
                route_set.append([first])
            else:
                for rest in expand(a[1:]):
                    route = [first] + rest
                    route_set.append(route)
        return route_set
    else:
        route_set = []
        first = [a[0]]
        if len(a) == 1:
            route_set.append(first)
        else:
            for rest in expand(a[1:]):
                route = first + rest
                route_set.append(route)
        return route_set

