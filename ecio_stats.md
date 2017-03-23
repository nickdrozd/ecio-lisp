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

----------
Total saves: 11
Max stack depth: 6
Total fetches: 100
Labels passed: 53
Syntax checks: 12
----------
Total file reads: 227
Run-time: 0.0689857006072998
----------

n = 1

----------
Total saves: 11
Max stack depth: 6
Total fetches: 100
Labels passed: 53
Syntax checks: 12
----------
Total file reads: 227
Run-time: 0.06718897819519043
----------

n = 2

----------
Total saves: 30
Max stack depth: 8
Total fetches: 328
Labels passed: 185
Syntax checks: 37
----------
Total file reads: 758
Run-time: 0.22564291954040527
----------

n = 3

----------
Total saves: 49
Max stack depth: 12
Total fetches: 556
Labels passed: 317
Syntax checks: 62
----------
Total file reads: 1289
Run-time: 0.3939206600189209
----------

n = 4

----------
Total saves: 87
Max stack depth: 16
Total fetches: 1012
Labels passed: 581
Syntax checks: 112
----------
Total file reads: 2351
Run-time: 0.7222328186035156
----------

n = 5

----------
Total saves: 144
Max stack depth: 20
Total fetches: 1696
Labels passed: 977
Syntax checks: 187
----------
Total file reads: 3944
Run-time: 1.2938480377197266
----------

n = 6

----------
Total saves: 239
Max stack depth: 24
Total fetches: 2836
Labels passed: 1637
Syntax checks: 312
----------
Total file reads: 6599
Run-time: 2.1581878662109375
----------

n = 7

----------
Total saves: 391
Max stack depth: 28
Total fetches: 4660
Labels passed: 2693
Syntax checks: 512
----------
Total file reads: 10847
Run-time: 3.365889310836792
----------

n = 8

----------
Total saves: 638
Max stack depth: 32
Total fetches: 7624
Labels passed: 4409
Syntax checks: 837
----------
Total file reads: 17750
Run-time: 5.612431526184082
----------

n = 9

----------
Total saves: 1037
Max stack depth: 36
Total fetches: 12412
Labels passed: 7181
Syntax checks: 1362
----------
Total file reads: 28901
Run-time: 9.38938307762146
----------

n = 10

----------
Total saves: 1683
Max stack depth: 40
Total fetches: 20164
Labels passed: 11669
Syntax checks: 2212
----------
Total file reads: 46955
Run-time: 15.8973548412323
----------


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

n = 0

----------
Total saves: 32
Max stack depth: 6
Total fetches: 203
Labels passed: 92
Syntax checks: 22
----------
Total file reads: 445
Run-time: 0.1605210304260254
----------

n = 1

----------
Total saves: 60
Max stack depth: 7
Total fetches: 411
Labels passed: 192
Syntax checks: 44
----------
Total file reads: 913
Run-time: 0.3141133785247803
----------

n = 2

----------
Total saves: 88
Max stack depth: 7
Total fetches: 619
Labels passed: 292
Syntax checks: 66
----------
Total file reads: 1381
Run-time: 0.49139904975891113
----------

n = 3

----------
Total saves: 116
Max stack depth: 7
Total fetches: 827
Labels passed: 392
Syntax checks: 88
----------
Total file reads: 1849
Run-time: 0.6387221813201904
----------

n = 4

----------
Total saves: 144
Max stack depth: 7
Total fetches: 1035
Labels passed: 492
Syntax checks: 110
----------
Total file reads: 2317
Run-time: 0.7856476306915283
----------

n = 5

----------
Total saves: 172
Max stack depth: 7
Total fetches: 1243
Labels passed: 592
Syntax checks: 132
----------
Total file reads: 2785
Run-time: 0.93282151222229
----------

n = 6

----------
Total saves: 200
Max stack depth: 7
Total fetches: 1451
Labels passed: 692
Syntax checks: 154
----------
Total file reads: 3253
Run-time: 1.0928044319152832
----------

n = 7

----------
Total saves: 228
Max stack depth: 7
Total fetches: 1659
Labels passed: 792
Syntax checks: 176
----------
Total file reads: 3721
Run-time: 1.2560434341430664
----------

