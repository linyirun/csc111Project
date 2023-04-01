from __future__ import annotations
import random
from graph import Graph
from person_edge import Person, INFECTED, SUSCEPTIBLE, RECOVERED
import timeit

NODE_RADIUS = 10

class Simulation:
    simu_graph: Graph
    close_contact_distance: int  # in pixles
    num_family: int
    family_size: int
    frame_num: int
    infected: set
    recover_period: int # in second
    id_to_family: dict[int, list[Person]]

    def __init__(self, num_family: int, family_size: int, speed: float, recover_period: int, initial_infected: int):
        """
        Initialize the simulation class
        Preconditions:
            - initial_infected <= num_family * family_size
        """
        self.close_contact_distance = 100
        self.recover_period = recover_period
        self.simu_graph = Graph()
        self.infected = set()
        self.frame_num = 0
        self.num_family = num_family
        self.family_size = family_size
        self.id_to_family = {}

        person_id = 0
        for i in range(1, num_family+1):
            added = []
            # Create a clique between this family, and add each person in the family to the suspectible
            # set in the graph
            for _ in range(family_size):
                x = random.randint(NODE_RADIUS, 500 - NODE_RADIUS)
                y = random.randint(NODE_RADIUS, 500 - NODE_RADIUS)
                person = Person(x, y, speed, i, person_id)
                person_id += 1
                for one in added:
                    self.simu_graph.build_family_edge(one, person)
                added.append(person)
                self.simu_graph.susceptible.add(person)
                self.simu_graph.id_to_person[person.id] = person
            self.id_to_family[i] = added

        # Randomly choose initial_infected number of people to be infected
        for _ in range(initial_infected):
            to_infect = self.simu_graph.susceptible.pop()
            to_infect.infection_frame = 0
            self.simu_graph.infected.add(to_infect)
            to_infect.state = INFECTED

    def frame(self):
        self.frame_num += 1
        if len(self.simu_graph.recovered) < self.num_family * self.family_size:
            #move
            for person in self.simu_graph.infected | self.simu_graph.susceptible | self.simu_graph.recovered:
                person.make_move()
            #infect
            for person in self.infected:
                if person is None:
                    continue
                person.state = INFECTED
                person.infection_frame = self.frame_num
                self.simu_graph.infected.add(person)
            self.simu_graph.update_edge(self.frame_num, self.recover_period, self.close_contact_distance)
            self.infected = self.simu_graph.make_infection(self.close_contact_distance)
        else:
            print('Done')


if __name__ == '__main__':
    x = timeit.timeit()
