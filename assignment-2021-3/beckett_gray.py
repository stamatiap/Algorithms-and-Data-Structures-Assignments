from itertools import permutations
import argparse

def make_first_gray_code(n):
    gray_code = [[]]
    for _ in range(0, n):
        reversed_gray_code = []
        for i in range(len(gray_code)):
            reversed_gray_code.append(gray_code[i][:])
        reversed_gray_code.reverse()
        for _ in range(len(reversed_gray_code)):
            gray_code.append(reversed_gray_code[_])
        for j in range(0, len(gray_code)):
            if j < len(gray_code) / 2:
                gray_code[j].insert(0, 0)
            else:
                gray_code[j].insert(0, 1)
    return gray_code

def flip(code, i):
    if code[i] == 0:
        code[i] = 1
    else:
        code[i] = 0
    
def find_id_code(code):
    for i in range(0, len(first_gray_code)):
        counter = 0
        for j in range(0, len(first_gray_code[i])):
            if code[j] == first_gray_code[i][j]:
                counter += 1
        if counter == len(first_gray_code[i]):
            return i

def gc_dfs(d, x, max_coord, n, gc, visited, all_codes):
    if d == 2**n:
        all_codes.append(list(gc))
        return 
    for i in range(0, min(n - 1, max_coord)+1):
        flip(x, i)
        id = find_id_code(x)
        if not visited[id]:
            gc.append(list(x))
            visited[id] = True
            gc_dfs(d+1, x, max(i + 1, max_coord), n, gc, visited, all_codes)
            visited[id] = False
            gc.pop()
        flip(x, i)

def get_all_gray_codes(first_gray_code):
    visited = [False for _ in range(len(first_gray_code))]
    x = [first_gray_code[0][_] for _ in range(len(first_gray_code[0]))]
    visited[0] = True
    gc = []
    gc.append(list(x))
    d = 1
    all_codes = []
    max_coord = 0
    gc_dfs(d, x, max_coord, n, gc, visited, all_codes)
    return all_codes

def bgc_dfs(d, x, max_coord, n, gc, visited, all_codes, changed_coord):
    if d == 2**n:
        all_codes.append(list(gc))
        return 
    for i in range(0, min(n - 1, max_coord)+1):
        if x[i] == 0:
            flip(x, i)
            changed_coord.append(i)
        elif i == changed_coord[0]:
            flip(x, i)
            changed_coord.pop(0)
        else:
            continue
        id = find_id_code(x)
        if not visited[id]:
            gc.append(list(x))
            visited[id] = True
            bgc_dfs(d+1, x, max(i + 1, max_coord), n, gc, visited, all_codes, changed_coord)
            visited[id] = False
            gc.pop()
        if x[i] == 0:
            flip(x, i)
            changed_coord.insert(0, i)
        elif i == changed_coord[-1]:
            flip(x, i)
            changed_coord.pop()
        else:
            continue

def get_all_beckett_gray_codes(first_gray_code):
    visited = [False for _ in range(len(first_gray_code))]
    x = [first_gray_code[0][_] for _ in range(len(first_gray_code[0]))]
    visited[0] = True
    gc = []
    gc.append(list(x))
    d = 1
    all_codes = []
    changed_coord = []
    max_coord = 0
    bgc_dfs(d, x, max_coord, n, gc, visited, all_codes, changed_coord)
    return all_codes

def delta_sequence(code):
    delta = []
    for i in range(0, len(code)-1):
        code1 = code[i]
        code2 = code[i+1]
        for j in range(0, len(code1)):
            if code1[j] != code2[j]:
                delta.append(j)
                break
    return delta

def is_cyclic(code_seq):
    counter = 0
    for i in range(len(code_seq[0])):
        if code_seq[0][i] != code_seq[-1][i]:
                counter += 1
    if counter == 1:
        return True
    else:
        return False

def change_delta(delta, perm):
    x = []
    for i in range(len(perm)):
        x.append(int(i))
    y = []
    for j in range(len(delta)):
        y.append(perm[delta[j]])
    return y

def find_isomorphisms(delt, n):
    deltas = []
    for s in delt:
        lst = [int(x) for x in s]
        deltas.append(lst)
    lst = []
    for j in range(n):
        lst.append(j)
    p = list(permutations(lst, n))
    isomorphisms = []
    for index, delta in enumerate(deltas):
        for i in range(1, len(p)):
            delta_after_perm = change_delta(delta, list(p[i]))
            sd = [str(i) for i in delta_after_perm]
            delta_after_perm_str = ''.join(sd)
            for j, d in enumerate(deltas):
                d.reverse()
                sd = [str(i) for i in d]
                delta_str = ''.join(sd)
                if delta_after_perm_str == delta_str:
                    isomorphisms.append(tuple((index, j)))
    return isomorphisms

def print_isomorphisms(isomorphisms, deltas):
    for i in range(int(len(isomorphisms)/2)):
        d1 = deltas[isomorphisms[i][0]]
        d2 = deltas[isomorphisms[i][1]]
        print(d1, "<=>", d2)

def print_r(deltas):
    isomorphisms = find_isomorphisms(deltas, n)
    print_isomorphisms(isomorphisms, deltas)

