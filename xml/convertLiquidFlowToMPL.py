#!/usr/bin/env python

from lxml import etree as ET
import re
import os
import sys


def listOfProjectFiles(path='.'):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".prj"):
                result.append(os.path.join(root, file))
    return result


def writeResult(filename, tree):
    tree.write(open(filename, 'wb'), encoding=tree.docinfo.encoding, pretty_print=True, xml_declaration=True)
#    res = ""
#    with open(filename, 'r') as f:
#        data = f.read()
#        ### this regex query doubles the line indentation, for an indent of 4
#        ### [:-1] removes the last character bc lxml writes newline at the end
#        data2 = re.sub(r"( {2,})<", r"\1\1<", data)[:-1]
#        ### put empty elements on the same level
#        res = re.sub(r"( +)<([\w?!/]+)>\s+</\2>", r"\1<\2>\n\1</\2>", data2)
#    with open(filename, 'w') as f:
#        print("""<?xml version="1.0" encoding="ISO-8859-1"?>""", file=f)
#        print(res, file=f)


# Find Properties Element of phase with sought type
def findPropertiesOfPhase(medium, phase, porous_medium_id):
    if phase == "Medium":
        return medium.find("./properties")
    phase_tree = medium.find("./phases/phase/[type='" + phase + "']")
    if phase_tree is None:
        return None
    return phase_tree.find("./properties")

def getMedia(root):
    ###### Add Media Group if non existent
    if (root.find("./media") == None):
        print("constructing new media/medium id=\"0\"")
        media = ET.XML("<media><medium id=\"0\"><phases>" + \
                "<phase><type>Gas</type><properties></properties></phase>" + \
                "<phase><type>AqueousLiquid</type><properties></properties></phase>" + \
                "<phase><type>Solid</type><properties></properties></phase>" + \
                "</phases><properties></properties></medium></media>")

        root.insert(3, media)
    return root.find("./media")

def getMedium(root, porous_medium_id):
    media = getMedia(root)
    # check if the porous medium definition with 'porous_medium_id' already exist
    path="./medium[@id=\"" + str(porous_medium_id) + "\"]"
    medium=media.xpath(path)
    if (len(medium) == 0):
        print("constructing new medium tag with id " + str(porous_medium_id))
        medium = ET.XML("<medium id=\"" + str(porous_medium_id) + "\"><phases>" + \
                "<phase><type>Gas</type><properties></properties></phase>" + \
                "<phase><type>AqueousLiquid</type><properties></properties></phase>" + \
                "<phase><type>Solid</type><properties></properties></phase>" + \
                "</phases><properties></properties></medium>")
        media.insert(porous_medium_id+1, medium)
    return media.xpath("./medium[@id=\"" + str(porous_medium_id) + "\"]")[0]

def getPhaseProperties(root, phase, porous_medium_id):
    medium = getMedium(root, porous_medium_id)
    return findPropertiesOfPhase(medium, phase, porous_medium_id)

def parameterUsesLocalCoordinateSystem(parameter):
    use_coord_system = parameter.find("./use_local_coordinate_system")
    if use_coord_system is None:
        return False
    return use_coord_system.text == "true"

def readConstantValue(tree):
    if parameterUsesLocalCoordinateSystem(tree):
        return None # Keep parameters with local coord systems as they are.

    type = tree.find("./type").text
    if type == "Constant":
        if (value := tree.find("./value")) is not None:
            return value.text
        if (values := tree.find("./values")) is not None:
            return values.text
    return None

def readConstantPorosityParameter(tree):
    type = tree.find("./type").text
    if type == "Constant":
        if (porosity_parameter := tree.find("./porosity_parameter")) is not None:
            return porosity_parameter.text

    return None

def readConstantPermeabilityTensorEntries(tree):
    type = tree.find("./type").text
    if type == "Constant":
        if (parameter := tree.find("./permeability_tensor_entries")) is not None:
            return parameter.text

    return None

def readDupuitPermeabilityTensorParameter(tree):
    type = tree.find("./type").text
    if type == "Dupuit":
        if (parameter := tree.find("./permeability_tensor_entries")) is not None:
            return parameter.text

    return None

def mplAppendConstant(mpl_properties, name, value):
    mpl_properties.append(ET.XML("<property><name>" + name + "</name><type>" + \
                        "Constant</type><value>" + value + "</value>" + \
                        "</property>"))

def mplAppendParameter(mpl_properties, tag_name, parameter_name):
    mpl_properties.append(ET.XML("<property><name>" + tag_name + "</name><type>" + \
                        "Parameter</type><parameter_name>" + parameter_name + \
                        "</parameter_name></property>"))

