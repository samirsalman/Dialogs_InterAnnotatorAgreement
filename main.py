import json
import os


according = []

def read_files(path1, path2):
    f1 = open(path1, "r+")
    f2 = open(path2, "r+")

    return json.load(f1), json.load(f2)


def extract_actions(d1, d2):
    actions1, actions2 = d1["actions"], d2["actions"]

    return [actions1, actions2]


def extract_beliefs(d1, d2):
    beliefs1, beliefs2 = d1["beliefs"], d2["beliefs"]

    return [beliefs1, beliefs2]


def rules_equal(r1, r2, rule_type, dialog):
    j = 0
    for k in r1.keys():
        if r1[k] != r2[k]:
            print(f'Rule type: {rule_type}\nKey: {k}\nR1: {r1[k]}\nR2: {r2[k]}')
            print(25 * '*' + "\n")

            return False
        else:
            according.append({"dialog":dialog, "type":  rule_type, "rule_index" : j})
        j+=1
    return True


def compute_rules(base_path1, base_path2, files1, files2):
    b, a, tot = 0, 0, 0

    for file_i in range(len(files1)):
        print(files1[file_i])
        print(files2[file_i])

        data1, data2 = read_files(base_path1 + files1[file_i], base_path2 + files2[file_i])

        beliefs = extract_beliefs(data1, data2)
        actions = extract_actions(data1, data2)

        for i in range(len(beliefs[0])):
            tot += 1
            if rules_equal(beliefs[0][i], beliefs[1][i], "belief", files1[file_i].split(".")[0]):
                b += 1
            if rules_equal(actions[0][i], actions[1][i], "actions",files1[file_i].split(".")[0]):
                a += 1

    print(f'actions: {a}\nbeliefs: {b}\ntot: {tot}')
    return a, b, tot


def load_files(dir1, dir2):
    return os.listdir(dir1), os.listdir(dir2)


def compute_inter_ann_agreement(set):
    fs1, fs2 = load_files(f"./annotations/michele/{set}/", f"./annotations/samir/{set}/")
    A, B, TOT = compute_rules(f"./annotations/michele/{set}/", f"./annotations/samir/{set}/", fs1, fs2)

    return A/TOT, B/TOT, set


ac, be, set = compute_inter_ann_agreement("small")
print(f"For {set} set\n\nActions agreement:{ac}\nBeliefs agreement:{be}")

small = open("small_results.csv", "w+")
small.write("action_agreement,belief_agreement\n"
            f"{ac},{be}")
small.close()

ac, be, set = compute_inter_ann_agreement("medium")
print(f"For {set} set\n\nActions agreement:{ac}\nBeliefs agreement:{be}")

medium = open("medium_results.csv", "w+")
medium.write("action_agreement,belief_agreement\n"
            f"{ac},{be}")
medium.close()
according_f = open("according.json", "a")
json.dump(according, according_f)