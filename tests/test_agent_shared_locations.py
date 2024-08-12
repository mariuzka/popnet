import popy


def test_1a():

    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class Meeting1(popy.MagicLocation):
        pass

    class Meeting2(popy.MagicLocation):
        pass

    model = popy.Model()
    agent_max = Max(model = model)
    agent_marius = Marius(model = model)
    agent_lukas = Lukas(model = model)
    meeting1 = Meeting1(model = model)
    meeting2 = Meeting2(model = model)
    meeting1.add_agents(agents = [agent_max, agent_marius])
    meeting2.add_agents(agents = [agent_marius, agent_lukas])

    assert len(model.locations) == 2
    assert len(model.agents) == 3
    
    assert agent_max.shared_locations(agent=agent_marius)[0].type == "Meeting1"
    assert not bool(agent_max.shared_locations(agent=agent_lukas))
   
    assert agent_marius.shared_locations(agent=agent_max)[0].type == "Meeting1"
    assert agent_marius.shared_locations(agent=agent_lukas)[0].type == "Meeting2"
    
    assert agent_lukas.shared_locations(agent=agent_marius)[0].type == "Meeting2"
    assert not bool(agent_lukas.shared_locations(agent=agent_max))



def test_1b():
    model = popy.Model()
    creator = popy.Creator(model = model)

    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class Meeting1(popy.MagicLocation):
        def filter(self, agent):
            return agent.type in ["Max", "Marius"]

    class Meeting2(popy.MagicLocation):
        def filter(self, agent):
            return agent.type in ["Marius", "Lukas"]

    _max = creator.create_agents(agent_class=Max, n=1)[0]
    _marius = creator.create_agents(agent_class=Marius, n=1)[0]
    _lukas = creator.create_agents(agent_class=Lukas, n=1)[0]
    creator.create_locations(location_classes=[Meeting1, Meeting2])

    assert len(model.locations) == 2
    assert len(model.agents) == 3
    
    assert _max.shared_locations(agent=_marius)[0].type == "Meeting1"
    assert not bool(_max.shared_locations(agent=_lukas))
    
    assert _marius.shared_locations(agent=_max)[0].type == "Meeting1"
    assert _marius.shared_locations(agent=_lukas)[0].type == "Meeting2"
    
    assert _lukas.shared_locations(agent=_marius)[0].type == "Meeting2"
    assert not bool(_lukas.shared_locations(agent=_max))