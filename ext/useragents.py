def getUserAgents(ioFile):
    userAgents = []

    with open(ioFile, 'r') as io:
        for agent in io.readlines():
            userAgents.append(agent.strip('\n'))
    return userAgents
