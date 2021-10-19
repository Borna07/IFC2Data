import ifcopenshell as ifc
import plotly.express as px
import pandas as pd


def get_attr_of_pset(_id, ifc_file):
    """ Get all attributes of an instance by given Id
        param _id: id of instance
        return: dict of dicts of attributes
    """
    dict_psets = {}

    try:
        defined_by_type = [x.RelatingType for x in ifc_file[_id].IsDefinedBy if x.is_a("IfcRelDefinesByType")]
        defined_by_properties = [x.RelatingPropertyDefinition for x in ifc_file[_id].IsDefinedBy if
                                 x.is_a("IfcRelDefinesByProperties")]
    except:
        dict_psets.update({ifc_file[_id].GlobalId: "No Attributes found"})
    else:
        for x in defined_by_type:
            if x.HasPropertySets:
                for y in x.HasPropertySets:
                    for z in y.HasProperties:
                        dict_psets.update({z.Name: z.NominalValue.wrappedValue})

        for x in defined_by_properties:
            if x.is_a("IfcPropertySet"):
                for y in x.HasProperties:
                    if y.is_a("IfcPropertySingleValue"):
                        dict_psets.update({y.Name: y.NominalValue.wrappedValue})
                    # this could be usefull for multilayered walls in Allplan
                    if y.is_a("IfcComplexProperty"):
                        for z in y.HasProperties:
                            dict_psets.update({z.Name: z.NominalValue.wrappedValue})
            if x.is_a("IfcElementQuantity"):
                for y in x.Quantities:
                    dict_psets.update({y[0]: y[3]})

    finally:
        dict_psets.update({"IfcGlobalId": ifc_file[_id].GlobalId})

        return dict_psets


def get_structural_storey(_id, ifc_file):
    """ Get structural (IfcBuilgingStorey) information of an instance by given Id
        param _id: id of instance
        return: dict of attributes
    """
    dict_structural = {}
    instance = ifc_file[_id]
    try:
        structure = instance.ContainedInStructure
        storey = structure[0].RelatingStructure.Name

    except:
        dict_structural.update({"Storey": "No Information found"})

    else:
        dict_structural.update({"Storey": storey})
    finally:
        return dict_structural

def movecol(df, cols_to_move=[], ref_col='', place='After'):
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]

    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]

    return (df[seg1 + seg2 + seg3])


def parser(contents):
    ifc_file = ifc.open(contents)
    rooms = ifc_file.by_type("IfcSpace")
    instances = ifc_file.by_type("IfcBuildingElement")
    project = ifc_file.by_type("IfcProject")[0].Name
    for room in rooms:
            instances.append(room)
    excel_list = []

    for inst in instances:
        info_pset = get_attr_of_pset(inst.id(), ifc_file=ifc_file)
        info = inst.get_info()
        for x in inst.IsDefinedBy:
            if x.is_a("IfcRelDefinesByType") == True:
                info_pset.update({"Type_Name": x.get_info()["RelatingType"].Name})
            else:
                pass
        info_pset.update({"Name": inst.Name})
        info_pset.update({"IfcType": info["type"]})
        info_pset.update({"Project": project})

        if inst.is_a("IfcSpace") == True:
            info_structural = inst.Decomposes[0].RelatingObject.Name
            info_pset.update({"Storey": info_structural})
        else:
            info_structural = get_structural_storey(inst.id(), ifc_file=ifc_file)
            info_pset.update(info_structural)


        excel_list.append(info_pset)

    df1 = pd.DataFrame(excel_list)

    df2 = movecol(df1,
                    cols_to_move=['IfcType', 'Storey'],
                    ref_col=df1.columns[0],
                    place='Before')
    
    return df2

def all_divide(df2, path):
    worterbuch = {}
    for item in df2.IfcType.unique():
        DF = df2[df2['IfcType'].str.contains(item, na=False)]
        DF = DF.dropna(axis='columns', how='all')
        worterbuch[item] = DF

    with pd.ExcelWriter(path) as writer:
        for i in worterbuch.keys():
            worterbuch[i].to_excel(writer, sheet_name=i)

def unique(df, path):
    names = []
    data = []
    for column in df.columns:
        name = column
        value = list(df[name].unique())
        names.append(name)
        data.append(value)

    df2 = pd.DataFrame(data, names)
    df2 = df2.transpose()

    df2.to_excel(path)

def unique_divide(df, path):
    worterbuch = {}
    dfs = dict(tuple(df.groupby('IfcType')))
    for key in dfs.keys():
        df = dfs[key]
        names = []
        data = []
        for column in df.columns:
            name = column
            value = list(df[name].unique())
            names.append(name)
            data.append(value)

        df2 = pd.DataFrame(data, names)
        worterbuch[key] = df2.transpose()

    with pd.ExcelWriter(path) as writer:
        for i in worterbuch.keys():
            worterbuch[i].to_excel(writer, sheet_name=i)

