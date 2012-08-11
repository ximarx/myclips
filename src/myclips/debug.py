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

def show_wme_details(wme, indent=4, explodeToken=False, maxDepth=3, explodeAMem=False):
    
    assert isinstance(wme, WME)

    IP = "".rjust(indent, ' ')

    tokens = wme.tokens

    print IP, "WME: f-", wme.factId," ", wme.fact
    print IP, "  |- TOKENS: ", len(tokens)
    for token in tokens:
        if not explodeToken:
            print IP, "  :  |- ",str(token)
        else:
            show_token_details(token, indent+8, False, maxDepth-1)
    print IP, "  |- Alpha-Memories: ", len(wme._alphaMemories)
    for am in wme._alphaMemories:
        if not explodeAMem:
            print IP, "  :  |- " ,str(am)
        else:
            show_alphamemory_details(am, indent+8, False, maxDepth-1)
            
def show_alphamemory_details(am, indent=4, explodeWme=False, maxDepth=2):
    
    IP = "".rjust(indent, ' ')
    if maxDepth <= 0:
        print IP, '*** MAX-DEPTH ***'
        return

    assert isinstance(am, AlphaMemory)
    
    print IP, "AlphaMemory: ",repr(am)
    parent = am.rightParent
    pindent = IP
    while parent != None and not isinstance(parent, RootNode):
        print pindent, "  :  |- PARENT:", parent
        pindent += "    "
        parent = parent.rightParent
    
    print IP, "  |- WMES: ", len(am.items)
    for wme in am.items:
        if not explodeWme:
            print IP, "  :  |- ", wme
        else:
            show_wme_details(wme, indent+8, False, maxDepth-1, False)
        
    
def show_token_details(token, indent=4, explodeWme=False, maxDepth=2):
    
    IP = "".rjust(indent, ' ')
    
    if maxDepth <= 0:
        print IP, '*** MAX-DEPTH ***'
        return
    
    assert isinstance(token, Token)
    
    
    
    print IP, "Token: ",str(token)
    print IP, "  |- wme: ", token.wme
    print IP, "  |- node: ", token.node
    print IP, "  |- PARENT: "
    ttok = token.parent
    tindent = IP + "        " 
    while ttok != None:
        print tindent, "  |- Token: ", repr(ttok)
        print tindent, "  :    |- wme: ", ttok.wme
        print tindent, "  :    |- #children: ", len(ttok._children)
        print tindent, "  :    |- node: ", ttok.node
        print tindent, "  :    |- PARENT:"
        tindent = tindent + "            "
        ttok = ttok.parent
    print IP, "  |- CHILDREN: ", len(token._children)
    for subtoken in token._children.values():
        show_token_details(subtoken, indent+8, False, maxDepth-1 )
    print IP, "  |- NEGATIVE-JOIN-RESULTS: ", len(token._negativeJoinResults)
    for res in token._negativeJoinResults:
        print IP, "  :  |- ", res
        print IP, "     :  |- wme: ", res.wme
        print IP, "     :  |- token: ", res.token
    
def draw_network_fragment(pnodes):

    try:
        from myclips.listeners._NetworkPlotterAdapter_NetworkX import _NetworkXWrapper as Plotter
    except ImportError:
        raise Exception()
    
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
            
    g.draw()
        
