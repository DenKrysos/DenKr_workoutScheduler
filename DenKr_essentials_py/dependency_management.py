#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-15

@author: Dennis Krummacker
'''

import os
import subprocess
import pkg_resources




def check_dependencies(fPath,fName):
    """
    Check whether all dependencies listed in requirements.txt are installed.
    """
    requirements_file=os.path.join(fPath,fName)
    # result=subprocess.run(["python", "-m", "pip", "freeze", "-r", requirements_file], stderr=subprocess.STDOUT)
    # print(f'{result.returncode} | {result.stdout}')
    # try:
    #     # Call pip to check if requirements are installed
    #     subprocess.check_output(["python", "-m", "pip", "freeze", "-r", requirements_file], stderr=subprocess.STDOUT)
    #     print("All dependencies are installed.")
    # except subprocess.CalledProcessError as e:
    #     print("Some dependencies are missing.")
    #     print(e.output)  # Print the error output from pip
    not_installed=[]
    with open(requirements_file, 'r') as f:
        for line in f:
            # Ignore comments and empty lines
            line=line.strip()
            if line.startswith('#') or not line:
                continue
            try:
                pkg_resources.require(line)
            except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                not_installed.append(line)
    return not_installed



def install_dependencies(fPath,fName):
    requirements_file=os.path.join(fPath,fName)
    subprocess.run(['python', '-m', 'pip', 'install', '-r', requirements_file])


def assure_dependencies(fPath,fName):
    not_installed=check_dependencies(fPath,fName)
    if 0<len(not_installed):
        #User Prompt
        inputtry=0
        while 1:
            print("==============================")
            print("»Dependencies are missing. Shall I install them?« (y/n)")
            inp=input()
            if inp=="y" or inp=="yes" or inp=="ja" or inp=="j" or inp=="1":
                print(f"-> Calling 'python -m pip install -r' on {fName}.")
                install_dependencies(fPath,fName)
                #inputtry=3
                return 0
            elif inp=="n" or inp=="no" or inp=="nein" or inp=="n" or inp=="0":
                print("-> NO Installation")
                print("--> Exiting...")
                #inputtry=3
                exit(1)
            else:
                print("-> »Invalid Input.",end='')
                inputtry+=1
                if inputtry>=3:
                    print("«\n»Yeah, I propose we just cancel this...«\n")
                    print("--> Exiting...")
                    exit(1)
                else:
                    print(" Try again.«\n")







# Different approach
import unittest
class TestRequirements(unittest.TestCase):
    """Test availability of required packages."""
    def test_requirements(self,fPath,fName):
        """Test that each required package is available."""
        requirements_file=os.path.join(fPath,fName)
        requirements=pkg_resources.parse_requirements(requirements_file.open())
        for requirement in requirements:
            requirement=str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)