def mplAppendDupuitParameter(mpl_properties, tag_name, parameter_name):
    mpl_properties.append(ET.XML("<property><name>" + tag_name + "</name><type>" + \
                        "Dupuit</type><parameter_name>" + parameter_name + \
                        "</parameter_name></property>"))

def getVanGenuchtenSaturationValues(material_property):
    SLR = material_property.find("./sr").text
    SGR = "{0:.15g}".format(1 - float(material_property.find("./smax").text))
    exponent = material_property.find("./m").text
    p0 = material_property.find("./pd").text
    print("vanGenuchtenSaturation: IGNORING pc_max.")
    return (SLR, SGR, exponent, p0)

def getVanGenuchtenRelativePermeabilityValues(material_property):
    SLR = material_property.find("./sr").text
    SGR = "{0:.15g}".format(1 - float(material_property.find("./smax").text))
    exponent = material_property.find("./m").text
    k_rel_min = material_property.find("./krel_min").text
    return (SLR, SGR, exponent, k_rel_min)

def mplAppendVanGenuchtenSaturation(mpl_properties, tag_name, SLR, SGR, exponent, p0):
    assert tag_name == "saturation"
    mpl_properties.append(ET.XML(
        "<property>" + \
            "<name>" + tag_name + "</name>" + \
            "<type>SaturationVanGenuchten</type>" + \
            "<residual_liquid_saturation>" + SLR + "</residual_liquid_saturation>" + \
            "<residual_gas_saturation>" + SGR + "</residual_gas_saturation>" + \
            "<exponent>" + exponent + "</exponent>" + \
            "<entry_pressure>" + p0 + "</entry_pressure>" + \
        "</property>" \
        ))

def mplAppendVanGenuchtenRelativePermeability(mpl_properties, tag_name, SLR, SGR, exponent, k_rel_min):
    assert tag_name == "relative_permeability"
    mpl_properties.append(ET.XML(
        "<property>" + \
            "<name>" + tag_name + "</name>" + \
            "<type>RelativePermeabilityVanGenuchten</type>" + \
            "<residual_liquid_saturation>" + SLR + "</residual_liquid_saturation>" + \
            "<residual_gas_saturation>" + SGR + "</residual_gas_saturation>" + \
            "<exponent>" + exponent + "</exponent>" + \
            "<minimum_relative_permeability_liquid>" + k_rel_min + "</minimum_relative_permeability_liquid>" + \
        "</property>" \
        ))

def removeXmlSubtree(tree):
    tree.getparent().remove(tree)

def replaceParameterWithMplProperty(root, paramName, phaseType, propName, porous_medium_id):
    props = getPhaseProperties(root, phaseType, porous_medium_id)
    assert props is not None

    #print("Process parameter", paramName)

    pName = root.find("./processes/process/" + paramName)
    if pName == None:
        print("Parameter", paramName, "not found")
        return

    param = root.find("./parameters/parameter/[name='" + pName.text.strip() + "']")
    assert param is not None, "Referenced parameter " + pName.text + " not found in parameters/."
    pType = param.find("./type").text

    ###### Exchange old params for new MPL-style input
    ###### if not a Constant parameter, old parameter stays and gets referenced

    if v := readConstantValue(param):
        mplAppendConstant(props, propName, v)
        removeXmlSubtree(param)
        removeXmlSubtree(pName)
        return

    props.append(ET.XML("<property><name>" + propName + "</name><type>" + \
                        "Parameter</type><parameter_name>" + pName.text + \
                        "</parameter_name></property>"))
    pName.getparent().remove(pName)


def isCurveType(tree):
    type = tree.find("./type")
    if type is None:
        return False
    return type.text == "Curve"

def isVanGenuchtenType(tree):
    type = tree.find("./type")
    return type is not None and \
            (type.text == "vanGenuchten" or type.text == "WettingPhaseVanGenuchten")

