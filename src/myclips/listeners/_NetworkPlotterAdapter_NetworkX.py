'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
from myclips.EventsManager import EventsManager
import networkx as nx
import matplotlib.pyplot as plt
from myclips.rete.HasTests import HasTests
from myclips.rete.Memory import Memory
from myclips.listeners.EventsManagerListener import EventsManagerListener
from myclips.rete.HasJoinTests import HasJoinTests


class _NetworkPlotterAdapter_NetworkX(EventsManagerListener):
    '''
    classdocs
    '''
    
    _WRAPPER = None

    def __init__(self, *args, **kargs):
        '''
        Constructor
        '''
        EventsManagerListener.__init__(self, {
                EventsManager.E_NODE_ADDED: self.onNodeAdded,
                EventsManager.E_NODE_REMOVED: self.onNodeRemoved,
                EventsManager.E_NODE_LINKED: self.onNodeLinked,
                EventsManager.E_NODE_UNLINKED: self.onNodeUnlinked,
                EventsManager.E_NETWORK_READY: self.onNetworkReady,
                EventsManager.E_NETWORK_SHUTDOWN: self.onNetworkShutdown,
            })
        
        self._wrapper = self.__class__._WRAPPER()
        
    @classmethod
    def useWrapper(cls, wrapperClass):
        cls._WRAPPER = wrapperClass
        return cls
    
    def __repr__(self, *args, **kwargs):
        return "<NetworkPlotter: adapter=NetworkX, wrapper=%s>"%repr(self._wrapper)
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onNodeAdded(self, theNode):
        self._wrapper.add_node(theNode)
    
    def onNodeRemoved(self, theNode):
        self._gWrapper.remove_node(theNode)
    
    def onNodeLinked(self, theParent, theNode, linkType=0):
        self._wrapper.add_edge(theNode, theParent, linkType)
    
    def onNodeUnlinked(self, theParent, theNode):
        self._wrapper.remove_edge(theNode, theParent)
        
    def onNetworkReady(self, network):
        self._wrapper.draw()
        
    def onNetworkShutdown(self, network):
        self._wrapper.clear()
    
