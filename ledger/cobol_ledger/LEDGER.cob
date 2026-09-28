      *> LEDGER -- the precision arm.
      *>
      *> Reads a postfix op stream produced by bridge.py, evaluates it on a
      *> packed-decimal stack, writes one result per claim.
      *>
      *> It does no parsing. py_ledger is authoritative for REACHABILITY and
      *> hands this program an op stream that is already flat; this program
      *> is authoritative for PRECISION and does nothing but arithmetic.
      *>
      *> NEVER COMPILED. GnuCOBOL is absent from the environment this source
      *> was written in: cobc and cobcrun both resolve to nothing. Nothing in
      *> this file has been run. See MANIFEST.json.
      *>
      *> REQUIRES a COBOL implementation permitting more than 18 digits in a
      *> numeric item: the working item is S9(18)V9(18), 36 digits. GnuCOBOL
      *> allows 38. An implementation capping at 18 will reject this source
      *> at compile time, which is the correct outcome -- it cannot carry the
      *> precision this arm exists to carry.
      *>
      *> ROUNDED MODE IS NEAREST-EVEN, chosen to match py_ledger's
      *> ROUND_HALF_EVEN. Leaving the two different would manufacture
      *> cross-ledger disagreements about rounding mode and hide
      *> disagreements about arithmetic.
      *>
      *> CC0.

       IDENTIFICATION DIVISION.
       PROGRAM-ID. LEDGER.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT OPS-FILE ASSIGN TO "OPS.DAT"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS OPS-STATUS.
           SELECT RES-FILE ASSIGN TO "RESULTS.DAT"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS RES-STATUS.

       DATA DIVISION.
       FILE SECTION.
       FD  OPS-FILE.
       01  OP-REC.
           05  OP-REF        PIC X(40).
           05  OP-SEQ        PIC 9(4).
           05  OP-KIND       PIC X(4).
           05  OP-NUM        PIC S9(18)V9(18) SIGN IS LEADING SEPARATE.

       FD  RES-FILE.
       01  RES-REC.
           05  RES-REF       PIC X(40).
           05  RES-NUM       PIC S9(18)V9(18) SIGN IS LEADING SEPARATE.
           05  RES-STAT      PIC X(4).

       WORKING-STORAGE SECTION.
       01  OPS-STATUS        PIC XX VALUE SPACES.
       01  RES-STATUS        PIC XX VALUE SPACES.
       01  EOF-FLAG          PIC X VALUE "N".
           88  AT-EOF        VALUE "Y".

       01  STACK-TABLE.
           05  STK OCCURS 64 TIMES PIC S9(18)V9(18) COMP-3.
       01  SP                PIC S9(4) COMP VALUE ZERO.

       01  A-VAL             PIC S9(18)V9(18) COMP-3.
       01  B-VAL             PIC S9(18)V9(18) COMP-3.
       01  R-VAL             PIC S9(18)V9(18) COMP-3.
       01  P-ACC             PIC S9(18)V9(18) COMP-3.
       01  EXP-INT           PIC S9(9) COMP.
       01  EXP-IDX           PIC S9(9) COMP.

       01  CUR-REF           PIC X(40) VALUE SPACES.
       01  CUR-STAT          PIC X(4)  VALUE "OK  ".

       PROCEDURE DIVISION.

       MAIN-PARA.
           OPEN INPUT OPS-FILE
           IF OPS-STATUS NOT = "00"
               DISPLAY "cannot open OPS.DAT, status " OPS-STATUS
               MOVE 3 TO RETURN-CODE
               STOP RUN
           END-IF
           OPEN OUTPUT RES-FILE
           IF RES-STATUS NOT = "00"
               DISPLAY "cannot open RESULTS.DAT, status " RES-STATUS
               MOVE 3 TO RETURN-CODE
               STOP RUN
           END-IF

           PERFORM UNTIL AT-EOF
               READ OPS-FILE
                   AT END SET AT-EOF TO TRUE
                   NOT AT END PERFORM HANDLE-OP
               END-READ
           END-PERFORM

           CLOSE OPS-FILE
           CLOSE RES-FILE
           MOVE 0 TO RETURN-CODE
           STOP RUN.

       HANDLE-OP.
           IF OP-REF NOT = CUR-REF
               MOVE OP-REF TO CUR-REF
               MOVE "OK  " TO CUR-STAT
               MOVE ZERO TO SP
           END-IF

           EVALUATE OP-KIND
               WHEN "PUSH" PERFORM DO-PUSH
               WHEN "ADD " PERFORM DO-ADD
               WHEN "SUB " PERFORM DO-SUB
               WHEN "MUL " PERFORM DO-MUL
               WHEN "DIV " PERFORM DO-DIV
               WHEN "NEG " PERFORM DO-NEG
               WHEN "POW " PERFORM DO-POW
               WHEN "END " PERFORM DO-END
               WHEN OTHER  MOVE "KIND" TO CUR-STAT
           END-EVALUATE.

       DO-PUSH.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           IF SP >= 64
               MOVE "OVFL" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           ADD 1 TO SP
           MOVE OP-NUM TO STK(SP).

       POP-TWO.
           IF SP < 2
               MOVE "UNDR" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           MOVE STK(SP) TO B-VAL
           SUBTRACT 1 FROM SP
           MOVE STK(SP) TO A-VAL.

       DO-ADD.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           PERFORM POP-TWO
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           COMPUTE R-VAL = A-VAL + B-VAL
               ON SIZE ERROR MOVE "OVFL" TO CUR-STAT
               NOT ON SIZE ERROR MOVE R-VAL TO STK(SP)
           END-COMPUTE.

       DO-SUB.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           PERFORM POP-TWO
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           COMPUTE R-VAL = A-VAL - B-VAL
               ON SIZE ERROR MOVE "OVFL" TO CUR-STAT
               NOT ON SIZE ERROR MOVE R-VAL TO STK(SP)
           END-COMPUTE.

       DO-MUL.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           PERFORM POP-TWO
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           COMPUTE R-VAL ROUNDED MODE IS NEAREST-EVEN = A-VAL * B-VAL
               ON SIZE ERROR MOVE "OVFL" TO CUR-STAT
               NOT ON SIZE ERROR MOVE R-VAL TO STK(SP)
           END-COMPUTE.

       DO-DIV.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           PERFORM POP-TWO
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
      *> A zero divisor returns DIV0. It does not return zero, and it does
      *> not return the numerator. An absent value is not a measurement.
           IF B-VAL = ZERO
               MOVE "DIV0" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           COMPUTE R-VAL ROUNDED MODE IS NEAREST-EVEN = A-VAL / B-VAL
               ON SIZE ERROR MOVE "OVFL" TO CUR-STAT
               NOT ON SIZE ERROR MOVE R-VAL TO STK(SP)
           END-COMPUTE.

       DO-NEG.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           IF SP < 1
               MOVE "UNDR" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           COMPUTE STK(SP) = 0 - STK(SP).

       DO-POW.
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           PERFORM POP-TWO
           IF CUR-STAT NOT = "OK  " THEN EXIT PARAGRAPH END-IF
           IF FUNCTION INTEGER-PART(B-VAL) NOT = B-VAL
               MOVE "POWX" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           COMPUTE EXP-INT = FUNCTION INTEGER-PART(B-VAL)
           IF EXP-INT < 0
               MOVE "POWX" TO CUR-STAT
               EXIT PARAGRAPH
           END-IF
           MOVE 1 TO P-ACC
           PERFORM VARYING EXP-IDX FROM 1 BY 1 UNTIL EXP-IDX > EXP-INT
               COMPUTE P-ACC ROUNDED MODE IS NEAREST-EVEN
                   = P-ACC * A-VAL
                   ON SIZE ERROR MOVE "OVFL" TO CUR-STAT
               END-COMPUTE
               IF CUR-STAT NOT = "OK  "
                   EXIT PERFORM
               END-IF
           END-PERFORM
           IF CUR-STAT = "OK  "
               MOVE P-ACC TO STK(SP)
           END-IF.

       DO-END.
           MOVE CUR-REF TO RES-REF
           MOVE CUR-STAT TO RES-STAT
           IF CUR-STAT = "OK  " AND SP = 1
               MOVE STK(1) TO RES-NUM
           ELSE
               MOVE ZERO TO RES-NUM
               IF CUR-STAT = "OK  "
                   MOVE "STCK" TO RES-STAT
               END-IF
           END-IF
           WRITE RES-REC
           MOVE ZERO TO SP.

       END PROGRAM LEDGER.
