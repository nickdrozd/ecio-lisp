import unittest

from repl import ecio_eval
from parse import parse

from garbage import collect_garbage
from mem import load_memory, write_memory, ROOT


class EcioTestCase(unittest.TestCase):
    def setUp(self):
        pass
        # initialize()


class TestRun(EcioTestCase):
    def test_temp_analyze(self):
        self.result = ecio_eval('''
            (if 3
                (if 0
                    4
                    7)
                8)
        ''')

        self.assert_result(7)

    @unittest.expectedFailure
    def test_run(self):
        self.eval_seq('''
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
          (def d8 (delay 8))
          (def result ((((addabc x) fibz) z) (d8)))
          result
        ''')
        # z = 9
        # fibz = 34
        # x = 306
        # result = 357

        self.assert_result(357)
    @unittest.expectedFailure
    def test_loop(self):
        self.eval_seq('''
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
        ''')

        self.assert_result(2200)
    @unittest.expectedFailure
    def test_redefinition(self):
        self.eval_seq('''
          (def result 0)
          (def x 1)
          (inc-n! result x)
          (def x 2)
          (inc-n! result x)
          (set! x 3)
          (inc-n! result x)
          (def f
            (delay
              (def x 4)
              (inc-n! result x)
              (set! x 5)
              (inc-n! result x)))
          (f)
          (def g
            (λ ()
              (def x 6)
              (def h
                (λ ()
                  (inc-n! x 1)
                  (inc-n! result x)))
              (inc-n! result x)
              (h)))
          (g)
        ''')

        self.assert_result(28)
    @unittest.expectedFailure
    def test_quasiquote(self):
        self.eval_seq('''
          (def a (qsq (0 1 2)))
          (def b (qsq (0 (unq (_+ 1 2)) 4)))
          (def c (qsq (0 (spl (list 1 2)) 4)))
          (qsq (a (spl a)
                b (unq b)
                c (unq c)))
        ''')

        self.assert_result(
            '(a 0 1 2 b (0 3 4) c (0 1 2 4))')

    #

    def assert_result(self, expected):
        self.assertEqual(
            self.result,
            parse(str(expected)),
            'Wrong result')

    def eval_seq(self, expr):
        begin_seq = '''
          (begin
            (defmac inc-n! (var n)
              (qsq (set! (unq var)
                         (_+ (unq var)
                             (unq n)))))
            (defmac delay exprs (qsq (λ () (spl exprs))))
            {})
        '''.format(expr)

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
