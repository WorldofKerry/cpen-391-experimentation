#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    // char uartReadData[] = "connectedgarbage"; // Example input string
    // int uartReadLen = 9;
    // char uartReadData[] = "capgarbage"; 
    // int uartReadLen = 3;
    char uartReadData[] = "id,0qewfadsv"; 
    int uartReadLen = 4;
    
    uartReadData[uartReadLen] = '\0'; 
    char *cmd, *data;
    cmd = strtok(uartReadData, ",");
    int data_length = uartReadLen - strlen(cmd) - 1;
    printf("Command: %s\n", cmd);
    if (data_length > 0) {
        data = malloc((data_length + 1) * sizeof(*data));
        memcpy(data, uartReadData + strlen(cmd) + 1, data_length);
        printf("Data: %s\n", data);
    }
    // free(uartReadData);

    return 0;
}
