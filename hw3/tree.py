
# basic tree class
# author: Ryan Phillips 
# (made for cs480 @ OSU)

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.depth = 0

    def add_child(self, obj):
        self.children.append(obj)

        #need to set depth recursively
        def set_depth(t):
            if (t != None or t != str):
                if (len(t.children) > 0):
                    for i in t.children:
                        if (i != None): 
                            i.depth = t.depth + 1
                            set_depth(i)
        set_depth(self)



    # this one works recursively... cool...
    # so use it like this: tree.add_child2(parent, child)
    def add_child2(self, obj2, obj3):
        if self.data == obj2:
            tmp = Node(obj3)
            self.add_child(tmp)
        else:
            def inner(_x, _obj2, _obj3):
                for i in _x.children:
                    if i.data == _obj2:
                        tmp = Node(_obj3)
                        i.add_child(tmp)

                    if len(_x.children) > 0:
                        inner(i, _obj2, obj3)
            inner(self,obj2,obj3)

     
def pre_order_trav(t):
    out = []
    def inner(t):
        if (t != None):
            out.append(t.data)
            if (len(t.children) > 0):
                for i in t.children:
                    if (i != None): 
                        inner(i)
    inner(t)
    return out

def post_order_trav(t):
    out = []
    def inner(t):
        if (t != None):
            if (len(t.children) > 0):
                for i in t.children:
                    if (i != None): 
                        inner(i)
            out.append(t.data)
    inner(t)
    return out

# Okay, I know this isn't an accurate visual representation - but it's good enough for now.
def print_tree(t):
	if (t != None):
		if (int(t.depth) > 0):
			print spacer2(int(t.depth-1)) + spacer(int(1)) + str(t.data)
		else: print str(t.data)
		if (len(t.children) > 0):
			print spacer2(int(t.depth)) + "|"
			for i in t.children:
				if (i != None): 
					print_tree(i)

def print_tree2(t):
    if (t != None):
        print str(t.depth), str(t.data)
        if (len(t.children) > 0):
            for i in t.children:
                if (i != None): 
                    print_tree2(i)

# needed for print_tree
def spacer(x):
	l = ""
	if (x > 0):
		l = "@"
		for i in xrange(x):
			l += "--"
		return l
	return l

# needed for print_tree
def spacer2(x):
	l = ""
	if (x > 0):
		l = "|"
		for i in xrange(x):
			l += "  "
		return l
	return l

def test_tree():
    print "input: 1 * 2 + 5 / 3"
    '''

    let's put this in our tree for testing:

    1 * 2 + 5 / 3

         +
        / \
       *   /
      / \  / \
     1  2  5  3     


    '''
    tree = Node('+')
    l = Node('*')
    r = Node('/')
    tree.add_child(l)
    tree.add_child(r)

    ll = Node('1')
    lr = Node('2')
    l.add_child(ll)
    l.add_child(lr)

    rl = Node('5')
    rr = Node('3')
    r.add_child(rl)
    r.add_child(rr)

    print_tree(tree)
    print_tree2(tree)


def t2():
    tree = Node('a')
    tree.add_child2('a', 'b')
    tree.add_child2('b', 'c')
    tree.add_child2('a', 'e')
    tree.add_child2('c', 'ok')
    tree.add_child2('ok', 'golly')
    print_tree(tree)







