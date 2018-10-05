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
    found = False
    while(next_nodes_to_expand):
        current_node = heappop(next_nodes_to_expand)
        if(current_node[1] == destination):
            found = True
            break
        if(current_node[0] == inf):
            break
        if(current_node[1] == initial_position):
            cost[current_node[1]] = 0
        else:
            cost[current_node[1]] = current_node[0]
        neighbours = navigation_edges(graph, current_node[1])
        for node in neighbours:
            if(node[1] == initial_position):
                continue      
            if((node[1] not in cost) or ((node[0] + current_node[0]) < cost[node[1]])):
                parents[node[1]] = current_node[1]
                if((node[1] not in cost) == True):
                    cost[node[1]] = (node[0] + cost[parents[node[1]]])
                heappush(next_nodes_to_expand, ((node[0] + cost[parents[node[1]]]), node[1]))
    if(found == True):
        path_list = []
        while(current_node[1] != initial_position):
            path_list.insert(0, current_node[1])
            current_node = (1,parents[current_node[1]])

        path_list.insert(0, initial_position)
        return path_list
    else:
        return None    

def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    next_nodes_to_expand = []
    heappush(next_nodes_to_expand, (0, initial_position))
    parents = {}
    cost = {}
    while(next_nodes_to_expand):
        current_node = heappop(next_nodes_to_expand)
        if(current_node[0] == inf):
            break
        if(current_node[1] == initial_position):
            cost[current_node[1]] = 0
        else:
            cost[current_node[1]] = current_node[0]
        neighbours = navigation_edges(graph, current_node[1])
        for node in neighbours:
            if(node[1] == initial_position):
                continue      
            if((node[1] not in cost) or ((node[0] + current_node[0]) < cost[node[1]])):
                parents[node[1]] = current_node[1]
                if((node[1] not in cost) == True):
                    cost[node[1]] = (node[0] + cost[parents[node[1]]])
                heappush(next_nodes_to_expand, ((node[0] + cost[parents[node[1]]]), node[1])) 
    return cost

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
        if(i < 0):
            continue
        for j in range(ycoor -1, ycoor +2):
            if(j < 0):
                continue
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
    show_level(level, False)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, True, path)
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
    show_level(level, False)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename1, src_waypoint1, dst_waypoint1 = 'example.txt', 'a','e'
    filename2, src_waypoint2, dst_waypoint2 = 'test_maze.txt', 'a','d'
    filename3, src_waypoint3, dst_waypoint3 = 'my_maze.txt', 'a','e'
    # Use this function call to find the route between two waypoints.
    test_route(filename1, src_waypoint1, dst_waypoint1)
    #test_route(filename2, src_waypoint2, dst_waypoint2)
    #test_route(filename3, src_waypoint3, dst_waypoint3)
    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename1, src_waypoint1, 'my_maze_costs.csv')
