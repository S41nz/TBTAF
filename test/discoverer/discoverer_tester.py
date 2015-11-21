'''
Created on 20/11/2015
'''

from discoverer.discoverer import TBTAFDiscoverer

if __name__ == '__main__':
    testCollection = TBTAFDiscoverer.LoadTests(r'./\\\\\samples/\//')
    for i in testCollection:
        print i.getTestMetadata().getAssetDescription()
        i.setup()
        i.execute()
        i.cleanup()
    codeMetaDataCollection = TBTAFDiscoverer.LoadCodeMetadata(r'.\samples')
    for md in codeMetaDataCollection:
        print md.getTags()