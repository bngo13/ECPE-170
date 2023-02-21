.globl main
.text

# s0 = arr head
# s1 = n
# t1 = i
# t2 = j
# t3 = temp anything
main:
    la $s0, arr #s0 is arr head
    lw $s1, n #s1 is n

    addi $t1, $t1, 0 # t1 for i

    startForFirst:
        addi $t3, $s1, -1 # t3 = n - 1
        slt $t3, $t1, $t3 # if i < n - 1 | then t3 = 1 | else t3 = 0
        beq $t3, $zero, endForFirst
        addi $t2, $zero, 0 #t2 for j
        startForSecond:
            sub $t3, $s1, $t1 # t3 = n - i
            addi $t3, $t3, -1 # t3 = t3 - 1
                              # t3 = n - i - 1
            slt $t3, $t2, $t3 # if j < t3 | then t3 = 1 | else t3 = 0
            beq $t3, $zero, endForSecond

            add $t3, $t2, $t2 # half offset j
            add $t3, $t3, $t3 # full offset j
            add $t3, $t3, $s0 # add offset to base array
            lw $t4, 0($t3) # t4 = arr[j]

            addi $t3, $t2, 1 # t3 = j + 1
            add $t3, $t3, $t3 # half offset j*2
            add $t3, $t3, $t3 # full offset j*4
            add $t3, $t3, $s0 # add offset to base array
            lw $t5, 0($t3) # t5 = arr[j + 1]

            slt $t3, $t4, $t5 # if arr[j] < arr[j+1] | then t3 = 1 | else t3 = 0
            bne $t3, 0, endIfFirst # if arr[j] < arr[j+1] | then endIfFirst | else startIfFirst
            beq $t4, $t5, endIfFirst # covers <=

            startIfFirst:
                add $t3, $t2, $t2 # half offset j
                add $t3, $t3, $t3 # full offset j
                add $t3, $t3, $s0 # add offset to base array
                sw $t5, 0($t3) # arr[j+1] = arr[j]

                addi $t3, $t2, 1 # t3 = j + 1
                add $t3, $t3, $t3 # half offset j*2
                add $t3, $t3, $t3 # full offset j*4
                add $t3, $t3, $s0 # add offset to base array
                sw $t4, 0($t3) # arr[j] = arr[j + 1]

            endIfFirst:

            addi $t2, $t2, 1
            j startForSecond
        endForSecond:

        addi $t1, $t1, 1
        j startForFirst

    endForFirst:

    li $v0, 10
    syscall

.data
    arr: .word 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    n: .byte 10
