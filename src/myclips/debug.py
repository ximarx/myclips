'''
Created on 17/mag/2012

@author: Francesco Capozzo
'''
from myclips.rete.WME import WME
from myclips.rete.nodes.AlphaMemory import AlphaMemory
from myclips.rete.nodes.RootNode import RootNode
from myclips.rete.Token import Token
from myclips.rete.Node import Node
from myclips.rete.BetaInput import BetaInput
from myclips.rete.nodes.NccNode import NccNode

def show_wme_details(stream, wme, indent=4, explodeToken=False, maxDepth=3, explodeAMem=False):
    '''
    Write the stream a group of details about a wme
    
    @param stream: the stream to write to
    @type stream: stream like instance
    @param wme: a wme
    @type wme: L{WME}
    @param indent: number of white space before the text
    @type indent: integer
    @param explodeToken: show details about linked tokens
    @type explodeToken: boolean
    @param maxDepth: a depth bound for recursions
    @type maxDepth: integer
    @param explodeAMem: show details about linked amem
    @type explodeAMem: boolean
    '''
    
    assert isinstance(wme, WME)

    IP = "".rjust(indent, ' ')

    tokens = wme.tokens

    print >> stream, IP, "WME: f-", wme.factId," ", wme.fact
    print >> stream, IP, "  |- TOKENS: ", len(tokens)
    for token in tokens:
        if not explodeToken:
            print >> stream, IP, "  :  |- ",str(token)
        else:
            show_token_details(stream, token, indent+8, False, maxDepth-1)
    print >> stream, IP, "  |- Alpha-Memories: ", len(wme._alphaMemories)
    for am in wme._alphaMemories:
        if not explodeAMem:
            print >> stream, IP, "  :  |- " ,str(am)
        else:
            show_alphamemory_details(stream, am, indent+8, False, maxDepth-1)
            
def show_alphamemory_details(stream, am, indent=4, explodeWme=False, maxDepth=2):
    '''
    Write to stream info about the alpha memory contents
    
    @param stream: the stream to write to
    @type stream: stream
    @param am: the alpha memory
    @type am: L{AlphaMemory}
    @param indent: number of whitespace before the text
    @type indent: integer
    @param explodeWme: show info about linked wme
    @type explodeWme: boolean
    @param maxDepth: max depth bound for recursion
    @type maxDepth: integer
    '''
    
    IP = "".rjust(indent, ' ')
    if maxDepth <= 0:
        print >> stream, IP, '*** MAX-DEPTH ***'
        return

    assert isinstance(am, AlphaMemory)
    
    print >> stream, IP, "AlphaMemory: ",repr(am)
    parent = am.rightParent
    pindent = IP
    while parent != None and not isinstance(parent, RootNode):
        print >> stream, pindent, "  :  |- PARENT:", parent
        pindent += "    "
        parent = parent.rightParent
    
    print >> stream, IP, "  |- WMES: ", len(am.items)
    for wme in am.items:
        if not explodeWme:
            print >> stream, IP, "  :  |- ", wme
        else:
            show_wme_details(stream, wme, indent+8, False, maxDepth-1, False)
        
    
def show_token_details(stream, token, indent=4, explodeWme=False, maxDepth=2):
    '''
    Write to stream infos about a Token
    
    @param stream: the stream to write to
    @type stream: stream
    @param token: a token
    @type token: L{Token}
    @param indent: whitespaces before the text
    @type indent: integer
    @param explodeWme: show info about linked wmes
    @type explodeWme: boolean
    @param maxDepth: max recursions bound
    @type maxDepth: integer
    '''
    
    IP = "".rjust(indent, ' ')
    
    if maxDepth <= 0:
        print >> stream, IP, '*** MAX-DEPTH ***'
        return
    
    assert isinstance(token, Token)
    
    
    
    print >> stream, IP, "Token: ",str(token)
    print >> stream, IP, "  |- wme: ", token.wme
    print >> stream, IP, "  |- node: ", token.node
    print >> stream, IP, "  |- PARENT: "
    ttok = token.parent
    tindent = IP + "        " 
    while ttok != None:
        print >> stream, tindent, "  |- Token: ", repr(ttok)
        print >> stream, tindent, "  :    |- wme: ", ttok.wme
        print >> stream, tindent, "  :    |- #children: ", len(ttok._children)
        print >> stream, tindent, "  :    |- node: ", ttok.node
        print >> stream, tindent, "  :    |- PARENT:"
        tindent = tindent + "            "
        ttok = ttok.parent
    print >> stream, IP, "  |- CHILDREN: ", len(token._children)
    for subtoken in token._children.values():
        show_token_details(subtoken, indent+8, False, maxDepth-1 )
    print >> stream, IP, "  |- NEGATIVE-JOIN-RESULTS: ", len(token._negativeJoinResults)
    for res in token._negativeJoinResults:
        print >> stream, IP, "  :  |- ", res
        print >> stream, IP, "     :  |- wme: ", res.wme
        print >> stream, IP, "     :  |- token: ", res.token
    
def prepare_network_fragment_plotter(pnodes):
    '''
    Navigates circuits of pnode in pnodes
    preparing a new instance of network plotter
    
    @param pnodes: a list of L{PNode}
    @type pnodes: list
    @rtype: NetworkPlotter
    @raise Exception: if no plotter class is available 
    '''

    try:
        from myclips.listeners._NetworkPlotterAdapter_NetworkX import _NetworkXWrapper as Plotter
    except ImportError, e:
        raise Exception("Matplotlib missing!")
    
    g = Plotter()
    
    visited = set()
    links = set()
    nodeStack = pnodes 
    
    while len(nodeStack) > 0:
        child = nodeStack.pop()
        
        assert isinstance(child, Node)
        
        if child not in visited:
            g.add_node(child)
            visited.add(child)
        if not child.isLeftRoot():
            if child.leftParent not in visited:
                g.add_node(child.leftParent)
                visited.add(child.leftParent)
            if (child, child.leftParent) not in links:
                g.add_edge(child, child.leftParent, -1 )
                links.add((child, child.leftParent))
        if not child.isRightRoot():
            if child.rightParent not in visited:
                g.add_node(child.rightParent)
                visited.add(child.rightParent)
            if (child, child.rightParent) not in links:
                g.add_edge(child, child.rightParent, 1 if isinstance(child, BetaInput) else 0 )
                links.add((child, child.rightParent))
        
        # special case: ncc nodes
        if isinstance(child, NccNode):
            assert isinstance(child, NccNode)
            if child.partner not in visited:
                g.add_node(child.partner)
                visited.add(child.partner)
            if (child, child.partner) not in links:
                g.add_edge(child, child.partner, 0)
                links.add((child, child.partner))
            
            nodeStack.append(child.partner)
                
        # inserisco prima il padre destro e poi il sinistro
        # perche voglio che la navigazione proceda prima
        # risalendo a sinistra
        if not child.isRightRoot():
            nodeStack.append(child.rightParent)
            
        if not child.isLeftRoot():
            nodeStack.append(child.leftParent)
            
    #g.draw()
    return g

def draw_network_fragment(pnodes):
    '''
    Draw circuits of pnode in pnodes
    @param pnodes: a list of L{PNode}
    @type pnodes: list
    '''
    
    
    prepare_network_fragment_plotter(pnodes).draw()
        
