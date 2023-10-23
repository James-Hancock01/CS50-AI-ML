import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main(directory):
    source = None
    target = None

    while source is None or target is None:
        source = person_id_for_name(input("\nName: "))
        if source is None:
            print("Person not found.")
            #sys.exit("Person not found.")

        target = person_id_for_name(input("Name: "))
        if target is None:
            print("Person not found.")
            # sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"\n{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # TODO
    states_explored = 0
    explored = set()
    solution = set()

    start = Node(source, None, None)
    Frontier = QueueFrontier()
    Frontier.add(start)

    neighbours_list = neighbours_for_person(source)  # list of all the neighbours [(movie_id,person_id),...]

    while True:
        if Frontier.empty():
            return None
            # raise Exception("no solution")


        # taking a node out the frontier
        node = Frontier.remove()
        states_explored += 1

        if node.state == target:    # is the node the target?
            solution = return_path(node)
            return solution

        # mark node as explored
        explored.add(node.state)

        # add neighbours to frontier
        for action, state in neighbours_for_person(node.state):
            if not Frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                if state != target: #is the child the target? if so the end has been found
                    Frontier.add(child)
                else:
                    return return_path(child)

def return_path(node):
    actions = []
    cells = []

    # now backtrack to produce list of nodes passed through

    while node.parent is not None:
        actions.append(node.action)
        cells.append(node.state)
        node = node.parent

    # at initial state            actions.reverse()
    cells.reverse()
    solution = list(zip(actions, cells))
    #print(solution)

    return solution

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbours_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbours = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbours.add((movie_id, person_id))
    return neighbours

if __name__ == "__main__":

    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    directory = None
    while directory is None:
        size = input("small (s) or large (l) dataset?   ")
        if size.lower() == "l":
            directory = "large"
        else:
            directory = "small"

    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    # directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    while True:
        main(directory)
