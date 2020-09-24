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


def main():
    """
    The main function
    """

    # check no. of arguments provided
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # run untill user exits
    while True:

        # if source or target is not found inform the user and restart
        source = person_id_for_name(input("Name Source: "))
        if source is None:
            print(f"{source} not found.")
            continue
        target = person_id_for_name(input("Name Target: "))
        if target is None:
            print(f"{target} not found.")
            continue

        # check for same name for target and source
        if target == source:
            print("0 degrees of seperation")
            continue

        # finding shortest path
        path = shortest_path(source, target)

        # if path exists then print path
        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        # check if user wants to exit
        choice = input("\nContinue?\n")
        if choice in ['no', 'n', 'No', 'NO', 'N', 'nO']:
            print("Exiting...")
            break


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # initializing the frontier and the first node with source
    node = Node(state=source, parent=None, action=None)
    ds = QueueFrontier()  # frontier
    ds.add(node)
    visited = set()  # keeps track of visited states

    while not ds.empty():
        node = ds.remove()
        visited.add(node.state)

        # check for all neighbors in the popped state
        for movieId, personId in neighbors_for_person(node.state):
            if not ds.contains_state(personId) and personId not in visited:
                newNode = Node(state=personId, parent=node, action=movieId)

                # if the nodes state is equal to target then we found the solution
                if newNode.state == target:
                    solution = solve(newNode, target)
                    print(f'{len(visited)+1} nodes visited')
                    return solution

                # else add the new node to the frontier to traverse later
                ds.add(newNode)

    # if the frontier is exhausted without finding the answer that means that answer doesn't exist
    return None


def solve(node, target):
    """
    Returns the path if solution is found.
    From source to target.
    """

    path = []  # list to store the path from source to target

    # loop from current node which is target, untill parent is not null, since only the source's parent is null
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent

    path.reverse()
    return path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))  # get matching names
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:  # if multiple matches found then let user select
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


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()  # stores the neighbor nodes
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
