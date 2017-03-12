# pylint: skip-file

MACRO = '__MACRO'

LIBRARY = {
            MACRO : [],
            "*": [
                "__MEM_0",
                "nums",
                [
                    [
                        "fold-left",
                        "_*",
                        1,
                        "nums"
                    ]
                ]
            ],
            "+": [
                "__MEM_0",
                "nums",
                [
                    [
                        "fold-left",
                        "_+",
                        0,
                        "nums"
                    ]
                ]
            ],
            "-": "_-",
            "/": "_/",
            "add1": [
                "__MEM_0",
                [
                    "n"
                ],
                [
                    [
                        "_+",
                        "n",
                        1
                    ]
                ]
            ],
            "fold-left": [
                "__MEM_0",
                [
                    "comb",
                    "null",
                    "seq"
                ],
                [
                    [
                        "def",
                        "loop",
                        [
                            "\u03bb",
                            [
                                "result",
                                "rest"
                            ],
                            [
                                "if",
                                [
                                    "null?",
                                    "rest"
                                ],
                                "result",
                                [
                                    "loop",
                                    [
                                        "comb",
                                        "result",
                                        [
                                            "car",
                                            "rest"
                                        ]
                                    ],
                                    [
                                        "cdr",
                                        "rest"
                                    ]
                                ]
                            ]
                        ]
                    ],
                    [
                        "loop",
                        "null",
                        "seq"
                    ]
                ]
            ],
            "list": [
                "__MEM_0",
                "s",
                [
                    "s"
                ]
            ],
            "null?": [
                "__MEM_0",
                [
                    "s"
                ],
                [
                    [
                        "=",
                        "s",
                        [
                            "quote",
                            []
                        ]
                    ]
                ]
            ],
            "square": [
                "__MEM_0",
                [
                    "n"
                ],
                [
                    [
                        "_*",
                        "n",
                        "n"
                    ]
                ]
            ],
            "sub1": [
                "__MEM_0",
                [
                    "n"
                ],
                [
                    [
                        "_-",
                        "n",
                        1
                    ]
                ]
            ],
            "zero?": [
                "__MEM_0",
                [
                    "n"
                ],
                [
                    [
                        "=",
                        "n",
                        0
                    ]
                ]
            ]
        }