class _NetworkXWrapper(object):
    
    def __init__(self):
        self._reinit()

    def _reinit(self):
        
        self._nodemap = {}
        self._edgemap = {}
        self._G = None
        self._nodeid = 1
        
        G = nx.DiGraph()
        self._G = G
            
            
    def add_node(self, node, parent=None, linkType=0):
        
        if not self._nodemap.has_key(node):
            
            # nuovo nodo
            self._nodemap[node] = self._nodeid
            self._G.add_node(self._nodeid,attr_dict={
                    'type': str(node.__class__.__name__).split(".")[-1],
                    'ref': node
                })
            if isinstance(node, (HasTests, HasJoinTests)):
                tests = node.tests
                self._G.node[self._nodeid]['tests'] = [str(t) for t in tests]
             
            if str(node.__class__.__name__).split(".")[-1] == "RootNode":
                self._G.node[self._nodeid]['label'] = 'ROOT'

            #if str(node.__class__.__name__).split(".")[-1] == "PropertyTestNode":
                #self._G.node[self._nodeid]['label'] = "Propert"

            if str(node.__class__.__name__).split(".")[-1] == "PNode":
                self._G.node[self._nodeid]['label'] = node.ruleName

            if isinstance(node, Memory):
                self._G.node[self._nodeid]['dyn_label'] = lambda ref:'[{0}]'.format(len(ref.items))


            parent_id = None
            if parent != None:
                parent_id = self._nodemap.get(parent, None)
            if parent_id != None:
                self.add_edge(parent_id, self._nodeid, linkType )
            
            self._nodeid += 1
                
        return self._nodemap[node]
    
    def remove_node(self, node):
        if self._nodemap.has_key(node):
            nodeId = self._nodemap[node]
            self._G.remove_node(nodeId)
            del self._nodemap[node]

    def add_edge(self, child, parent, linkType=0):
        
        if child == None or parent == None:
            return
        
        if self._nodemap.has_key(child):
            child = self._nodemap[child]
        else:
            self.add_node(child)
            child = self._nodemap[child]
            
        if self._nodemap.has_key(parent):
            parent = self._nodemap[parent]
        else:
            self.add_node(parent)
            parent = self._nodemap[parent]
        
        self._G.add_edge(child, parent)
        
        self._G.edge[child][parent]["type"] = linkType

    def remove_edge(self, child, parent):
        if self._nodemap.has_key(child):
            child = self._nodemap[child]
        else:
            return
        if self._nodemap.has_key(parent):
            parent = self._nodemap[parent]
        else:
            return
        
        self._G.remove_edge(child, parent)
            
            
    def _prepare_draw(self, resolveDynamic=False):
        
        G = self._G
                
        eright=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] > 0]
        eleft=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] < 0]
        enormal=[(u,v) for (u,v,d) in G.edges(data=True) if d['type'] == 0]
        
        nroots=[n for (n,d) in G.nodes(data=True) if d['type'] == 'RootNode']
        namems=[n for (n,d) in G.nodes(data=True) if d['type'] == 'AlphaMemory']
        nctns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'PropertyTestNode']
        nbmems=[n for (n,d) in G.nodes(data=True) if d['type'] == 'BetaMemory']
        njns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'JoinNode']
        npnodes=[n for (n,d) in G.nodes(data=True) if d['type'] == 'PNode']
        nnjns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NegativeJoinNode']
        fns=[n for (n,d) in G.nodes(data=True) if d['type'] == 'TestNode']
        nccs=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NccNode']
        nccps=[n for (n,d) in G.nodes(data=True) if d['type'] == 'NccPartnerNode']
        
        if resolveDynamic:
            for n,d in G.nodes(data=True):
                
                if d.has_key('label') and d.has_key('dyn_label') and callable(d['dyn_label']):
                    d['label'] = "\\n".join([d['label'], d['dyn_label'](d['ref'])])
                    del d['dyn_label']
                    
                elif d.has_key('dyn_label') and callable(d['dyn_label']):
                    d['label'] = d['dyn_label'](d['ref'])
                    del d['dyn_label']
                    
                if d.has_key('label') and d.has_key('tests') and len(d['tests']) > 0:
                    d['label'] = "\\n".join([d['label'], "\\n".join(d['tests'])])
                    del d['tests']
                    
                elif d.has_key('tests') and len(d['tests']) > 0:
                    d['label'] = "\\n".join(d['tests'])
                    del d['tests']


        ltests=dict([(n,"\n".join(d['tests'])) for (n,d) in G.nodes(data=True) if d.has_key('tests') and len(d['tests']) > 0])
        llabels=dict([(n,d['label']) for (n,d) in G.nodes(data=True) if d.has_key('label') and not d.has_key('dyn_label')])
        lbothlabels=dict([(n,"\n".join([d['dyn_label'](d['ref']), d['label']])) for (n,d) in G.nodes(data=True) if d.has_key('label') and d.has_key('dyn_label') and callable(d['dyn_label'])])
        ldynlabels=dict([(n,d['dyn_label'](d['ref'])) for (n,d) in G.nodes(data=True) if d.has_key('dyn_label') and ( not d.has_key('label') ) and callable(d['dyn_label'])])


        try:
            # graphviz needed, otherwise use sprint_layout
            pos = nx.graphviz_layout(G, root=nroots[0]) # positions for all nodes
        except ImportError:
            pos = nx.spring_layout(G)
            
        
        # nodes
        #nx.draw_networkx_nodes(G,pos,node_size=600)

        # differenzio i nodi per tipo
        # ROOT
        nx.draw_networkx_nodes(G,pos,nodelist=nroots,
                               node_size=1000,alpha=0.7)
        
        # CONSTANT TEST NODE
        nx.draw_networkx_nodes(G,pos,nodelist=nctns,
                               node_size=600,alpha=0.7,node_color='w')

        # ALPHA MEMORIES
        nx.draw_networkx_nodes(G,pos,nodelist=namems,
                               node_size=600,alpha=0.7,node_color='y',node_shape='s')
        
        # JOINS
        nx.draw_networkx_nodes(G,pos,nodelist=njns,
                               node_size=900,alpha=0.7,node_color='w',node_shape='v')

        # BETA MEMORIES
        nx.draw_networkx_nodes(G,pos,nodelist=nbmems,
                               node_size=600,alpha=0.7,node_color='r',node_shape='s')
        
        # NEGATIVE JOINS
        nx.draw_networkx_nodes(G,pos,nodelist=nnjns,
                               node_size=900,alpha=0.7,node_color='w',node_shape='^')
        
        # FILTER NODES
        nx.draw_networkx_nodes(G,pos,nodelist=fns,
                               node_size=900,alpha=0.7,node_color='g',node_shape='p')
        
        # NCC-NODES
        nx.draw_networkx_nodes(G,pos,nodelist=nccs,
                               node_size=600,alpha=0.7,node_color='g',node_shape='s')

        # NCCP-NODES
        nx.draw_networkx_nodes(G,pos,nodelist=nccps,
                               node_size=600,alpha=0.7,node_color='g',node_shape='d')
        
        # PNODES
        nx.draw_networkx_nodes(G,pos,nodelist=npnodes,
                               node_size=900,alpha=0.7,node_color='w',node_shape='8')
        
        
        
        
        # edges
        nx.draw_networkx_edges(G,pos,edgelist=eright,
                            width=3,alpha=0.5,edge_color='r')
        nx.draw_networkx_edges(G,pos,edgelist=eleft,
                            width=3,alpha=0.5,edge_color='g')
        nx.draw_networkx_edges(G,pos,edgelist=enormal,
                            width=3,alpha=0.5,edge_color='b',style='dashed')
        
        
        # labels
        nx.draw_networkx_labels(G,pos,labels=ltests,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=llabels,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=lbothlabels,font_size=10)
        nx.draw_networkx_labels(G,pos,labels=ldynlabels,font_size=10)
        
        #plt.savefig("weighted_graph.png") # save as png
        #plt.show() # display
        
        #nx.
        
        #return plt        

    def draw(self):
        self._prepare_draw()
        
        plt.axis('off')
        plt.box("off")
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1,
                      wspace=0, hspace=0)
        plt.show()

    def dot_string(self):
        self._prepare_draw(resolveDynamic=True)
    
        #import StringIO    
        #stringBuffer = StringIO.StringIO()
        
        A = nx.to_agraph(self._G)
        
        #nx.write_dot(self._G, stringBuffer)
        
        #return stringBuffer.getvalue()
        return A.to_string()
        
    def clear(self):
        
        plt.clf()
        self._reinit()
                
    def __repr__(self, *args, **kwargs):
        return "<_NetworkXWrapper>"            
    