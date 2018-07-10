import csv
from os.path import join, dirname

def load_grounding_map(filename):
    gm_rows = load_csv(filename)
    gm_tuples = []
    g_map = {}
    for row in gm_rows:
        gm_tuples.append(tuple(row))
        key = row[0]
        db_refs = {'TEXT': key}
        keys = [entry for entry in row[1::2] if entry != '']
        values = [entry for entry in row[2::2] if entry != '']
        if len(keys) != len(values):
            print('ERROR: Mismatched keys and values in row %s' % str(row))
            continue
        else:
            db_refs.update(dict(zip(keys, values)))
            if len(db_refs.keys()) > 1:
                g_map[key] = db_refs
            else:
                g_map[key] = None
    return g_map, tuple(gm_tuples)


def load_equivalences(filename):
    equivalences = {}
    rows = load_csv(filename)
    for row in rows:
        fplx_id = row[2]
        equiv = (row[0], row[1])
        if fplx_id not in equivalences:
            equivalences[fplx_id] = [equiv]
        else:
            equivalences[fplx_id].append(equiv)
    return equivalences


def load_relationships(filename):
    relationships = []
    rows = load_csv(filename)
    for row in rows:
        relationships.append(((row[0], row[1]), row[2], (row[3], row[4])))
    return relationships


def load_entities(filename):
    entities = []
    rows = load_csv(filename)
    for row in rows:
        entities.append(row[0])
    return entities


def load_csv(filename):
    filename = join(dirname(__file__), filename)
    with open(filename) as fh:
        csvreader = csv.reader(fh, delimiter=',', quotechar='"')
        rows = [row for row in csvreader]
    return rows


def load_synonyms(gm):
    synonyms = {}
    for syn, db_refs in gm.items():
        for db, db_id in db_refs.items():
            if db == 'FPLX':
                if db_id in synonyms:
                    synonyms[db_id].append(syn)
                else:
                    synonyms[db_id] = [syn]
    return synonyms

relationships = load_relationships('relations.csv')
equivalences = load_equivalences('equivalences.csv')
gm, gm_tuples = load_grounding_map('grounding_map.csv')
entities = load_entities('entities.csv')

synonyms = load_synonyms(gm)

