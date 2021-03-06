import logging
import re
from g2m_util import load_file, get_root_level_gradle_file, namespace, get_module_element
from lxml import etree

logger = logging.getLogger()
scm_dev_cnx_root = 'scm:git:git@github.com:upside-services'

# CHANGE THIS TEMPLATE'S PARENTS FOR YOUR SPECIFIC PURPOSES
template = """<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.upside</groupId>
        <artifactId>upside-service-pom</artifactId>
        <version>1.2.1</version>
    </parent>

    <groupId>com.upside.xxx</groupId>
    <packaging>pom</packaging>
    <artifactId>xxx</artifactId>
    <version>xxx</version>

    <name>xxx</name>
    <description>xxx</description>

    <scm>
        <developerConnection>xxx</developerConnection>
        <tag>HEAD</tag>
    </scm>

    <properties>
    </properties>

    <modules>
    </modules>
    
    <build>
    </build>
    
    <dependencyManagement>
        <dependencies>
        </dependencies>
    </dependencyManagement>

</project>
"""


def create_root_level_pom(group_id, artifact, artifact_version, gradle_files):
    """
    :param group_id the group_id of the artifact
    :param artifact the name of the artifact, which will also be used
    as the 'name' and 'description' tags in the returned pom
    :param artifact_version the version of the artfiact
    :param gradle_files: An array of tuples (see find_gradle_files) with
    information about which submodules our root-level pom should specify
    :return: An lxml Element containing content appropriate for a project's
    root-level pom.xml file
    """
    root_gradle = get_root_level_gradle_file(gradle_files)

    utf8_parser = etree.XMLParser(encoding='utf-8')
    pom = etree.fromstring(template, parser=utf8_parser)
    pom.find(f"{namespace}groupId").text = group_id
    pom.find(f"{namespace}artifactId").text = artifact
    pom.find(f"{namespace}version").text = artifact_version
    pom.find(f"{namespace}name").text = artifact
    pom.find(f"{namespace}description").text = artifact
    pom.find(f"{namespace}scm/{namespace}developerConnection").text = f"{scm_dev_cnx_root}/{artifact}.git"

    modules = pom.find(f"{namespace}modules")
    list.sort(gradle_files)
    for gradle_file in gradle_files:
        if not root_gradle == gradle_file:
            new_module = get_module_element(gradle_file)
            logging.debug(f"Adding new_module {new_module.text}")
            modules.append(new_module)

    return pom


def find_group_id(path_file_tuple):
    """
    Extracts any artifact 'group' information it can from a build.gradle file.
    Usually this is just contained in the root-level file under 'allprojects{ }'
    :param path_file_tuple: The build.gradle file to search
    :return: The group attribute referenced in the path_file_tuple, or None
    """
    content = load_file(path_file_tuple)
    pattern = re.compile("group\\s?=\\s?'(.*)'")
    for line in content:
        match = re.search(pattern, line)
        if match:
            return match.group(1)
    return None



