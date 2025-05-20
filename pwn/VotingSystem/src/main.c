#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define C "Work, sleep, party.\n"
#define B "No relax, no free time. Just work!\n"
#define A "Make your life great again!\n"

void Vote_Validation_System(char* candidate_name) {
        if (strstr(candidate_name, "A") != NULL) {
        printf("Error: This candidate is forbidden! Shutting down the system...\n");
        exit(1);
    }
}

void Voting_Booth() {
    char vote_input[256] = {0};
    char welcome_msg[512];
    
    snprintf(welcome_msg, sizeof(welcome_msg),
        "\nWelcome to Digital Voting System\n"
        "Choose your candidate:\n"
        "%s"
        "%s", 
        B, 
        C);
    
    printf(welcome_msg); 
    gets(vote_input);
    Vote_Validation_System(vote_input);
    
    printf("You voted for: ");
    printf(vote_input);
    printf("\nThank you for voting!\n");
}

int main(int argc, char* argv[]) {
    printf("=== Digital Voting System v1.0 ===\n");
    
    while(1) {
        Voting_Booth();
    }
}