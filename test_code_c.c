#include <stdio.h>
#include <string.h>

void reverse(char s[]) {
    int length = strlen(s);
    int c, i, j;

    for (i = 0, j = length - 1; i < j; i++, j--) {
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

int main() {
    int T = 0;
    scanf("%d", &T);
    while(T--) {
        char str[1024];
        scanf("%s", &str);
        reverse(str);
        printf("%s\n", str);
    }
    return 0;
}
