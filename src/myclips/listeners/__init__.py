
try:
    from myclips.listeners._NetworkPlotterAdapter_NetworkX import _NetworkPlotterAdapter_NetworkX
    from myclips.listeners._NetworkPlotterAdapter_NetworkX import _NetworkXWrapper
    NetworkPlotter = _NetworkPlotterAdapter_NetworkX.useWrapper(_NetworkXWrapper)
except:
    
    # replace the NetworkPlotter class with a fake one if
    # networkX is not available
    
    from myclips.listeners.EventsManagerListener import EventsManagerListener
    import myclips
    class NetworkPlotter(EventsManagerListener):
        def __init__(self):
            myclips.logger.warning("NetworkX library (or dependencies) can't be found. Network Plotter not available")            
            EventsManagerListener.__init__(self)
        
    
