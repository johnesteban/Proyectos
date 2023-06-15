from scipy.spatial.distance import pdist, squareform
import math 
def dist(positions,n):
    distances = pdist(positions)
    dist_matrix = squareform(distances)

    for i in range(int(n)+1):
        dist_matrix[i,i]=math.inf 
    return dist_matrix