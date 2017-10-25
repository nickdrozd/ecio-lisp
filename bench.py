from repl import ecio_eval
from stats import display_stats


def run_benchmark():
    recursive_fib = '''
    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))
'''

    iterative_fib = '''
    (begin
      (def fibonacci
        (λ (n)
          (def loop
            (λ (a b count)
               (if (= count n)
                   a
                   (loop b (_+ a b) (_+ count 1)))))
          (loop 0 1 0)))
      (fibonacci {}))
'''

    mutative_fib = '''
    (begin
      (def fibonacci
        (λ (n)
          (def a 0)
          (def b 1)
          (def count 0)
          (def loop
            (λ ()
              (if (= count n)
                  a
                  (begin
                    (def temp b)
                    (set! b (_+ a b))
                    (set! a temp)
                    (set! count (_+ count 1))
                    (loop)))))
          (loop)))
      (fibonacci {}))
'''

    fib_vals = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 5,
        6: 8,
        7: 13,
        8: 21,
        9: 34,
        10: 55,
    }

    functions = {
        'RECURSIVE': recursive_fib,
        'ITERATIVE': iterative_fib,
        'MUTATIVE': mutative_fib,
    }

    for function_name, function in functions.items():
        print(function_name)

        for i in range(11):
            print('n = {}'.format(i))
            print()

            expected = fib_vals[i]
            result = ecio_eval(function.format(i))

            if result != expected:
                print('Incorrect result')
                return

            display_stats(1)
            print()


if __name__ == '__main__':
    run_benchmark()
