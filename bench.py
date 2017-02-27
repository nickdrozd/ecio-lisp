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

    names = {
        recursive_fib: 'RECURSIVE',
        iterative_fib: 'ITERATIVE'
    }

    exprs = recursive_fib, iterative_fib

    for expr in exprs:
        print(expr)

        for i in range(11):
            print('n = {}'.format(i))
            print()

            expected = fib_vals[i]
            result = ecio_eval(expr.format(i))

            if result != expected:
                print('Incorrect result')
                return

            display_stats(1)
            print()

if __name__ == '__main__':
    run_benchmark()
