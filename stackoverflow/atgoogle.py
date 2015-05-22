from lxml import etree
tree = etree.parse("dumps/android/Users.xml")
print("""
    <style>
    body{
        font-family: arial;
        margin:40px auto; max-width:650px;
        line-height:1.6; font-size:18px;
        color:#222; padding:0 10px
    }
    h1,h2,h3{line-height:1.2}
    </style>
""")

g = 0

for i, row in enumerate(tree.iter()):
    about = row.get('AboutMe')
    if about:
        if " at google" in about.lower():
            print('<strong>-----</strong>')
            print(about)
            g += 1

print(g,"/",len(list(tree.iter())))