def addMPLMaterialProperty(root, property_type, property_name, phase,
                           mpl_property_name, porous_medium_id):
    props = getPhaseProperties(root, phase, porous_medium_id)
    assert props is not None

    #print("Material property", property_type + "/" + property_name)
    material_property = root.find("./processes/process/material_property/" +
                                  property_type + "/" + property_name)
    if material_property == None:
        print("Material property", property_type + "/" + property_name,
              "not found")
        return

    if v := readConstantValue(material_property):
        # add it to mpl, remove from material_property, and we are done.
        mplAppendConstant(props, property_name, v)
        removeXmlSubtree(material_property)
        return

    if p := readConstantPorosityParameter(material_property):
        # Find parameter
        param = root.find("./parameters/parameter/[name='" + p + "']")
        if v := readConstantValue(param):
            mplAppendConstant(props, property_name, v)
            removeXmlSubtree(material_property)
            #removeXmlSubtree(param)
        return

    if p := readConstantPermeabilityTensorEntries(material_property):
        # Find parameter
        param = root.find("./parameters/parameter/[name='" + p + "']")
        if parameterUsesLocalCoordinateSystem(param):
            # Keep parameters with local coord systems as they are.
            mplAppendParameter(props, property_name, p)
        if v := readDupuitConstantValue(param):
            mplAppendConstant(props, property_name, v)
        return

    if p := readDupuitPermeabilityTensorParameter(material_property):
        # Find parameter
        param = root.find("./parameters/parameter/[name='" + p + "']")
        # Keep parameters for Dupuit permeability as they are.
        mplAppendDupuitParameter(props, property_name, p)
        return

    if (property_name == "relative_permeability" \
     or property_name == "capillary_pressure") \
     and isCurveType(material_property):
        print("Replace curve parameter", property_name, "with constant", mpl_property_name)
        mplAppendConstant(props, mpl_property_name, "1")  # assume fully saturated
        removeXmlSubtree(material_property)
        return

    if property_name == "capillary_pressure" and isVanGenuchtenType(material_property):
        values = getVanGenuchtenSaturationValues(material_property)
        mplAppendVanGenuchtenSaturation(props, mpl_property_name, *values)
        removeXmlSubtree(material_property)
        return

    if property_name == "relative_permeability" and isVanGenuchtenType(material_property):
        values = getVanGenuchtenRelativePermeabilityValues(material_property)
        mplAppendVanGenuchtenRelativePermeability(props, mpl_property_name, *values)
        removeXmlSubtree(material_property)

def removeMaterialProperty(root, property_type, property_name, phase,
                           mpl_property_name, porous_medium_id):
    props = getPhaseProperties(root, phase, porous_medium_id)
    assert props is not None

    #print("Material property", property_type + "/" + property_name)
    material_property = root.find("./processes/process/material_property/" +
                                  property_type + "/" + property_name)
    if material_property == None:
        print("Material property", property_type + "/" + property_name,
              "not found")
        return

    if v := readConstantValue(material_property):
        # add it to mpl, remove from material_property, and we are done.
        removeXmlSubtree(material_property)
        return

    if p := readConstantPorosityParameter(material_property):
        # Find parameter
        param = root.find("./parameters/parameter/[name='" + p + "']")
        if v := readConstantValue(param):
            removeXmlSubtree(material_property)
            removeXmlSubtree(param)
        return

    if p := readConstantPermeabilityTensorEntries(material_property):
        # Find parameter
        param = root.find("./parameters/parameter/[name='" + p + "']")
        if parameterUsesLocalCoordinateSystem(param):
            # Keep parameters with local coord systems as they are.
            removeXmlSubtree(material_property)
        if v := readConstantValue(param):
            removeXmlSubtree(material_property)
            removeXmlSubtree(param)
        return

    if p := readDupuitPermeabilityTensorParameter(material_property):
        removeXmlSubtree(material_property)
        return

    if (property_name == "relative_permeability" \
     or property_name == "capillary_pressure") \
     and isCurveType(material_property):
        removeXmlSubtree(material_property)
        return

    if property_name == "capillary_pressure" and isVanGenuchtenType(material_property):
        removeXmlSubtree(material_property)
        return

    if property_name == "relative_permeability" and isVanGenuchtenType(material_property):
        values = getVanGenuchtenRelativePermeabilityValues(material_property)
        removeXmlSubtree(material_property)

def addFluidPropertyWithMplProperty(root, property_type, property_name,
                                        phase, mpl_property_name,
                                        porous_medium_id):
    props = getPhaseProperties(root, phase, porous_medium_id)
    assert props is not None

    #print("Material property", property_type + "/" + property_name)
    material_property = root.find("./processes/process/material_property/" +
                                  property_type + "/" + property_name)
    if material_property == None:
        print("Material property", property_type + "/" + property_name,
              "not found")
        return

    if v := readConstantValue(material_property):
        # add it to mpl.
        mplAppendConstant(props, property_name, v)
        return

def removeFluidProperty(root, property_type, property_name, phase,
                        mpl_property_name, porous_medium_id):
    props = getPhaseProperties(root, phase, porous_medium_id)
    assert props is not None

    #print("Material property", property_type + "/" + property_name)
    material_property = root.find("./processes/process/material_property/" +
                                  property_type + "/" + property_name)
    if material_property == None:
        return

    if v := readConstantValue(material_property):
        # remove property from the old xml structures
        removeXmlSubtree(material_property)
        return