n = 8

----------
Total saves: 256
Max stack depth: 7
Total fetches: 1867
Labels passed: 892
Syntax checks: 198
----------
Total file reads: 4189
Run-time: 1.4225411415100098
----------

n = 9

----------
Total saves: 284
Max stack depth: 7
Total fetches: 2075
Labels passed: 992
Syntax checks: 220
----------
Total file reads: 4657
Run-time: 1.562903642654419
----------

n = 10

----------
Total saves: 312
Max stack depth: 7
Total fetches: 2283
Labels passed: 1092
Syntax checks: 242
----------
Total file reads: 5125
Run-time: 1.7182204723358154
----------


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

----------
Total saves: 17
Max stack depth: 6
Total fetches: 164
Labels passed: 86
Syntax checks: 19
----------
Total file reads: 371
Run-time: 0.1252434253692627
----------

n = 1

----------
Total saves: 28
Max stack depth: 6
Total fetches: 314
Labels passed: 170
Syntax checks: 35
----------
Total file reads: 715
Run-time: 0.23515987396240234
----------

n = 2

----------
Total saves: 39
Max stack depth: 6
Total fetches: 464
Labels passed: 254
Syntax checks: 51
----------
Total file reads: 1059
Run-time: 0.339127779006958
----------

n = 3

----------
Total saves: 50
Max stack depth: 6
Total fetches: 614
Labels passed: 338
Syntax checks: 67
----------
Total file reads: 1403
Run-time: 0.42785000801086426
----------

n = 4

----------
Total saves: 61
Max stack depth: 6
Total fetches: 764
Labels passed: 422
Syntax checks: 83
----------
Total file reads: 1747
Run-time: 0.5416491031646729
----------

n = 5

----------
Total saves: 72
Max stack depth: 6
Total fetches: 914
Labels passed: 506
Syntax checks: 99
----------
Total file reads: 2091
Run-time: 0.6371340751647949
----------

n = 6

----------
Total saves: 83
Max stack depth: 6
Total fetches: 1064
Labels passed: 590
Syntax checks: 115
----------
Total file reads: 2435
Run-time: 0.7419490814208984
----------

n = 7

----------
Total saves: 94
Max stack depth: 6
Total fetches: 1214
Labels passed: 674
Syntax checks: 131
----------
Total file reads: 2779
Run-time: 0.8042550086975098
----------

n = 8

----------
Total saves: 105
Max stack depth: 6
Total fetches: 1364
Labels passed: 758
Syntax checks: 147
----------
Total file reads: 3123
Run-time: 0.8877136707305908
----------

n = 9

----------
Total saves: 116
Max stack depth: 6
Total fetches: 1514
Labels passed: 842
Syntax checks: 163
----------
Total file reads: 3467
Run-time: 1.0174803733825684
----------

n = 10

----------
Total saves: 127
Max stack depth: 6
Total fetches: 1664
Labels passed: 926
Syntax checks: 179
----------
Total file reads: 3811
Run-time: 1.0906903743743896
----------











03/22/17

The explicit control evaulator has been reimplemented using the analyze-execute model from SICP 4.1.7. It has the optimizations of the eval-apply evaluator, but it hasn't been optimized for the analyze-execute specific features (there are plenty of opportunities).

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

n = 0

----------
Total saves: 106
Max stack depth: 31
Total fetches: 672
Labels passed: 317
Syntax checks: 39
----------
Total file reads: 1441
Run-time: 0.6043035984039307
----------

n = 1

----------
Total saves: 141
Max stack depth: 31
Total fetches: 909
Labels passed: 419
Syntax checks: 39
----------
Total file reads: 1945
Run-time: 0.7813854217529297
----------

n = 2

----------
Total saves: 176
Max stack depth: 31
Total fetches: 1146
Labels passed: 521
Syntax checks: 39
----------
Total file reads: 2449
Run-time: 0.9927103519439697
----------

n = 3

----------
Total saves: 211
Max stack depth: 31
Total fetches: 1383
Labels passed: 623
Syntax checks: 39
----------
Total file reads: 2953
Run-time: 1.1739189624786377
----------

n = 4

