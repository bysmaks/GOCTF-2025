#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_MEMES 10
#define MAX_MEME_LEN 128

char memes[MAX_MEMES][MAX_MEME_LEN] = {
    "Когда забыл сделать git push",
    "404 Brain Not Found",
    "Синтаксическая ошибка в жизни",
    "Segmentation fault (core dumped)",
    "while(true) { sleep(); }",
    "sudo make me a sandwich",
    "У меня есть 99 проблем, но 127 из них - переполнение буфера",
    "Это не баг, это фича",
    "Работает? Не трогай!",
    "Я не ленивый, я в энергосберегающем режиме"
};

void run_program() {
    char flag[64];
    FILE *fp = fopen("flag.txt", "r");
    if(fp) {
        fgets(flag, sizeof(flag), fp);
        fclose(fp);
    } else {
        strcpy(flag, "flag{default_flag}");
    }
    char *stack_flag = flag;

    char user_memes[MAX_MEMES][MAX_MEME_LEN];
    int meme_count = 0;
    srand(time(0));

    while(1) {
        printf("\n1. Show random meme\n");
        printf("2. Add your meme\n");
        printf("3. Exit\n");
        printf("Choice: ");
        fflush(stdout);

        int choice;
        scanf("%d", &choice);
        getchar();

        switch(choice) {
            case 1: {
      if(meme_count > 0) {
          int idx = rand() % meme_count;
         printf("Random meme: ");
         printf(user_memes[idx]); 
         printf("\n");
     } else {
         printf("No memes added yet. Showing default:\n");
         int idx = rand() % MAX_MEMES;
         printf("%s\n", memes[idx]);  
     }
      break;
  }
            case 2: {
                if(meme_count < MAX_MEMES) {
                    printf("Enter your meme (max %d chars): ", MAX_MEME_LEN-1);
                    fgets(user_memes[meme_count], MAX_MEME_LEN, stdin);
                    user_memes[meme_count][strcspn(user_memes[meme_count], "\n")] = '\0';
                    meme_count++;
                    printf("Meme added!\n");
                } else {
                    printf("Meme wall is full!\n");
                }
                break;
            }
            case 3:
                printf("Exiting...\n");
                return;
            default:
                printf("Invalid choice!\n");
        }
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("=== Memes Wall ===\n");
    run_program();
    return 0;
}
