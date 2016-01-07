# author   : Johann-Mattis List
# email    : mattis.list@lingpy.org
# created  : 2015-08-05 20:32
# modified : 2015-08-05 20:32
"""
Script prepares the data for the parsimony experiment on Tukano languages.

What this script basically does is reading in the files on sound changes and
reflexes and creating a weighted network. All data is then stored as JSON, and
JSON is again loaded by the main script that runs the analysis.
"""

__author__="Johann-Mattis List"
__date__="2015-08-05"

from lingpy import *
import networkx as nx
import json

# function to make local graph
def local_graph(changes):
    C = {}
    for line in changes:
        idx, prt, ctx = int(line[0]), line[1], line[2]
        source, target = line[-2].strip(), line[-1].strip()
        if source != target:
            try:
                C[idx, prt, ctx] += [[source, target]]
            except:
                C[idx, prt, ctx] = [[source, target]]
    return C

def global_graph(changes):
    G = nx.DiGraph()
    for line in changes:
        idx, prt, ctx = int(line[0]), line[1], line[2]
        source, target = line[-2].strip(), line[-1].strip()
        if source != target:
            G.add_edge(source, target)
    return G

def get_weight_from_graph(graph, nodeA, nodeB, chars):

    try:
        d = nx.shortest_path_length(graph, nodeA, nodeB)
    except nx.NetworkXNoPath:
        d = len(chars) * 10
    except nx.NetworkXError:
        d = len(chars) * 10

    return d

# get correspondences and changes
corrs = csv2list('D_reflexes.tsv', strip_lines=False)

# load the taxa
tdat = csv2list('D_languages.tsv', strip_lines=False)
taxa = [x[0] for x in tdat[1:]]

# get the header
header = [h.title() for h in corrs[0]]

# get the main data
data = corrs[1:]

# get the proto-data
D = {}
for line in data:
    idx = int(line[0])
    proto = line[1].strip()[1:]
    ctx = line[2]
    refs = [x.strip() for x in line]
    for i,ref in enumerate(refs):
        if '/' in ref:
            nrefs = [x.strip() for x in ref.split('/')]
        else:
            nrefs = [ref]
        refs[i] = nrefs
    
    tmp = dict(
            zip(
                header, 
                refs 
                )
            )
    tmph = sorted([h for h in tmp if h in taxa])
    patterns = [tmp[h] for h in tmph]
    
    D[idx, proto, ctx] = patterns

# load the two different sound change patterns
sc_complex = csv2list('D_changes.tsv')[1:]

# create the digraph
G = nx.DiGraph()

# start compiling the output dictionary to be then formatted to json
out = {}
out['patterns'] = []
out['chars'] = []
out['fitch.chars'] = []
out['fitch'] = []
out['protos'] = []

# we first make all patterns without the proto-forms
protos = sorted(D.keys())
for p in protos:
    
    # get the data
    
    pattern = D[p]
    out['patterns'] += [pattern]
    chars = []
    for px in pattern:
        for c in px:
            chars += [c]

    chars = sorted(set(chars))
    matrix = [[0 for p in chars] for c in chars]
    for i,c1 in enumerate(chars):
        for j,c2 in enumerate(chars):
            if i < j:
                matrix[i][j] = 1
                matrix[j][i] = 1
    out['fitch'] += [matrix]
    out['chars'] += [chars]
    out['fitch.chars'] += [chars]
    out['protos'] += [[p[0],p[1], p[2]]]
out['taxa'] = tmph

# we add three matrix types for now, one complete, one with the full network,
# and one with partial networks
out[''] = [] # ???
out['diwest'] = []
out['sankoff'] = []

# make the dictionary and the graph
CL = local_graph(sc_complex)

for idx, (a, b, c) in enumerate(out['protos']):

    if (a,b,c) in D:
        
        # create graphs for local analyses
        cdl = nx.DiGraph()
        cdl.add_edges_from(CL[a, b, c])
        cul = cdl.to_undirected()

        # all chars we want to consider this time are in the complex undirected
        # graph (but also the complex local graph)
        chars = sorted(cul.nodes())
        nlen = len(chars)
        
        # create the matrices
        m_cdl = [[0 for x in range(nlen)] for y in range(nlen)] # diwest model
        m_cul = [[0 for x in range(nlen)] for y in range(nlen)] # sankoff model


        for i,nA in enumerate(chars):
            for j,nB in enumerate(chars):

                m_cdl[i][j] = get_weight_from_graph(cdl, nA, nB, chars) 
                m_cul[i][j] = get_weight_from_graph(cul, nA, nB, chars) 

        out['diwest']    += [m_cdl]
        out['sankoff']  += [m_cul]
        out['chars'][idx] = chars
    else:
        print(a,b,c)

all_chars = []
for charset in out['chars']:
    all_chars += charset
out['allchars'] = sorted(set(all_chars))
for i,c in enumerate(out['allchars']):
    print(i+1,c)

reflexes = []
for pattern in out['patterns']:
    for p in pattern:
        reflexes += p
out['reflexes'] = sorted(set(reflexes))
for r in out['reflexes']:
    print(r)

with open('I_data.json', 'w') as f:
    f.write(json.dumps(out, indent=2))



