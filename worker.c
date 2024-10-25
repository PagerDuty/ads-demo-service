#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define PAYLOAD_MB 10


void process_work(char *payload) {
    size_t size = PAYLOAD_MB * 1024 * 1024;

    printf("Processing work...\n");
    for (size_t i = 0; i < size; i += 4096) {
        payload[i] = 0;  
    }
    sleep(1);
}


void controller() {
    while (1) {
        char *buffer = malloc(PAYLOAD_MB * 1024 * 1024 * sizeof(char));
        process_work(buffer);
        //free(buffer);
    }
}

int main() {
    controller();    
    return 0;
}