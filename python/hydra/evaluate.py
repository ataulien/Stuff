import parse_numactl


def shortestDistanceFrom(nodeIdx, hardwareInfo):
    """ Returns a list of nodes sorted by their distance to the given node
        Note: This list does contain the given node itself. 
        @param nodeIdx [int] Index of the source-node
        @param hardwareInfo [parse_numactl.HardwareInfo] parsed info from numactl"""

    # Get the list of all nodes this node can reach
    nodes = hardwareInfo.distanceMatrix.nodes[nodeIdx]

    # Zip with their specific index, creating a list like this:
    # [(0, 0.123), (1, 0.432), ...]
    zipped = zip(nodes, range(0, hardwareInfo.nodesAvailable))

    # Sort by distance-key
    zipped = sorted(zipped, key=lambda x: x[0])

    # Unzip that list again
    unzipped = zip(*zipped)

    # Second entry of the unzipped pair does now contain the sorted node-indices
    return unzipped[1]
