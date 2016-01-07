from lingpy import *
from parsimony import *
from newick import *

matrixA = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
        ]

matrixB = [
        [0, 1, 1],
        [1, 0, 100],
        [1, 100, 0]
        ]

matrixC = [
        [0, 1, 100],
        [100, 0, 100],
        [1, 100, 0]
        ]

matrixD = [
        [0, 1, 100, 100],
        [100, 0, 100, 100],
        [100, 100, 0, 100],
        [1, 100, 1, 0]
        ]

charactersA = ['A','B','C']
charactersB = ['A','B','C','U']
patterns = [[['A'],['B'],['C'],['C']]]
taxa = ['langA', 'langB', 'langC', 'langD']


D = {}
matrices = [[matrixA], [matrixB], [matrixC], [matrixD]]
matrix_names = ['m1', 'm2', 'm3', 'm4']
for i,matrix in enumerate(matrices):
    
    if i < 3:
        trees = heuristic_parsimony(
                taxa,
                patterns,
                matrix,
                [charactersA],
                iterations=20,
                sample_steps=1,
                stop_iteration=True
                )
    else:
        trees = heuristic_parsimony(
                taxa,
                patterns,
                matrix,
                [charactersB],
                iterations=20,
                sample_steps=1,
                stop_iteration=True
                )

    tree_set = trees[0]
    with open(matrix_names[i]+'.tree', 'w') as f:
        for j,tree in enumerate(tree_set):
            if i < 3:
                w,p,r = sankoff_parsimony(
                        patterns[0],
                        taxa,
                        LingPyTree(tree),
                        matrix[0],
                        charactersA
                        )
            else:
                w,p,r = sankoff_parsimony(
                        patterns[0],
                        taxa,
                        LingPyTree(tree),
                        matrix[0],
                        charactersB
                        )
            
            lptree = LingPyTree(tree)

            # create labels
            labels = {}
            _p = dict(p[0])
            for node in lptree.nodes:
                labels[lptree[node]['label']] = _p[node]

            lptree.output('html', filename=matrix_names[i]+'_'+str(j),
                    labels=labels)
            newick_tree = lptree.output('nwk', labels=labels)
            f.write(tree+';\n')
