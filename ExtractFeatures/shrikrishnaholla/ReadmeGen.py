#!/usr/bin/python
"""This is a simple markdown readme generator. It walks through the directory it is in,
imports every module/package in the directory and dumps the documentation of every source file
in a readme file in that directory"""
import os
import importlib
import types
if __name__ == '__main__':
    rootdir = os.getcwd()
    rootname = rootdir[rootdir.rfind('/')+1:]
    pkg = dict()
    for root, dirs, files in os.walk(rootdir):
        if root.find('.git') == -1:
            packagename = root.replace(rootdir, '')
            if packagename == '':
                packagename = root[root.rfind('/')+1:]
            packagename = packagename.strip('/')
            packagename = packagename.replace('/','.')
            modules = dict()

            for package in dirs:
                try:
                    pkg[package] = __import__(package)
                except ImportError, e:
                    #print 'could not import', package, e
                    pass
                except ValueError:
                    pass

            for module in files:
                try:
                    if packagename != rootname:
                        modules[module] = __import__(packagename+'.'+module[:module.find('.')],globals(), locals(), files, -1)
                    else:
                        modules[module] = __import__(module[:module.find('.')], globals(), locals(), files, -1)
                except ImportError,e :
                    #print 'could not import', module, e
                    pass
                except ValueError:
                    pass

            if len(modules) > 1 or len(pkg) >1:
                readme = open(root+'/README.md', 'wb')
                readme.write('\n')
                readme.write(packagename.title()+'\n')
                readme.write('='*len(packagename)+'\n')
                readme.write('\n')
                if '__init__.py' in modules and modules['__init__.py'].__doc__!= None:
                    lines = (modules['__init__.py'].__doc__).splitlines()
                    for line in lines:
                        readme.write(line+'  \n')

                for module in modules:
                    if module != '__init__.py' and module.find('.pyc') == -1:
                        readme.write('\n')
                        readme.write(module[:module.find('.')].title()+'\n')
                        readme.write('-'*len(module[:module.find('.')])+'\n')
                        if modules[module].__doc__ != None:
                            readme.write('\n')
                            lines = (modules[module].__doc__).splitlines()
                            for line in lines:
                                readme.write(line+'  \n')
                        for bloc in modules[module].__dict__:
                            if isinstance(modules[module].__dict__[bloc], types.ClassType) and modules[module].__dict__[bloc].__doc__ != None:
                                readme.write('\n')
                                readme.write('##'+bloc+'##'+'\n')
                                readme.write('\n')
                                lines = (modules[module].__dict__[bloc].__doc__).splitlines()
                                for line in lines:
                                    readme.write(line+'  \n')
                            elif isinstance(modules[module].__dict__[bloc], types.FunctionType) and modules[module].__dict__[bloc].__doc__ != None:
                                readme.write('\n')
                                readme.write('###'+bloc+'###'+'\n')
                                readme.write('\n')
                                lines = (modules[module].__dict__[bloc].__doc__).splitlines()
                                for line in lines:
                                    readme.write(line+'  \n')
                readme.close()
