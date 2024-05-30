from bs4 import BeautifulSoup

name = "CDR_TrainingSet.BioC.xml"

def children(bs):
    children = bs.find_all(recursive = False)
    child_list = []
    for child in children:
        child_list.append(child.name)
    return child_list


# read .xml file
with open(name) as fh:
    soup = BeautifulSoup(fh, "xml")


documents = soup.find_all('document')


for doc in documents:
    # for storing id, title, abstract, relations
    jdoc = {}

    # for storing mesh:{type, name}
    anno_dic = {}

    # for storing relations of one document
    jrel = []

    # set id
    id = doc.id.string
    jdoc['id'] = id
    
    # parse passages
    passages = doc.find_all('passage')
    # parse relations
    relations = doc.find_all('relation')

    # passage
    for psg in passages:
        # type = title or abstract
        type = psg.infon.string
        
        # title
        if type == 'title':
            text = psg.find('text', recursive = False).string
            jdoc['title'] = text
        
        # abstract
        if type == 'abstract':
            text = psg.find('text', recursive = False).string
            jdoc['abstract'] = text

        # entities
        annotations = psg.find_all("annotation", recursive = False)
        for anno in annotations:
            Multi = False
            if anno.find(attrs = {"key":"CompositeRole"}, recursive = False):
                if anno.find(attrs = {"key":"CompositeRole"}, recursive = False).string == 'CompositeMention':
                    continue
            
            mesh = anno.find(attrs={"key": "MESH"}, recursive = False).string
            en_type = anno.find(attrs={"key": "type"}, recursive = False).string
            en_name = anno.find("text", recursive = False).string

            if "|" in mesh:
                meshs = mesh.split('|')
                Multi = True
            
            if Multi:
                for mesh in meshs:
                    if mesh in anno_dic.keys():
                        continue
                    anno_dic[mesh] = {'type':en_type, 'name':en_name}
                continue

            if mesh in anno_dic.keys():
                continue

            anno_dic[mesh] = {'type':en_type, 'name':en_name}

    # relation
    for rel in relations:
        rel_type = rel.find(attrs={"key": "relation"}, recursive = False).string
        chemical_id = rel.find(attrs={"key": "Chemical"}, recursive = False).string
        disease_id = rel.find(attrs={"key": "Disease"}, recursive = False).string

        chemical = anno_dic[chemical_id]
        disease = anno_dic[disease_id]

        jrel.append({"rel_type":rel_type, "chemical":chemical, "disease":disease})

    # write .PubTator.txt  file
    with open('train.PubTator.txt', "a") as fh:
        id = jdoc['id']
        title_split = jdoc['title'].split("\n")
        abstract_split = jdoc['abstract'].split("\n")

        abstract_edited = []
        title_edited = []

        for part in abstract_split:
            abstract_edited.append(part.strip())
        for part in title_split:
            title_edited.append(part.strip())

        separator = '' 
        abstract = separator.join(abstract_edited)
        title = separator.join(title_edited)

        fh.write(f"\n\n{id}|t|{title}{abstract}")
        for rel in jrel:
            
            type = rel['rel_type']
            chem_dic = rel['chemical']
            disease_dic = rel["disease"]

            if chem_dic['type'] != "Chemical":
                print("ERROR!")
                break
            if disease_dic['type'] != "Disease":
                print("ERROR!")
                break 
            chem = chem_dic['name']
            disease = disease_dic['name']
            fh.write(f"\n{id}\t{type}\t{chem}\t{disease}")

    

    
    
    
    
    
    
    
    # if id == '2234245':
    #     print(anno_dic)

