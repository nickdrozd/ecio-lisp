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









02/28/17

Add a check for simple arguments. This appears to be a much more profitable optimization than the simple func check, but that may be because these stats only cover a function with simple functions.


    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))

n = 0

Total saves: 13
Max stack depth: 6
Labels passed: 49
Total file reads: 216
Run-time: 0.06912827491760254

n = 1

Total saves: 13
Max stack depth: 6
Labels passed: 49
Total file reads: 216
Run-time: 0.06911444664001465

n = 2

Total saves: 39
Max stack depth: 10
Labels passed: 167
Total file reads: 712
Run-time: 0.2130730152130127

n = 3

Total saves: 65
Max stack depth: 15
Labels passed: 285
Total file reads: 1208
Run-time: 0.35520005226135254

n = 4

Total saves: 117
Max stack depth: 20
Labels passed: 521
Total file reads: 2200
Run-time: 0.6575515270233154

n = 5

Total saves: 195
Max stack depth: 25
Labels passed: 875
Total file reads: 3688
Run-time: 1.104053020477295

n = 6

Total saves: 325
Max stack depth: 30
Labels passed: 1465
Total file reads: 6168
Run-time: 1.8697834014892578

n = 7

Total saves: 533
Max stack depth: 35
Labels passed: 2409
Total file reads: 10136
Run-time: 3.1492176055908203

n = 8

Total saves: 871
Max stack depth: 40
Labels passed: 3943
Total file reads: 16584
Run-time: 5.249367713928223

n = 9

Total saves: 1417
Max stack depth: 45
Labels passed: 6421
Total file reads: 27000
Run-time: 8.8052237033844

n = 10

Total saves: 2301
Max stack depth: 50
Labels passed: 10433
Total file reads: 43864
Run-time: 15.587692499160767


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

Total saves: 20
Max stack depth: 6
Labels passed: 80
Total file reads: 356
Run-time: 0.1110382080078125

n = 1

Total saves: 35
Max stack depth: 7
Labels passed: 156
Total file reads: 679
Run-time: 0.20235037803649902

n = 2

Total saves: 50
Max stack depth: 7
Labels passed: 232
Total file reads: 1002
Run-time: 0.2878115177154541

n = 3

Total saves: 65
Max stack depth: 7
Labels passed: 308
Total file reads: 1325
Run-time: 0.4055898189544678

n = 4

Total saves: 80
Max stack depth: 7
Labels passed: 384
Total file reads: 1648
Run-time: 0.505164384841919

n = 5

Total saves: 95
Max stack depth: 7
Labels passed: 460
Total file reads: 1971
Run-time: 0.6050670146942139

n = 6

Total saves: 110
Max stack depth: 7
Labels passed: 536
Total file reads: 2294
Run-time: 0.7012438774108887

n = 7

Total saves: 125
Max stack depth: 7
Labels passed: 612
Total file reads: 2617
Run-time: 0.7806341648101807

n = 8

Total saves: 140
Max stack depth: 7
Labels passed: 688
Total file reads: 2940
Run-time: 0.9037270545959473

n = 9

Total saves: 155
Max stack depth: 7
Labels passed: 764
Total file reads: 3263
Run-time: 0.994060754776001

n = 10

Total saves: 170
Max stack depth: 7
Labels passed: 840
Total file reads: 3586
Run-time: 1.0769333839416504












03/18/17

Two changes:

  1) Waiting to assign the initial until after the first arg (func) has been evaluated. This eliminates an unnecessary save of the empty arglist, as per SICP footnote 5.23.

  2) Evaluating the functions along with the arguments, rather than separately, and including it in ARGL. This eliminates the FUNC saves (and also raises the question: is FUNC needed? [Answer: it probably isn't needed for the interpreter, but it's handy for the compiler.]).

Which change was more impactful?

Note that the run times are actually higher than before. The price of the increase in stack efficiency is a greater number of labels passed, and in this system jumping to a label is not fast.

    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))

n = 0

Total saves: 11
Max stack depth: 6
Labels passed: 53
Total file reads: 227
Run-time: 0.06679940223693848

n = 1

Total saves: 11
Max stack depth: 6
Labels passed: 53
Total file reads: 227
Run-time: 0.0676124095916748

n = 2

Total saves: 30
Max stack depth: 8
Labels passed: 185
Total file reads: 758
Run-time: 0.22137761116027832

n = 3

Total saves: 49
Max stack depth: 12
Labels passed: 317
Total file reads: 1289
Run-time: 0.3810606002807617

n = 4

Total saves: 87
Max stack depth: 16
Labels passed: 581
Total file reads: 2351
Run-time: 0.7017796039581299

n = 5

Total saves: 144
Max stack depth: 20
Labels passed: 977
Total file reads: 3944
Run-time: 1.1670665740966797

n = 6

Total saves: 239
Max stack depth: 24
Labels passed: 1637
Total file reads: 6599
Run-time: 1.98274564743042

n = 7

Total saves: 391
Max stack depth: 28
Labels passed: 2693
Total file reads: 10847
Run-time: 3.307210683822632

n = 8

Total saves: 638
Max stack depth: 32
Labels passed: 4409
Total file reads: 17750
Run-time: 5.5228917598724365

n = 9

Total saves: 1037
Max stack depth: 36
Labels passed: 7181
Total file reads: 28901
Run-time: 9.243800640106201

n = 10

Total saves: 1683
Max stack depth: 40
Labels passed: 11669
Total file reads: 46955
Run-time: 15.641118049621582


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

Total saves: 17
Max stack depth: 6
Labels passed: 86
Total file reads: 371
Run-time: 0.11427164077758789

n = 1

Total saves: 28
Max stack depth: 6
Labels passed: 170
Total file reads: 715
Run-time: 0.2171478271484375

n = 2

Total saves: 39
Max stack depth: 6
Labels passed: 254
Total file reads: 1059
Run-time: 0.31978797912597656

n = 3

Total saves: 50
Max stack depth: 6
Labels passed: 338
Total file reads: 1403
Run-time: 0.40293073654174805

n = 4

Total saves: 61
Max stack depth: 6
Labels passed: 422
Total file reads: 1747
Run-time: 0.49988508224487305

n = 5

Total saves: 72
Max stack depth: 6
Labels passed: 506
Total file reads: 2091
Run-time: 0.6033778190612793

n = 6

Total saves: 83
Max stack depth: 6
Labels passed: 590
Total file reads: 2435
Run-time: 0.6923844814300537

n = 7

Total saves: 94
Max stack depth: 6
Labels passed: 674
Total file reads: 2779
Run-time: 0.7959372997283936

n = 8

Total saves: 105
Max stack depth: 6
Labels passed: 758
Total file reads: 3123
Run-time: 0.89408278465271

n = 9

Total saves: 116
Max stack depth: 6
Labels passed: 842
Total file reads: 3467
Run-time: 0.9927518367767334

n = 10

Total saves: 127
Max stack depth: 6
Labels passed: 926
Total file reads: 3811
Run-time: 1.0948302745819092

