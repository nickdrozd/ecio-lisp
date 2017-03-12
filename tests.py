import unittest

from repl import ecio_eval
# from parse import parse

from garbage import collect_garbage
from mem import load_memory, write_memory, ROOT


class EcioTestCase(unittest.TestCase):
    def setUp(self):
        pass
        # initialize()


class TestRun(EcioTestCase):
    def test_run(self):
        self.expr = '''
          (def x 2)
          (def y 3)
          (def z 4)
          (inc-n! z (_+ x y))
          (def fibonacci
            (λ (n)
              (if (< n 2)
                  n
                  (_+ (fibonacci (- n 1))
                      (fibonacci (- n 2))))))
          (def fibz (fibonacci z))
          (set! x
            (* 1 (square 3) fibz 1))
          (def addabc
            (λ (a)
              (λ (b)
                (λ (c)
                  (λ (x)
                    (+ x a b c))))))
          (def d8 (λ () 8))
          (def result ((((addabc x) fibz) z) (d8)))
          result
        '''
        # z = 9
        # fibz = 34
        # x = 306
        # result = 357

        self.assert_result(357)

    def test_loop(self):
        self.expr = '''
          (def total 0)
          (def count 0)
          (def loop
            (λ ()
              (if (= count 10)
                  (_* total count)
                  (begin
                    (inc-n! count 2)
                    (inc-n! total (square count))
                    (loop)))))
          (loop)
        '''

        self.assert_result(2200)

    def test_redefinition(self):
        # macros don't work in function calls?
        self.expr = '''
          (def result 0)
          (def x 1)
          (inc-n! result x)
          (def x 2)
          (inc-n! result x)
          (set! x 3)
          (inc-n! result x)
          (def f
            (λ ()
              (def x 4)
              (set! result (+ result x))
              (set! x 5)
              (set! result (+ result x))))
          (f)
          (def g
            (λ ()
              (def x 6)
              (def h
                (λ ()
                  (set! x (+ x 1))
                  (set! result (+ result x))))
              (set! result (+ result x))
              (h)))
          (g)
        '''

        self.assert_result(28)

    #

    def assert_result(self, expected):
        self.eval_expr()

        self.assertEqual(
            self.result,
            expected,
            'Wrong result')

    def eval_expr(self):
        begin_seq = '''
          (begin
            (defmac inc-n! (var n)
              (qsq (set! (unq var)
                         (_+ (unq var)
                             (unq n)))))
            {})
        '''.format(self.expr)

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
