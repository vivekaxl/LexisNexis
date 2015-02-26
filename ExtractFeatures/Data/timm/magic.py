"""
Magic Method Hack #1: Generating HTML (version 3)

Changed the constructor of ``Tag`` to accept keyword arguments. Also, we show
how to create more interesting "tag" objects.
"""
import os, copy, webbrowser

class Tag():
    def __init__(self, name, **kwargs):
        self.name = name
        self.attrs = kwargs
        self.children = []

    def __call__(self, **kwargs):
        #print kwargs
        tag = copy.deepcopy(self)
        tag.attrs.update(kwargs)
        return tag

    def __getitem__(self, args):
        tag = copy.deepcopy(self)
        if isinstance(args, tuple): 
            tag.children.extend(args)
        else:
            tag.children.append(args)
        return tag
    
    def __str__(self):
        result = '<' + self.name
        if self.attrs:
            result += ' '
            result += ' '.join('%s="%s"' % item for item in self.attrs.items())
        if self.children:
            result += '>'
            result += ''.join(str(c) for c in self.children)
            result += '</%s>\n' % self.name
        else:
            result += ' />\n'
        return result

def dijit(tag):
    return """<html><head>
<title>Dijit Generation Example</title>
    <style type="text/css">
        @import "http://o.aolcdn.com/dojo/1.0.0/dijit/themes/tundra/tundra.css";
        @import "http://o.aolcdn.com/dojo/1.0.0/dojo/resources/dojo.css"
    </style>
    <script type="text/javascript" src="http://o.aolcdn.com/dojo/1.0.0/dojo/dojo.xd.js"
        djConfig="parseOnLoad: true"></script>
    <script type="text/javascript">
        dojo.require("dijit.form.Button");
        dojo.require("dijit.form.CheckBox");
        dojo.require("dijit.form.TextBox");
        dojo.require("dijit.form.DateTextBox");
        dojo.require("dojo.parser");
    </script>
</head>
<body class="tundra">%s</body></html>""" % str(tag)

div         = Tag('div')
p           = Tag('p')
checkbox    = Tag('input', dojoType='dijit.form.CheckBox', type='checkbox')
textbox     = Tag('input', dojoType='dijit.form.TextBox', type='text')
button      = Tag('button', dojoType='dijit.form.Button')
datetextbox = Tag('input', dojoType='dijit.form.DateTextBox', type='text')

if __name__ == '__main__':
    page = div [
        p [
            'This is a Button ',
            button['Click me!'],
        ],
        p [
            'This is a TextBox ',
            textbox(value='The cow jumped over the moon, and it exploded'),
        ],
        p [
            'This is a CheckBox ',
            checkbox(checked='checked'),
        ],
        p [
            'This is a DateTextBox ',
            datetextbox(value='1998-03-23'),
        ],
    ]

    html = dijit(page)
    print html
    open('output.html', 'w').write(html)
    webbrowser.open('file://' + os.path.abspath('output.html'))

class X:
  def __call__(i,**kwargs):
    print 200
    print "!", kwargs
    return 11
  def __getitem__(i,args):
    print 10
#
#y = X()

#y [21,23]
