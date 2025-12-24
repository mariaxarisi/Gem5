#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int N;
    long long sum = 0;
    
    if (argc != 2) {
        printf("Usage: %s <N>\n", argv[0]);
        return 1;
    }
    
    N = atoi(argv[1]);
    
    if (N <= 0) {
        printf("Please provide a positive integer\n");
        return 1;
    }
    
    for (int i = 1; i <= N; i++) {
        sum += i;
    }
    
    printf("Sum from 1 to %d = %lld\n", N, sum);
    
    return 0;
}