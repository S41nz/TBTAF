'''
Created on 20/11/2015
'''

from discoverer.discoverer import TBTAFDiscoverer

if __name__ == '__main__':
    print "--------------------------------"
    print "Results from LoadTests"
    print "--------------------------------"
    testCollection = TBTAFDiscoverer.LoadTests(r'./\\\\\samples/\//')
    for i in testCollection:
        print i.getTestMetadata().getAssetDescription()
        i.setup()
        i.execute()
        i.cleanup()
    print "--------------------------------"
    print "Tags from LoadCodeMetadata"
    print "--------------------------------"
    codeMetaDataCollection = TBTAFDiscoverer.LoadCodeMetadata(r'.\samples')
    for md in codeMetaDataCollection:
        print "Size: " + str(len(md.getTags())) + ". Tags: " + str(md.getTags()) 