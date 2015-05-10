import os
from subprocess import Popen, PIPE

total = 0
ok = 0
for root, dirs, files in os.walk('tests'):
    for dir in dirs:
        for subroot, subdirs, subfiles in os.walk(os.path.join('tests', dir)):
            for file in subfiles:
                total += 1
                f = os.path.join('tests', dir, file)
                print '======================='
                print 'file: ' + f
                p = Popen(['python', f], stdin=PIPE, stdout=PIPE)
                python_output = p.communicate()[0]
                print 'output from python:'
                print python_output

                p = Popen(['python', 'pyClass.py', f, 'false'], stdin=PIPE, stdout=PIPE)
                my_output = p.communicate()[0]
                print 'output from my interpreter:'
                print my_output

                assert python_output == my_output
                if python_output == my_output:
                    ok += 1
                    print file + ' OK!'
                print '======================='

if ok == total:
    print '****************'
    print '* %(ok)2d/%(total)2d PASSED *' % {'ok' : ok, 'total' : total}
    print '*  ALL PASSED  *'
    print '****************'
else:
    print '****************'
    print '%(ok)d/%(total)d PASSED' % {'ok' : ok, 'total' : total}
    print '****************'
