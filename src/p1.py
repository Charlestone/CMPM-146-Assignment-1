from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush, heapify


#I worked with Carlos del Rey
#I also used the wikipedia

#Core functions
def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    next_nodes_to_expand = []
    heappush(next_nodes_to_expand, (0, initial_position))

    parents = {}
    cost = {}

    cost[initial_position] = 0

    found = False

    print(next_nodes_to_expand)
    while(next_nodes_to_expand):
        print('bish what')
        current_node = heappop(next_nodes_to_expand)

        if(current_node[1] == destination):
            found = True
            break

        neighbours = navigation_edges(graph, current_node[1])
        for node in neighbours:
            if(node[1] == initial_position):
                continue
            #if they're already in heap
            print('PRINTING PARENT')
            print(parents)
            print('PRINTING COST')
            print(cost)       
            if((node[1] not in cost) or ((node[0] + cost[parents[node[1]]])< cost[node[1]])):
                cost[node[1]] = node[0]
                parents[node[1]] = current_node[1]
                heappush(next_nodes_to_expand, (cost[node[1]] + node[0], node[1]))

    print(parents)

    if(found == True):
        path_list = []
        while(current_node[1] != initial_position):
            path_list.insert(0, current_node[1])
            current_node = (1,parents[current_node[1]])

        path_list.insert(0, initial_position)
        print(path_list)
        return path_list
    else:
        return None    

    # #Heap for the nodes we are going to expand
    #next_nodes_to_expand = []
    # #We push the initial node into the heap
    # heappush(next_nodes_to_expand, (0, initial_position))
    # #dict for the parent of the nodes
    # parents = {}
    # #Variable to check wheter we have foun the solution or not
    # found = False
    # #while loop
    # while(len(next_nodes_to_expand) != 0):
    #     #We extract the ne
    #     current_node = heappop(next_nodes_to_expand)
    #     currcost, currpos = current_node
    #     #print( currpos)
    #     if(currpos == destination):
    #         found = True
    #         break
    #     neighbours = navigation_edges(graph, currpos)
    #     for aux in neighbours:
    #         #cost and position of neighbor node
    #         auxcost, auxpos = aux

    #         #if node is inside the heap
    #         if(aux in next_nodes_to_expand):
    #             #NEW: if neighbour is parent, then skip
    #             if(parents[auxpos][1] == initial_position):
    #                 continue

    #             # if(auxpos in parents == False):
    #             #     heappush(next_nodes_to_expand, (auxcost, auxpos))
    #             #     parents[auxpos] = current_node
    #             #     continue
    #             #print('this is aux')
    #             #print(aux)
    #             #get the node's index in the heap
    #             index = next_nodes_to_expand.index(aux)

    #             #get the cost and position of whatever's in the index from heap
    #             cost, pos = next_nodes_to_expand[index]

    #             #NEW: get the neighbor node's parent's index
    #             #trying to access something that's not there anymore
    #             #whenever we pop things off, we lose track of their costs
    #             #print(parents)
    #             # parent_index = next_nodes_to_expand.index(parents[auxpos])
    #             # parcost, parpos = next_nodes_to_expand[parent_index]

    #             #NEW: we don't need to access heap because parent dictionary
    #             #stores the node's parent's cost and position anyways
    #             parcost, parpos = parents[auxpos]
    #             if( cost > auxcost + parcost):
    #                 next_nodes_to_expand[index] = (auxcost + parcost, auxpos)
    #                 heapify(next_nodes_to_expand)
    #                 parents[auxpos] = current_node
    #         else:
    #             heappush(next_nodes_to_expand, (auxcost + currcost, auxpos))
    #             #print((auxcost + currcost, auxpos))
    #             parents[auxpos] = current_node


    # if(found == True):
    #     print(parents)
    #     pathlist = []
    #     start_position = currpos
    #     counter = 0
    #     while(start_position != initial_position):
    #         pathlist.insert(0, start_position)
    #         start_position = parents[start_position][1]
    #         counter += 1
    #         if(counter == 30):
    #             print(pathlist)
    #             break

    #     # while(currpos != initial_position):
    #     #     print('current position')
    #     #     print(currpos)
    #     #     print('initial_position')
    #     #     print(initial_position)

    #     #     #NEW:insert the position
    #     #     pathlist.insert(0, currpos)
    #     #     currpos = parents[currpos][1]
            
    #     # return pathlist
    # else:
    #     return None




def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    neighbours = []
    xcoor, ycoor = cell
    for i in range(xcoor -1, xcoor +2):
        for j in range(ycoor -1, ycoor +2):
            #We don't want to include the current node in the list of neighbours
            if(i != xcoor or j != ycoor):

                if(((i,j) in level['walls']) == False):
                    distance = sqrt(abs(i-xcoor)+abs(j-ycoor))
                    cost = level['spaces'][(i,j)]*(distance/2) + level['spaces'][cell]*(distance/2)
                else:
                    cost = inf
                neighbours.append((cost, (i,j)))

    return neighbours


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    #cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
