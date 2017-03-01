TODO:
  * Formatting (ugh)
    * csv?

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
























02/28/17

As per SICP exercise 5.32, added a check to function evaluation to skip saving the env in the case that the function is a variable (requiring only lookup).

    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))

n = 0

Total saves: 18
Max stack depth: 8
Labels passed: 46
Total file reads: 219
Run-time: 0.0731816291809082

n = 1

Total saves: 18
Max stack depth: 8
Labels passed: 46
Total file reads: 219
Run-time: 0.07265448570251465

n = 2

Total saves: 60
Max stack depth: 13
Labels passed: 149
Total file reads: 709
Run-time: 0.24394941329956055

n = 3

Total saves: 102
Max stack depth: 18
Labels passed: 252
Total file reads: 1199
Run-time: 0.4178471565246582

n = 4

Total saves: 186
Max stack depth: 23
Labels passed: 458
Total file reads: 2179
Run-time: 0.7314357757568359

n = 5

Total saves: 312
Max stack depth: 28
Labels passed: 767
Total file reads: 3649
Run-time: 1.3084232807159424

n = 6

Total saves: 522
Max stack depth: 33
Labels passed: 1282
Total file reads: 6099
Run-time: 2.1473546028137207

n = 7

Total saves: 858
Max stack depth: 38
Labels passed: 2106
Total file reads: 10019
Run-time: 3.507129669189453

n = 8

Total saves: 1404
Max stack depth: 43
Labels passed: 3445
Total file reads: 16389
Run-time: 5.892965078353882

n = 9

Total saves: 2286
Max stack depth: 48
Labels passed: 5608
Total file reads: 26679
Run-time: 9.971230268478394

n = 10

Total saves: 3714
Max stack depth: 53
Labels passed: 9110
Total file reads: 43339
Run-time: 16.86273431777954


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

Total saves: 32
Max stack depth: 8
Labels passed: 74
Total file reads: 368
Run-time: 0.11788105964660645

n = 1

Total saves: 62
Max stack depth: 10
Labels passed: 140
Total file reads: 698
Run-time: 0.22602033615112305

n = 2

Total saves: 92
Max stack depth: 10
Labels passed: 206
Total file reads: 1028
Run-time: 0.33154940605163574

n = 3

Total saves: 122
Max stack depth: 10
Labels passed: 272
Total file reads: 1358
Run-time: 0.44367241859436035

n = 4

Total saves: 152
Max stack depth: 10
Labels passed: 338
Total file reads: 1688
Run-time: 0.5592334270477295

n = 5

Total saves: 182
Max stack depth: 10
Labels passed: 404
Total file reads: 2018
Run-time: 0.6895220279693604

n = 6

Total saves: 212
Max stack depth: 10
Labels passed: 470
Total file reads: 2348
Run-time: 0.773449182510376

n = 7

Total saves: 242
Max stack depth: 10
Labels passed: 536
Total file reads: 2678
Run-time: 0.8748209476470947

n = 8

Total saves: 272
Max stack depth: 10
Labels passed: 602
Total file reads: 3008
Run-time: 1.0248358249664307

n = 9

Total saves: 302
Max stack depth: 10
Labels passed: 668
Total file reads: 3338
Run-time: 1.1520755290985107

n = 10

Total saves: 332
Max stack depth: 10
Labels passed: 734
Total file reads: 3668
Run-time: 1.293924331665039

