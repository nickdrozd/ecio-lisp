import unittest

from repl import ecio_eval

from garbage import collect_garbage
from mem import load_memory, write_memory, clear_memory, ROOT


class EcioTestCase(unittest.TestCase):
    def setUp(self):
        pass
        # initialize()


class TestRun(EcioTestCase):
    '''Evaluates an expression using all basic language features

    The expression includes a tree-recursive fibonacci function,
    so it runs pretty slow. Be patient!
    '''
    def test_run(self):
        expr = '''
            (def x 2)
            (def y 3)
            (def z 4)
            (set! z (_+ z (_+ x y)))
            (def fibonacci
              (λ (n)
                (if (< n 2)
                    n
                    (_+ (fibonacci (_- n 1))
                        (fibonacci (_- n 2))))))
            (def fibz (fibonacci z))
            (set! x
              (_* ((λ (x)
                    (_* x x)) 3)
                  fibz))
            (def addabc
              (λ (a)
                (λ (b)
                  (λ (c)
                    (λ (x)
                      (_+ x (_+ a (_+ b c))))))))
            (def d8 (λ () 8))
            (def result ((((addabc x) fibz) z) (d8)))
            result
        '''
        # z = 9
        # fibz = 34
        # x = 306
        # result = 357

        # test some repl functions too!
        self.load_and_run(expr)

        self.assert_result(357)

    def test_loop(self):
        expr = '''
            (def count 0)
            (def loop
              (λ ()
                (if (= count 10)
                    (_* count count)
                    (begin
                      (set! count (_+ count 1))
                      (loop)))))
            (loop)
        '''

        self.load_and_run(expr)

        self.assert_result(100)

    def test_redefinition(self):
        expr = '''
            (def result 0)
            (def x 1)
            (set! result (_+ result x))
            (def x 2)
            (set! result (_+ result x))
            (set! x 3)
            (set! result (_+ result x))
            (def f
              (λ ()
                (def x 4)
                (set! result (_+ result x))
                (set! x 5)
                (set! result (_+ result x))))
            (f)
            (def g
              (λ ()
                (def x 6)
                (def h
                  (λ ()
                    (set! x (_+ x 1))
                    (set! result (_+ result x))))
                (set! result (_+ result x))
                (h)))
            (g)
        '''
    

        self.load_and_run(expr)

        self.assert_result(28)

    # 

    def assert_result(self, expected):
        self.assertEqual(
            self.result,
            expected,
            'Wrong result')

    def load_and_run(self, statements):
        begin_seq = '(begin {})'.format(statements)
        self.result = ecio_eval(begin_seq)




class TestGarbageCollector(EcioTestCase):
    def test_gc(self):
        memory = {
            "__MEM_0": [
                {
                    "add12": [
                        "__MEM_12",
                        [
                            "x"
                        ],
                        [
                            [
                                "_+",
                                "x",
                                [
                                    "_+",
                                    "a",
                                    [
                                        "_+",
                                        "b",
                                        "c"
                                    ]
                                ]
                            ]
                        ]
                    ],
                    "add9": [
                        "__MEM_5",
                        [
                            "x"
                        ],
                        [
                            [
                                "_+",
                                "x",
                                [
                                    "_+",
                                    "a",
                                    [
                                        "_+",
                                        "b",
                                        "c"
                                    ]
                                ]
                            ]
                        ]
                    ],
                    "addabc": [
                        "__MEM_0",
                        [
                            "a"
                        ],
                        [
                            [
                                "\u03bb",
                                [
                                    "b"
                                ],
                                [
                                    "\u03bb",
                                    [
                                        "c"
                                    ],
                                    [
                                        "\u03bb",
                                        [
                                            "x"
                                        ],
                                        [
                                            "_+",
                                            "x",
                                            [
                                                "_+",
                                                "a",
                                                [
                                                    "_+",
                                                    "b",
                                                    "c"
                                                ]
                                            ]
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ],
                    "f": [
                        "__MEM_0",
                        [],
                        [
                            [
                                "\u03bb",
                                [],
                                8
                            ]
                        ]
                    ],
                    "variable": "value",
                },
                None
            ],
            "__MEM_1": [
                {},
                "__MEM_0"
            ],
            "__MEM_10": [
                {
                    "a": 3
                },
                "__MEM_0"
            ],
            "__MEM_11": [
                {
                    "b": 4
                },
                "__MEM_10"
            ],
            "__MEM_12": [
                {
                    "c": 5
                },
                "__MEM_11"
            ],
            "__MEM_13": [
                {},
                "__MEM_0"
            ],
            "__MEM_14": [
                {},
                "__MEM_13"
            ],
            "__MEM_2": [
                {},
                "__MEM_1"
            ],
            "__MEM_3": [
                {
                    "a": 2
                },
                "__MEM_0"
            ],
            "__MEM_4": [
                {
                    "b": 3
                },
                "__MEM_3"
            ],
            "__MEM_5": [
                {
                    "c": 4
                },
                "__MEM_4"
            ],
            "__MEM_6": [
                {
                    "x": 8
                },
                "__MEM_5"
            ],
            "__MEM_7": [
                {},
                "__MEM_0"
            ],
            "__MEM_8": [
                {},
                "__MEM_7"
            ],
            "__MEM_9": [
                {
                    "x": 8
                },
                "__MEM_5"
            ]
        }

        write_memory(memory)

        collect_garbage()

        self.load_memory()

        self.assert_null_root_enclosure()
        self.assert_address_count(7)
        self.assert_root_definition_count(5)


    def assert_address_count(self, expected):
        actual_address_count = len(self.memory.keys())

        self.assertEqual(
            actual_address_count,
            expected,
            'Address count -- expected: {}, actual: {}'.format(
                expected, actual_address_count))

    def assert_root_definition_count(self, expected):
        root_frame, _ = self.memory[ROOT]
        actual_definition_count = len(root_frame.keys())

        self.assertEqual(
            actual_definition_count,
            expected,
            'Root definition count -- expected: {}, actual: {}'.format(
                expected, actual_definition_count))

    def assert_null_root_enclosure(self):
        _, enclosure = self.memory[ROOT]

        self.assertIsNone(
            enclosure,
            'Root enclosure -- expected: {}, actual: {}'.format(
                None, enclosure))

    def load_memory(self):
        self.memory = load_memory()
