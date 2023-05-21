# CPS workflow

## World 


## Agents
Universal parameters:
problem_solving
communication

role_taking (2-4)
role_distribution (3-4)
conflict_negotiation (3-4)
conflict_resolve (4)


Level 1

Level 2

Level 3
role_distributed=1

Level 4
=1





## Teams are formed

## Problems
A team is posed with a problem with Task_complexity (1:3) and Size (1000)


Then we distribute role: 1 to len(team) (Do you fulfill your role or not?)
- each is assigned a "correct" role
- Then roles are more probable to become correct based on lvl2-4

- If Lvl 3/4 then roles are distributed correctly/evenly at first
- Self.Role=X

First we try to generate common-ground:
- Based on agents Communication parameter
- Common_ground = 0 or 1

Then we simulate role_alignment:
- There some 0.8 prob that role stays correct
- Theres some 0.2 prob that role might shift to incorrect

Then Solutions are generated:
- generate some 50 to 150 solution (based on problem_solving)
- If lvl doesnt match task lvl then solution cannot be given

If some role > 1:
- Then conflict appears

If common_ground=0
- Lowest solution is chosen

If all roles are evenly distributed and common ground = 1:
    Then choose the 

Adjustement of error/Meta negotiations/Self and team monitoring:
- Resolve_conflict
    - 50% prob of conflict resolvement
    - 90% if lvl 3 is present
- Reach_common_ground
    - 






def team(self):

    team_size_min, team_size_max = 2, 5

    neighbor_nodes = self.model.network.get_neighbors(node, include_center=False)
    neighbors = self.model.network.get_cell_list_contents(neighbor_nodes)

    team_id

    for neighbor in neighbors:
        connection_strength = (self.communication + neighbor.communication) / 2
        if len(team_members) < team_size_max and connection_strength > 0.5 and neighbor not in team_members and neighbor.unique_id not in [agent.unique_id for team in self.model.teams.values() for agent in team] and:


    while remaining_neighbors > 0 and len(self.team_members) < team_size_max:
        for neighbor in neighbors:
            connection_strength = (self.communication + neighbor.communication) / 2
            if len(self.team_members) < team_size_max and connection_strength > 0.5:
                if len(self.team_members) == team_size_min - 1:
                    # Check if neighbor is in a team of size 2
                    for team in self.model.teams.values():
                        if len(team) == team_size_min and neighbor in team:
                            # Merge the teams
                            self.team_members += team
                            self.model.teams.pop(team_id)
                            break
                elif neighbor not in self.team_members and neighbor.unique_id not in [agent.unique_id for team in self.model.teams.values() for agent in team]:
                    self.team_members.append(neighbor)
                    remaining_neighbors -= 1


        team_size_min, team_size_max = 2, 5

        node = self.unique_id
        neighbor_nodes = self.model.network.get_neighbors(node, include_center=False)
        neighbors = self.model.network.get_cell_list_contents(neighbor_nodes)

        remaining_neighbors = len(neighbors)

        team_members = []

        while remaining_neighbors > 0 and len(team_members) < team_size_max:
            for neighbor in neighbors:
                connection_strength = (self.communication + neighbor.communication) / 2
                if len(team_members) < team_size_max and connection_strength > 0.5:
                     if neighbor.team_id > -1: 
                        if(len(team_members) < (team_size_max/2) and len(self.model.teams[neighbor.team_id]) < (team_size_max / 2):
                            self.team_members += neighbor.team_members
                            for member in neighbor.team_members:
                                member.team_id = self.team_id
                            self.model.teams.pop(neighbor.team_id)

                     elif neighbor.team_id < 0:
                        team_members.append(neighbor)
                remaining_neighbors -= 1

            if len(team_members) < team_size_min and self.model.team_id == -1:
                team_id = len(self.model.teams) + 1 
                self.team_id = team_id
                
                self.model.teams[team_id] = team_members
                # print team 
                print("Team", team_id, "formed:", [member.unique_id for member in self.team_members])
    