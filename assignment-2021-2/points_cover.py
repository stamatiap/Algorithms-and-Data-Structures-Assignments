import argparse
from itertools import combinations

def read_file(input_file):
    with open(input_file) as points_file:
        points = []
        for line in points_file:
            coordinates = [int(x) for x in line.split()]
            points.append(tuple((coordinates[0], coordinates[1])))
    return points

def calc_line_equations(points):
    line_equations = []
    pairs = combinations(range(0,len(points)), 2)
    for point1, point2 in pairs:
        if points[point2][0] != points[point1][0]:
            a = float(points[point2][1] - points[point1][1]) / float(points[point2][0] - points[point1][0])
            b = points[point1][1] - (a * points[point1][0])
        else:
            a = "inf"
            b = points[point1][0]
        line_equations.append([tuple((a,b)), [point1, point2]])
    return line_equations

def get_unique_parallel_lines(line_equations):
    unique_lines = []
    for line in line_equations:
        if (line[0][0] == "inf" or line[0][0] == 0) and line[0] not in unique_lines:
            unique_lines.append(line[0])
    return unique_lines

def get_all_unique_lines(line_equations):
    unique_lines = []
    for line in line_equations:
        if line[0] not in unique_lines:
            unique_lines.append(line[0])
    return unique_lines

def find_subsets(line_equations, unique_lines):
    groups = [[] for _ in range(len(unique_lines))]
    for i, line in enumerate(unique_lines):
        for eq in line_equations:
            if line == eq[0]:
                groups[i] += eq[1]
    for i in range(0, len(groups)):
        groups[i] = list(set(groups[i]))
    return groups
    
def max_coverage_subset(subsets, universe):
    max_covered = -1
    selected = None
    for subset in subsets:
        coverage = len([value for value in subset if value in universe])
        if coverage > max_covered:
            max_covered = coverage
            selected = subset
    return selected

def greedy_algorithm(remaining_subsets, uncovered_universe):
    selected_subsets = []
    while len(uncovered_universe) > 0:
        selected = max_coverage_subset(remaining_subsets, uncovered_universe)
        selected_subsets.append(selected)
        for point in selected:
            if point in uncovered_universe:
                uncovered_universe.remove(point)
    return selected_subsets

def recursive(remaining_subsets, uncovered_universe, S, all_sets):
    for i, item in enumerate(remaining_subsets):
        if len(uncovered_universe) > 0:
            if uncovered_universe[0] in item:
                for j in item:
                    if j in uncovered_universe:
                        uncovered_universe.remove(j)
                S.append(remaining_subsets.pop(i))
                recursive(remaining_subsets, uncovered_universe, S, all_sets)
    else:
        all_sets.append(S)
        S = []

def optimization_algorithm(subsets, universe):
    all_sets = []
    S = []
    sub = subsets[:]
    uni = universe[:]
    recursive(subsets, universe, S, all_sets)
    all_sets.append(greedy_algorithm(sub, uni))
    return min(all_sets, key=len)

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="find optimal solution", action="store_true")
parser.add_argument("-g", help="find only parallel to axes lines", action="store_true")
parser.add_argument("points_file", help="file with the coordinates of each point")
args = parser.parse_args()

points = read_file(args.points_file)
points = list(sorted(points))
uncovered_universe = list(range(0, len(points)))
line_equations = calc_line_equations(points)

for index, item in enumerate(points):
    counter_y = len([point for point in points if point[1] == item[1]])
    if counter_y == 1:
        line_equations.append([tuple((0, item[1])), [index]])
    counter_x = len([point for point in points if point[0] == item[0]])
    if counter_x == 1:
        line_equations.append([tuple(('inf', item[0])), [index]])

if args.g:
    lines = get_unique_parallel_lines(line_equations)
else:
    lines = get_all_unique_lines(line_equations)

remaining_subsets = find_subsets(line_equations, lines)

if args.f:
    selected_subsets = optimization_algorithm(remaining_subsets, uncovered_universe)
else:
    selected_subsets = greedy_algorithm(remaining_subsets, uncovered_universe)

selected_subsets = [list(sorted(x)) for x in selected_subsets]
selected_subsets = list(sorted(selected_subsets))
selected_subsets = list(sorted(selected_subsets, key=len, reverse=True))
for subset in selected_subsets:
    output = [points[i] for i in subset]
    if len(output) == 1:
        output.append(tuple((output[0][0] + 1, output[0][1])))
    print(*output, sep=" ")