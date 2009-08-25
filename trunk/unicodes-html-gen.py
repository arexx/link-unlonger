from unicoder import ranges

def unicodes(name, first, last):
    print """
        <div class="group">
            <h2 class="name">%(name)s: %(count)d characters</h2>
            <div class="chars">%(chars)s</div>
        </div>""" % {
        "name": name,
        "count": last - first + 1,
        "chars": "".join([
            """
                <div class="char">
                    %(num)d
                    <div class="graph">&#%(num)d;</div>
                </div>""" % {"num": num}
            for num in xrange(first, last+1)
        ])
    }
    
    
def main():
    print """
        <html>
        <head>
            <title>Unicodes</title>
        </head>
        <style>
            body {
                font-family: sans-serif;
            }
        
            .group {
                clear: both;
                padding-top: 30px;
            }
        
            .char {
                width: 80px;
                height: 70px;
                padding: 10px;
                text-align: center;
                float: left;
                border: 1px solid #888;
                margin-left: -1px;
                margin-top: -1px;
            }
            
            .graph {
                font-size: 50px;
            }
        </style>
        <body>
    """

    totalchars = 0

    for (name, first, last) in ranges:
        totalchars += (last - first) + 1
        unicodes(name, first, last)

    print """
        <div class="group">
            <h2>Total characters: %(totalchars)d</h2>
        </div>
        </body>
        </html>
    """ % locals()


if __name__ == '__main__':
    main()