def recursevelyEmpty(tree):
    #print("Recursively empty checking:", '<' + tree.tag + '>', "with text", tree.text)
    if tree is None:
        print("Recursively empty found got an non-existing tree.")
        print("RETURN False")
        return False    # non-exisiting tree is not empty, s.t. it will not be deleted
    if tree.text is not None:
        print("Recursively empty found this non-empty part:", '<' + tree.tag + '>', "with text", tree.text)
        print("RETURN False")
        return False
    all_recursively_empty = all(recursevelyEmpty(c) for c in tree.iterchildren())
    print("RETURN", all_recursively_empty)
    return all_recursively_empty

def cleanupEmptyMplPhases(tree, porous_medium_id):
    for phase_name in ["Solid", "Gas", "AqueousLiquid"]:
        properties = getPhaseProperties(tree, phase_name, porous_medium_id)
        if recursevelyEmpty(properties):
            # remove the phase if there are no properties
            print("Remove phase w/o properties:", phase_name)
            phase = properties.getparent()
            removeXmlSubtree(phase)

def removeRecursivelyEmptyTree(tree):
    if tree is None:
        return
    assert recursevelyEmpty(tree), "tree <"+ tree.tag+ "> is not empty!"
    removeXmlSubtree(tree)

def countPorousMediumTags(tree):
    return len(tree.xpath('//porous_medium/porous_medium'))

def processFile(filename):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filename, parser)

    # (parameter name, phase, property)
    process_parameter_table = {
        # Solid
        ("solid_bulk_modulus", "Solid", "bulk_modulus"),
        ("reference_solid_density", "Solid", "reference_density"),
        ("solid_density", "Solid", "density"),
        ("biot_coefficient", "Solid", "biot_coefficient"),
        ("linear_thermal_expansion_coefficient", "Solid",
         "thermal_expansivity"),
        # Medium
        ("thermal_conductivity", "Medium", "thermal_conductivity"),
        ("specific_heat_capacity", "Medium", "specific_heat_capacity"),
        ("specific_heat_capacity", "Medium", "specific_heat_capacity"),
        ("temperature", "Medium", "reference_temperature"),
        # Liquid
        ("fluid_bulk_modulus", "AqueousLiquid", "bulk_modulus"),
    }

    liquid_property_table = {
        ("fluid", "viscosity", "AqueousLiquid", "viscosity"),
        ("fluid", "density", "AqueousLiquid", "density")
    }

    material_property_table = {
        ("porous_medium/porous_medium", "storage", "Solid", "storage"),
        ("porous_medium/porous_medium", "permeability", "Medium", "permeability"),
        ("porous_medium/porous_medium", "porosity", "Medium", "porosity"),
        ("porous_medium/porous_medium", "capillary_pressure", "Medium", "saturation"),
        ("porous_medium/porous_medium", "relative_permeability", "Medium", "relative_permeability")
    }

    # count porous_medium tags
    number_porous_medium_tags = countPorousMediumTags(tree.getroot())
    print('number of porous_medium tags: ' + str(number_porous_medium_tags))

    for porous_medium_id in range(0, number_porous_medium_tags):
        for entry in process_parameter_table:
            replaceParameterWithMplProperty(tree.getroot(), *entry, porous_medium_id)

        for entry in material_property_table:
            addMPLMaterialProperty(tree.getroot(), *entry, porous_medium_id)

        for entry in liquid_property_table:
            addFluidPropertyWithMplProperty(tree.getroot(), *entry, porous_medium_id)

    for porous_medium_id in range(0, number_porous_medium_tags):
        for entry in liquid_property_table:
            removeFluidProperty(tree.getroot(), *entry, porous_medium_id)

        for entry in material_property_table:
            removeMaterialProperty(tree.getroot(), *entry, porous_medium_id)

        cleanupEmptyMplPhases(tree, porous_medium_id)
        try:
            print("trying to remove old material_property tree:")
            #print(ET.tostring(tree.find("./processes/process/material_property"),
            #    pretty_print=True))
            removeRecursivelyEmptyTree(tree.find("./processes/process/material_property"))
        except AssertionError:
            print("The old material property subtree could not be removed.")
            print("Project file will be invalid.")

    writeResult(filename + ".new", tree)


if os.path.isfile(sys.argv[1]):
    processFile(sys.argv[1])

if os.path.isdir(sys.argv[1]):
    filenamelist = listOfProjectFiles(sys.argv[1])
    for filename in filenamelist:
        processFile(filename)
