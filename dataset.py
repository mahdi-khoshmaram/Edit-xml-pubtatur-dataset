from bs4 import BeautifulSoup



def children(bs):
    children = bs.find_all(recursive = False)
    child_list = []
    for child in children:
        child_list.append(child.name)
    return child_list


name = "CDR_TrainingSet.BioC.xml"


# read .xml file
with open(name) as fh:
    soup = BeautifulSoup(fh, "xml")


documents = soup.find_all('document')

for doc in documents:
    anno_dic = {}
    # set id
    id = doc.id.string
    
    # parse passages
    passages = doc.find_all('passage')

    # write .PubTator.txt  file
    with open('train.PubTator.txt', "a") as fh:
        for psg in passages:
            # type = title or abstract
            type = psg.infon.string
            
            # title
            if type == 'title':
                text = psg.find('text', recursive = False).string
                # fh.write(f"{id}|t|{text}")
            
            # abstract
            if type == 'abstract':
                text = psg.find('text', recursive = False).string
                # fh.write(f"{text}\n\n")

            # entities
            annotations = psg.find_all("annotation", recursive = False)
            for anno in annotations:
                mesh = anno.find(attrs={"key": "MESH"}).string
                en_type = anno.find(attrs={"key": "type"}).string
                en_name = anno.find("text", recursive = False).string
                
                if mesh in anno_dic.keys():
                    continue
                print(children(anno))
                anno_dic[mesh] = {'type':en_type, 'name':en_name}
    # if id == '2234245':
    #     print(anno_dic)

