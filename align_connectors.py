#      Python: 3.7.6
#   Kodierung: utf-8
""" """
class Aligner():
    """ """

    def __init__(self, path, connectors, mode='naive'):
        self.path = path
        self.connectors = connectors
        self.mode = mode


def main():
    obj1 = Aligner('test.txt', {'aber', 'doch', 'jedoch',
                                'allerdings', 'andererseits', 'hingegen'})


if __name__ == "__main__":
    main()
