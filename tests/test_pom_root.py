import unittest
import xml.etree.ElementTree as ET
from pom_root import find_group_id, create_root_level_pom
from tests import gradle_files


class TestPomRoot(unittest.TestCase):

    def test_find_group_id(self):
        root_build_gradle = ('./tests/my-fake-project', 'build.gradle')
        self.assertEqual('com.upside.merchant', find_group_id(root_build_gradle))

    def test_create_root_level_pom(self):
        pom = create_root_level_pom('myartifact', '1.0.0', gradle_files)
        actual = ET.tostring(pom)
        expected = ET.fromstring(EXPECTED_POM)
        self.assertEqual(ET.tostring(expected), actual)


EXPECTED_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.upside</groupId>
        <artifactId>upside-service-pom</artifactId>
        <version>1.1.0</version>
    </parent>

    <groupId>com.upside.merchant</groupId>
    <packaging>pom</packaging>
    <artifactId>myartifact</artifactId>
    <version>1.0.0</version>

    <name>myartifact</name>
    <description>myartifact</description>

    <scm>
        <developerConnection>scm:git:git@github.com:upside-services/myartifact.git</developerConnection>
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
