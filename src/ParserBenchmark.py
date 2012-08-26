import sys
import time

if __name__ == '__main__':
    
    nFile = sys.argv[1]
    
    filer = open("../../icse-ie/tests/"+nFile, 'rU')
    
    s = filer.read()
    
    import myclips
    
    network = myclips.Network()
    parser = network.getParser()
    
    start_time = time.time()
    parser.parse(s, True)
    print time.time() - start_time, " seconds"
