# %%
from collections import Counter

import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(popy.MagicLocation):
        n_agents = 2

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def nest(self):
            return School

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 4

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 2
        if location.type == "Classroom":
            assert len(location.agents) == 2

    for agent in model.agents:
        assert (
            agent.neighbors(location_classes=[Classroom])[0]
            is agent.neighbors(location_classes=[School])[0]
        )

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()


test_1()


# %%


def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "group": [1, 2, 1, 2, 1, 2, 1, 2],
            "_id": [1, 2, 3, 4, 5, 6, 7, 8],
        }
    )

    class School(popy.MagicLocation):
        n_agents = 4

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.group

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 8
    assert len(model.locations) == 6

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert not all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.type == "Classroom"
    )

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="id")

    class School(popy.MagicLocation):
        n_agents = 4

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.group

        def nest(self):
            return School

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 8
    assert len(model.locations) == 6
    assert all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.type == "Classroom"
    )

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="group")

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
        if location.type == "Classroom":
            assert len(location.agents) == 2

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert any(
        agent.neighbors(location_classes=[Classroom])
        not in agent.neighbors(location_classes=[School])
        for agent in model.agents
    )

    for location in model.locations:
        if location.type == "School":
            for agent in location.agents:
                assert all(agent.School == nghbr.School for nghbr in agent.neighbors())


test_2()

# %%


def test_3():
    class City(popy.MagicLocation):
        n_agents = 4

    class Group(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.group

    model = popy.Model()
    creator = popy.Creator(model=model)

    for i in range(8):
        agent = popy.Agent(model=model)
        agent.group = i % 2

    creator.create_locations(location_classes=[City, Group])

    for location in model.locations.select(model.locations.type == "City"):
        assert int(location.agents[0].group) == 0
        assert int(location.agents[1].group) == 1
        assert int(location.agents[2].group) == 0
        assert int(location.agents[3].group) == 1

    for location in model.locations.select(model.locations.type == "Group"):
        assert location.agents[0].group == location.agents[1].group

    # not all members of the same group are also in the same city (which is not desired)
    assert not all(
        location.agents[0].City == location.agents[1].City for location in model.locations
    )

    class GroupNestedInCity(Group):
        def nest(self):
            return City

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create_locations(location_classes=[City, GroupNestedInCity])

    for location in model.locations.select(model.locations.type == "City"):
        assert int(location.agents[0].group) == 0
        assert int(location.agents[1].group) == 1
        assert int(location.agents[2].group) == 0
        assert int(location.agents[3].group) == 1

    for location in model.locations.select(model.locations.type == "Group"):
        assert location.agents[0].group == location.agents[1].group

    # all members of a group are in the same city
    assert all(location.agents[0].City == location.agents[1].City for location in model.locations)


test_3()
