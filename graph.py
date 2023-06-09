"""
The graph class
This class stores the people who are uninfected, infected, and recovered, as well
as a mapping from the person id to the person.
"""

from __future__ import annotations
# from python_ta.contracts import check_contracts
from person_edge import Person, RECOVERED, Edge


# @check_contracts
class Graph:
    """This is the Graph contaning all the Persons in the simulation. The Graph class also keeps track of all the
    Person who are Infected, Susceptible or recovered.

    Instance Attributes:
    - infected: a set containing all the Person who are infected.
    - susceptible: a set containing all the Person who could be infected in future.
    - recovered: a set containing all the Person who have recovered and can not be infeced again.
    - id_to_person: a dictionary contanning all the Person with the id of Person as key and Person object as
    associated values.
    - infectivity: The rate of infection in the simulation

    Representation Invarients:
    - all(person in self.id_to_person.values() for person in self.infected)
    - all(person in self.id_to_person.values() for person in self.susceptible)
    - all(person in self.id_to_person.values() for person in self.recovered)
    - all(self.id_to_person[identification].id == identification for identification in self.id_to_person)
    """
    infected: set[Person]
    susceptible: set[Person]
    recovered: set[Person]
    id_to_person: dict[int, Person]
    infectivity: float

    def __init__(self, infectivity: float) -> None:
        """This function inicilize the Graph class by making it to an empty graph."""
        self.infected = set()
        self.susceptible = set()
        self.recovered = set()
        self.id_to_person = {}
        self.infectivity = infectivity

    def build_family_edge(self, person1: Person, person2: Person) -> None:
        """This fucntion build an family edge between person1 and person2.

        - Preconditions:
            - person1.family_id == person2.family_id
        """
        edge = Edge(person1, person2)
        person1.family[person2.id] = edge
        person2.family[person1.id] = edge

    def update_edge(self, current_frame: int, recover_period: int, close_contact_distance: int) -> None:
        """This function updates the all the close contact edge in the simulation. This includes break the existing
        edges if the distance between two Person is larger than close_contact_distance and adding an edge between
        two Person if the distance between them is less than close_contact_distance.
        """
        to_remove = set()
        for patient in self.infected:
            patient.close_contact = {}
            if current_frame - patient.infection_frame > recover_period:
                patient.state = RECOVERED
                to_remove.add(patient)
            else:
                for person in self.susceptible:
                    if ((person.location[0] - patient.location[0]) ** 2 + (
                            person.location[1] - patient.location[1]) ** 2) ** 0.5 < close_contact_distance or \
                            person.family_id == patient.family_id:
                        patient.create_close_contact_edge(person)

        for patient in to_remove:
            self.infected.remove(patient)
            self.recovered.add(patient)

    def make_infection(self, close_contact_distance: int) -> set[Person]:
        """return all the newly infected people under the current connection of graph. This fuction make all the
        infected person spread virus by calling Edge.infect.

         - Preconditions:
            close_contact_distance >= 0
        """
        newly_infected = set()
        for patient in self.infected:
            for family_edge in patient.family.values():
                potencial_infect = family_edge.infect(close_contact_distance, self.infectivity)
                if potencial_infect is not None:
                    newly_infected.add(potencial_infect)
            for edge in patient.close_contact.values():
                value = edge.infect(close_contact_distance, self.infectivity)
                if value is not None and value.family_id != patient.family_id:
                    newly_infected.add(value)
        return newly_infected


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['E9999', 'R1702'],
        'max-line-length': 120
    })
