class FP_Node:

    def __init__(self, value, parent):
        """ Creates an FP node - a data structure for use as tree nodes in an FP tree """
        self.value = value
        self.count = 1
        self.children = {} # {value: node}
        self.twin = None
        self.parent = parent

    def add_child(self, node):
        """ 
        Add a new child node
        """
        self.children[node.value] = node

    def add_twin(self, twin_node):
        """ 
        Connect a twin node to this node 
        Twin node must have the same value
        """
        if twin_node.value == self.value:
            self.twin = twin_node
        else:
            raise ValueError("Attempted to connect sibling node with value {} \
            with node of value {}. Sibling nodes must have same value".format(twin_node.value, self.value))

    def up_count(self):
        """ Increase the count value of this node """
        self.count += 1

class FP_Tree:

    def __init__(self, support):
        """ Creates an FP tree for generating association rules for a set of transactions """
        self.support = support
        self.support_order_map = {}
        self.root = FP_Node(None, None)
        self.last_value_pointers = {} # {value: node} dict of pointers used for linking same value nodes

    def get_item_frequencies(self, table):
        """ 
        Scan data and find support for each item 
        Populates the support_order instance attribute with the list of most to least common values
        """
        frequencies = {}
        for entry in table:
            for item in entry:
                if item in frequencies:
                    frequencies[item] += 1
                else:
                    frequencies[item] = 1
        frequencies = {item:count for item, count in frequencies.items() if count >= 2}
        for position, item in enumerate(sorted(frequencies, key = frequencies.__getitem__, reverse = True)):
            self.support_order_map[item] = position   

    def add_node(self, value, parent):
        """ 
        Add a node to the FP tree as a child of the specified parent node 
        If a node with the same value already exists in the tree, creates a twin link from it to this node
        Returns the new node
        """
        return self._add_node(value, parent)

    def _add_node(self, value, parent):
        """ 
        Add a node to the FP tree as a child of the specified parent node 
        If a node with the same value already exists in the tree, creates a twin link from it to this node
        Returns the new node
        """
        # existing node with that value as child, just up count
        if value in parent.children.keys():
            new_node = parent.children[value]
            new_node.up_count()
        # create new child node, twinning as necessary
        else: 
            new_node = FP_Node(value, parent)
            parent.add_child(new_node)
            if value in self.last_value_pointers.keys():
                self.last_value_pointers[value].add_twin(new_node)
            self.last_value_pointers[value] = new_node
        return new_node

    def add_transaction(self, values):
        """ Add a list of values which make up a single transaction to the FP tree """
        values = [value for value in values if value in self.support_order_map] # filter out unsupported values
        if values:
            values = sorted(values, key = lambda item: self.support_order_map[item]) # order values by support order
            node = self.root
            for value in values:
                node = self.add_node(value, node)

    def print_tree(self):
        """ Print the entire FP tree with a new line for each level of the tree """
        results = []
        depth_limit = 1

        while True:
            results = self._print_tree(self.root, 0, depth_limit)
            depth_limit += 1
            if results:
                print(results)
            else:
                return

    def _print_tree(self, node, current_level, depth_limit):
        """ Get the values at a given depth limit for all descendants of a given node """
        results = []
        if not node:
            return
        elif current_level == depth_limit:
            return node.value
        elif node.children:
            for child in node.children.values():
                result = self._print_tree(child, current_level + 1, depth_limit)
                if result:
                    results.extend(result)
        else:
            return
        return results

    def find_node(self, value):
        """
        Find and return a node with specified value
        Returns the first node found (leftmost)
        """
        return self._find_node(self.root, value)

    def _find_node(self, node, value):
        """
        Find and return a node with specified value, which is the descendant of a specified node
        Returns the first node found (leftmost)
        """
        if node.value == value:
            return node
        elif node.children:
            for child in node.children.values():
                found = self._find_node(child, value)
                if found:
                    return found

    def get_prefix_tree(self, value):
        """ Get the prefix path sub-tree which ends in a given value """

        def prefixes_to_root(node):
            path = []
            while node is not self.root:
                path.append(node)
                node = node.parent
            return path

        return [prefixes_to_root(node) for node in self.get_twins(value)]

    def get_twins(self, value):
        """ 
        Get the chain of twins for nodes of a given value 
        Returns the chain of twin nodes as a list
        """
        node = self.find_node(value)
        if node:
            return [twin for twin in self._get_twins(node)]

    def _get_twins(self, node):
        """ Generator to retrieve the twin nodes for a given node """
        if not node:
            return
        else:
            yield node
            yield from self._get_twins(node.twin)
        
    def build_conditional_tree(self, value):
        """ Build the conditional FP tree for a given value """
        # Get the prefix sub tree
        # Update support counts for each node in the tree for it's "value" support count
        # Remove nodes with "value"
        # Remove infrequent items from prefix paths
        twins = self.get_twins(value)
        support = sum([node.count for node in twins]) # get support of item
        if support < self.support:
            pass # TODO complete
            
    def 