----------
Total saves: 246
Max stack depth: 31
Total fetches: 1620
Labels passed: 725
Syntax checks: 39
----------
Total file reads: 3457
Run-time: 1.4375619888305664
----------

n = 5

----------
Total saves: 281
Max stack depth: 31
Total fetches: 1857
Labels passed: 827
Syntax checks: 39
----------
Total file reads: 3961
Run-time: 1.8285324573516846
----------

n = 6

----------
Total saves: 316
Max stack depth: 31
Total fetches: 2094
Labels passed: 929
Syntax checks: 39
----------
Total file reads: 4465
Run-time: 1.9753153324127197
----------

n = 7

----------
Total saves: 351
Max stack depth: 31
Total fetches: 2331
Labels passed: 1031
Syntax checks: 39
----------
Total file reads: 4969
Run-time: 2.2253479957580566
----------

n = 8

----------
Total saves: 386
Max stack depth: 31
Total fetches: 2568
Labels passed: 1133
Syntax checks: 39
----------
Total file reads: 5473
Run-time: 2.1752994060516357
----------

n = 9

----------
Total saves: 421
Max stack depth: 31
Total fetches: 2805
Labels passed: 1235
Syntax checks: 39
----------
Total file reads: 5977
Run-time: 2.5058350563049316
----------

n = 10

----------
Total saves: 456
Max stack depth: 31
Total fetches: 3042
Labels passed: 1337
Syntax checks: 39
----------
Total file reads: 6481
Run-time: 2.6740076541900635
----------


    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci {}))

n = 0

----------
Total saves: 49
Max stack depth: 24
Total fetches: 378
Labels passed: 210
Syntax checks: 26
----------
Total file reads: 862
Run-time: 0.2993807792663574
----------

n = 1

----------
Total saves: 49
Max stack depth: 24
Total fetches: 378
Labels passed: 210
Syntax checks: 26
----------
Total file reads: 862
Run-time: 0.30638551712036133
----------

n = 2

----------
Total saves: 75
Max stack depth: 24
Total fetches: 639
Labels passed: 345
Syntax checks: 26
----------
Total file reads: 1432
Run-time: 0.476668119430542
----------

n = 3

----------
Total saves: 101
Max stack depth: 24
Total fetches: 900
Labels passed: 480
Syntax checks: 26
----------
Total file reads: 2002
Run-time: 0.682269811630249
----------

n = 4

----------
Total saves: 153
Max stack depth: 24
Total fetches: 1422
Labels passed: 750
Syntax checks: 26
----------
Total file reads: 3142
Run-time: 1.0721426010131836
----------

n = 5

----------
Total saves: 231
Max stack depth: 25
Total fetches: 2205
Labels passed: 1155
Syntax checks: 26
----------
Total file reads: 4852
Run-time: 1.7221033573150635
----------

n = 6

----------
Total saves: 361
Max stack depth: 30
Total fetches: 3510
Labels passed: 1830
Syntax checks: 26
----------
Total file reads: 7702
Run-time: 2.796583652496338
----------

n = 7

----------
Total saves: 569
Max stack depth: 35
Total fetches: 5598
Labels passed: 2910
Syntax checks: 26
----------
Total file reads: 12262
Run-time: 4.753705978393555
----------

n = 8

----------
Total saves: 907
Max stack depth: 40
Total fetches: 8991
Labels passed: 4665
Syntax checks: 26
----------
Total file reads: 19672
Run-time: 7.762490510940552
----------

n = 9

----------
Total saves: 1453
Max stack depth: 45
Total fetches: 14472
Labels passed: 7500
Syntax checks: 26
----------
Total file reads: 31642
Run-time: 12.251363515853882
----------

n = 10

----------
Total saves: 2337
Max stack depth: 50
Total fetches: 23346
Labels passed: 12090
Syntax checks: 26
----------
Total file reads: 51022
Run-time: 20.593132257461548
----------


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

----------
Total saves: 61
Max stack depth: 28
Total fetches: 493
Labels passed: 265
Syntax checks: 30
----------
Total file reads: 1105
Run-time: 0.3806135654449463
----------

n = 1

