'''
Created on 20/11/2015
'''

from __future__ import absolute_import
from __future__ import print_function
from discoverer.discoverer import TBTAFDiscoverer

if __name__ == '__main__':
    print("--------------------------------")
    print("Results from LoadTests")
    print("--------------------------------")
    testCollection = TBTAFDiscoverer.LoadTests(r'./\\\\\samples/\//')
    file_no = 1
    for i in testCollection:
        md = i.getTestMetadata()
        print("File numbet " +  str(file_no) +  ":")
        print("\tAssetID: " + str(md.getAssetID()))
        print("\tTags (" + str(len(md.getTags())) +"): " +  str(md.getTags()))
        print("\tPriority: " + str(md.getPriority()))
        print("\tDescription: " + md.getAssetDescription())
        print("\tTest results below")
        i.setup()
        i.execute()
        i.cleanup()
        file_no += 1
        print("***********")
        print("")
    print("")
    print("--------------------------------")
    print("Tags from LoadCodeMetadata")
    print("--------------------------------")
    codeMetaDataCollection = TBTAFDiscoverer.LoadCodeMetadata(r'.\samples')
    file_no = 1
    for md in codeMetaDataCollection:
        print("File numbet " +  str(file_no) +  ":")
        print("\tAssetID: " + str(md.getAssetID()))
        print("\tTags (" + str(len(md.getTags())) +"): " +  str(md.getTags()))
        print("\tPriority: " + str(md.getPriority()))
        print("\tDescription: " + md.getAssetDescription())  
        file_no += 1
        print("***********")
        print("")