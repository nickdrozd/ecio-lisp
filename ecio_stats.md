TODO: Formatting (ugh)

02/28/17

The main body of the evaluator is laid out more or less the same as the code in SICP.

    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))

n = 0

Total saves: 22
Max stack depth: 8
Labels passed: 50
Total file reads: 243
Run-time: 0.08472347259521484

n = 1

Total saves: 22
Max stack depth: 8
Labels passed: 50
Total file reads: 243
Run-time: 0.08649945259094238

n = 2

Total saves: 78
Max stack depth: 13
Labels passed: 167
Total file reads: 817
Run-time: 0.29813671112060547

n = 3

Total saves: 134
Max stack depth: 18
Labels passed: 284
Total file reads: 1391
Run-time: 0.478851318359375

n = 4

Total saves: 246
Max stack depth: 23
Labels passed: 518
Total file reads: 2539
Run-time: 0.8967223167419434

n = 5

Total saves: 414
Max stack depth: 28
Labels passed: 869
Total file reads: 4261
Run-time: 1.523017168045044

n = 6

Total saves: 694
Max stack depth: 33
Labels passed: 1454
Total file reads: 7131
Run-time: 2.611776828765869

n = 7

Total saves: 1142
Max stack depth: 38
Labels passed: 2390
Total file reads: 11723
Run-time: 4.365293502807617

n = 8

Total saves: 1870
Max stack depth: 43
Labels passed: 3911
Total file reads: 19185
Run-time: 7.296448230743408

n = 9

Total saves: 3046
Max stack depth: 48
Labels passed: 6368
Total file reads: 31239
Run-time: 12.298634052276611

n = 10

Total saves: 4950
Max stack depth: 53
Labels passed: 10346
Total file reads: 50755
Run-time: 20.28084707260132


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

n = 0

Total saves: 38
Max stack depth: 8
Labels passed: 80
Total file reads: 404
Run-time: 0.1305379867553711

n = 1

Total saves: 76
Max stack depth: 10
Labels passed: 154
Total file reads: 782
Run-time: 0.25650596618652344

n = 2

Total saves: 114
Max stack depth: 10
Labels passed: 228
Total file reads: 1160
Run-time: 0.38715648651123047

n = 3

Total saves: 152
Max stack depth: 10
Labels passed: 302
Total file reads: 1538
Run-time: 0.5311250686645508

n = 4

Total saves: 190
Max stack depth: 10
Labels passed: 376
Total file reads: 1916
Run-time: 0.6329634189605713

n = 5

Total saves: 228
Max stack depth: 10
Labels passed: 450
Total file reads: 2294
Run-time: 0.7622084617614746

n = 6

Total saves: 266
Max stack depth: 10
Labels passed: 524
Total file reads: 2672
Run-time: 0.880944013595581

n = 7

Total saves: 304
Max stack depth: 10
Labels passed: 598
Total file reads: 3050
Run-time: 1.0140507221221924

n = 8

Total saves: 342
Max stack depth: 10
Labels passed: 672
Total file reads: 3428
Run-time: 1.1422312259674072

n = 9

Total saves: 380
Max stack depth: 10
Labels passed: 746
Total file reads: 3806
Run-time: 1.258692741394043

n = 10

Total saves: 418
Max stack depth: 10
Labels passed: 820
Total file reads: 4184
Run-time: 1.3859965801239014