def print_f(code, letter):
    binary_code = []
    for x in code:
        z = list(x)
        z.reverse()
        binary_code.append(''.join(map(str, z)))
    if is_cyclic(code[:-1]):
        binary_code.pop()
    print(letter, *binary_code, sep=" ")

def print_m(code):
    table = []
    for j in range(n-1, -1, -1):
        lst = []
        for x in code:
            lst.append(x[j])
        table.append(list(lst))
    for j in range(len(table)-1, -1, -1):
        if is_cyclic(code[:-1]):
            table[j].pop()
        print(*table[j], sep=" ")

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", help="find and print all the codes (cycles and paths)", action="store_true")
group.add_argument("-b", help="find and print all cyclic Beckett-Gray codes", action="store_true")
group.add_argument("-u", help="find and print all unfinished Beckett-Gray codes", action="store_true")
group.add_argument("-c", help="find and print all cyclic Gray codes", action="store_true")
group.add_argument("-p", help="find and print all Gray paths", action="store_true")
parser.add_argument("-r", help="find and print isomorphisms", action="store_true")
parser.add_argument("-f", help="print complete binary code", action="store_true")
parser.add_argument("-m", help="print code in the form of a table", action="store_true")
parser.add_argument("number_of_bits", type=int, help="number of bits")
args = parser.parse_args()

n = args.number_of_bits
first_gray_code = make_first_gray_code(n)

if args.a:
    all_codes = get_all_gray_codes(first_gray_code)
    deltas = []
    letters = []
    for i in range(0, len(all_codes)):
        letter = 'P'
        if is_cyclic(all_codes[i]):
            all_codes[i].append(all_codes[i][0])
            letter = "C"
        letters.append(letter)
        delta_seq = delta_sequence(all_codes[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        print(letter, delta)
        if args.f:
            print_f(all_codes[i], letters[i])
        if args.m:
            print_m(all_codes[i])
    if args.r:
        print_r(deltas)

elif args.b:
    all_codes = get_all_beckett_gray_codes(first_gray_code)
    cyclic_beckett = []
    for i in range(len(all_codes)):
        if is_cyclic(all_codes[i]):
            all_codes[i].append(all_codes[i][0])
            cyclic_beckett.append(all_codes[i])
    deltas = []
    letters = []
    for i in range(len(cyclic_beckett)):
        delta_seq = delta_sequence(cyclic_beckett[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        letters.append("B")
        print(letters[i], deltas[i])
        if args.f:
            print_f(cyclic_beckett[i], letters[i])
        if args.m:
            print_m(cyclic_beckett[i])
    if args.r:
        print_r(deltas)

elif args.u:
    all_codes = get_all_beckett_gray_codes(first_gray_code)
    non_cyclic_beckett = []
    for i in range(len(all_codes)):
        if not is_cyclic(all_codes[i]):
            non_cyclic_beckett.append(all_codes[i])
    deltas = []
    letters = []
    for i in range(len(non_cyclic_beckett)):
        delta_seq = delta_sequence(non_cyclic_beckett[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        letters.append("U")
        print(letters[i], deltas[i])
        if args.f:
            print_f(non_cyclic_beckett[i], letters[i])
        if args.m:
            print_m(non_cyclic_beckett[i])
    if args.r:
        print_r(deltas)
    
elif args.c:
    all_codes = get_all_gray_codes(first_gray_code)
    cyclic_gray = []
    for i in range(len(all_codes)):
        if is_cyclic(all_codes[i]):
            all_codes[i].append(all_codes[i][0])
            cyclic_gray.append(all_codes[i])
    deltas = []
    letters = []
    for i in range(len(cyclic_gray)):
        delta_seq = delta_sequence(cyclic_gray[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        letters.append("C")
        print(letters[i], deltas[i])
        if args.f:
            print_f(cyclic_gray[i], letters[i])
        if args.m:
            print_m(cyclic_gray[i])
    if args.r:
        print_r(deltas)

elif args.p:
    all_codes = get_all_gray_codes(first_gray_code)
    paths_gray = []
    for i in range(len(all_codes)):
        if not is_cyclic(all_codes[i]):
            paths_gray.append(all_codes[i])
    deltas = []
    letters = []
    for i in range(paths_gray):
        delta_seq = delta_sequence(paths_gray[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        letters.append("P")
        print(letters[i], deltas[i])
        if args.f:
            print_f(paths_gray[i], letters[i])
        if args.m:
            print_m(paths_gray[i])
    if args.r:
        print_r(deltas)

else:
    all_codes = get_all_gray_codes(first_gray_code)
    deltas = []
    letters = []
    for i in range(0, len(all_codes)):
        letter = 'P'
        if is_cyclic(all_codes[i]):
            all_codes[i].append(all_codes[i][0])
            letter = "C"
        letters.append(letter)
        delta_seq = delta_sequence(all_codes[i])
        s = [str(i) for i in delta_seq]
        delta = ''.join(s)
        deltas.append(delta)
        print(letter, delta)
        if args.f:
            print_f(all_codes[i], letters[i])
        if args.m:
            print_m(all_codes[i])
    if args.r:
        print_r(deltas)