----------
Total saves: 76
Max stack depth: 28
Total fetches: 661
Labels passed: 351
Syntax checks: 30
----------
Total file reads: 1471
Run-time: 0.5086367130279541
----------

n = 2

----------
Total saves: 91
Max stack depth: 28
Total fetches: 829
Labels passed: 437
Syntax checks: 30
----------
Total file reads: 1837
Run-time: 0.6384379863739014
----------

n = 3

----------
Total saves: 106
Max stack depth: 28
Total fetches: 997
Labels passed: 523
Syntax checks: 30
----------
Total file reads: 2203
Run-time: 0.7351176738739014
----------

n = 4

----------
Total saves: 121
Max stack depth: 28
Total fetches: 1165
Labels passed: 609
Syntax checks: 30
----------
Total file reads: 2569
Run-time: 0.8446676731109619
----------

n = 5

----------
Total saves: 136
Max stack depth: 28
Total fetches: 1333
Labels passed: 695
Syntax checks: 30
----------
Total file reads: 2935
Run-time: 0.9845635890960693
----------

n = 6

----------
Total saves: 151
Max stack depth: 28
Total fetches: 1501
Labels passed: 781
Syntax checks: 30
----------
Total file reads: 3301
Run-time: 1.1039810180664062
----------

n = 7

----------
Total saves: 166
Max stack depth: 28
Total fetches: 1669
Labels passed: 867
Syntax checks: 30
----------
Total file reads: 3667
Run-time: 1.2359495162963867
----------

n = 8

----------
Total saves: 181
Max stack depth: 28
Total fetches: 1837
Labels passed: 953
Syntax checks: 30
----------
Total file reads: 4033
Run-time: 1.4266352653503418
----------

n = 9

----------
Total saves: 196
Max stack depth: 28
Total fetches: 2005
Labels passed: 1039
Syntax checks: 30
----------
Total file reads: 4399
Run-time: 1.6152348518371582
----------

n = 10

----------
Total saves: 211
Max stack depth: 28
Total fetches: 2173
Labels passed: 1125
Syntax checks: 30
----------
Total file reads: 4765
Run-time: 1.7288978099822998
----------







03/22/17

For comparison between the eval-apply and analyze-execute evaluators, here are the same fibonacci functions, but with (fibonacci 10) being executed twice after being defined.


    (begin
      (def fibonacci
        (λ (n)
          (if (< n 2)
              n
              (_+ (fibonacci (_- n 1))
                  (fibonacci (_- n 2))))))
      (fibonacci 10)
      (fibonacci 10))

ANALYZE

----------
Total saves: 4639
Max stack depth: 53
Total fetches: 46436
Labels passed: 24032
Syntax checks: 29
----------
Total file reads: 101448
Run-time: 44.38411593437195
----------

EVAL

----------
Total saves: 3362
Max stack depth: 43
Total fetches: 40304
Labels passed: 23328
Syntax checks: 4421
----------
Total file reads: 93859
Run-time: 35.1933479309082
----------


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
      (fibonacci 10)
      (fibonacci 10))

ANALYZE

----------
Total saves: 846
Max stack depth: 31
Total fetches: 5657
Labels passed: 2461
Syntax checks: 42
----------
Total file reads: 12035
Run-time: 5.146688222885132
----------

EVAL

----------
Total saves: 620
Max stack depth: 10
Total fetches: 4542
Labels passed: 2174
Syntax checks: 481
----------
Total file reads: 10199
Run-time: 3.4945788383483887
----------

    (begin
      (def fibonacci
        (λ (n)
          (def loop
            (λ (a b count)
               (if (= count n)
                   a
                   (loop b (_+ a b) (_+ count 1)))))
          (loop 0 1 0)))
      (fibonacci 10)
      (fibonacci 10))

ANALYZE

----------
Total saves: 383
Max stack depth: 28
Total fetches: 4047
Labels passed: 2080
Syntax checks: 33
----------
Total file reads: 8844
Run-time: 3.3052279949188232
----------

EVAL

----------
Total saves: 250
Max stack depth: 9
Total fetches: 3304
Labels passed: 1842
Syntax checks: 355
----------
Total file reads: 7571
Run-time: 2.2749998569488525
----------









