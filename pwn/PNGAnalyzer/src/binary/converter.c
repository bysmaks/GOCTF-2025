#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>
typedef struct {
    uint32_t width;
    uint32_t height;
} png_size_data;

typedef struct {
    uint8_t *data;
    size_t length;
} png_data;

void swap_endian(uint32_t *value) {
    *value = __builtin_bswap32(*value);
}

void get_something() {
    FILE *flag = fopen("/flag.txt", "r");
    if (!flag) {
        perror("Error opening flag. Write to organizators.");
        exit(1);
    }

    char buf[128];
    if (fgets(buf, sizeof(buf), flag)) {
        printf("FLAG: %s\n", buf);
    }
    fclose(flag);
    exit(0);
}

png_size_data get_png_size_data(const char *filepath) {
    png_size_data result = {0, 0};
    FILE *file = fopen(filepath, "rb");
    if (!file) {
        perror("Error opening file");
        return result;
    }

    uint8_t header[8];
    fread(header, 1, 8, file);

    if (header[0] != 0x89 || header[1] != 'P' || header[2] != 'N' || header[3] != 'G' ||
        header[4] != 0x0D || header[5] != 0x0A || header[6] != 0x1A || header[7] != 0x0A) {
        fprintf(stderr, "Not a valid PNG file\n");
        fclose(file);
        return result;
    }

    uint32_t length;
    fread(&length, 1, 4, file);
    swap_endian(&length);

    char type[4];
    fread(type, 1, 4, file);
    if (type[0] != 'I' || type[1] != 'H' || type[2] != 'D' || type[3] != 'R') {
        fprintf(stderr, "Invalid chunk type, expected IHDR\n");
        fclose(file);
        return result;
    }

    uint32_t width, height;
    fread(&width, 1, 4, file);
    fread(&height, 1, 4, file);
    swap_endian(&width);
    swap_endian(&height);

    result.width = width;
    result.height = height;
    fclose(file);

    return result;
}

png_data parse_png(const char *filepath, const int length) {
    uint8_t buffer[length];
    png_data result = {NULL, 0};
    uint32_t chunk_length;
    char chunk_type[5] = {0};
    uint32_t buffer_offset = 0;
    

    FILE *file = fopen(filepath, "rb");
    if (!file) {
        perror("Error opening file");
        png_data empty_data = {NULL, 0};
        return empty_data;
    }

    uint8_t signature[8];
    if (fread(signature, 1, 8, file) != 8 || memcmp(signature, "\x89PNG\r\n\x1a\n", 8) != 0) {
        fprintf(stderr, "Not a valid PNG file\n");
        fclose(file);
        png_data empty_data = {NULL, 0};
        return empty_data;
    }
    
    while (1) {
        
        if (fread(&chunk_length, 1, 4, file) != 4) {
            break; 
        }
        chunk_length = ntohl(chunk_length);

        
        if (fread(chunk_type, 1, 4, file) != 4) {
            break;
        }
        
        printf("Chunk: %s, Length: %u\n", chunk_type, chunk_length);
        if (fread(buffer + buffer_offset, 1, chunk_length, file) != chunk_length) {
            fprintf(stderr, "Error reading chunk data\n");
            fclose(file);
            png_data empty_data = {NULL, 0};
            return empty_data;
        }
        
        uint8_t crc[4];
        if (fread(crc, 1, 4, file) != 4) {
            break;
        }

        if (strcmp(chunk_type, "IHDR") == 0) {
            printf("IHDR Chunk: Image header\n\n");
        } else if (strcmp(chunk_type, "IDAT") == 0) {
            buffer_offset += chunk_length;
            printf("IDAT Chunk: Image data\n");
            printf("Last 8 bytes of data: ");
            for (size_t i = buffer_offset - 8; i < buffer_offset; i++) {
                printf("%02x ", buffer[i]);
        }
        printf("\n\n");
        } else if (strcmp(chunk_type, "IEND") == 0) {
            printf("IEND Chunk: End of PNG file\n");
            break;
        }
    }

    fclose(file);
    result.data = malloc(buffer_offset);
    if (!result.data) {
        perror("malloc failed");
        png_data empty_data = {NULL, 0};
        return empty_data;
    }
    memcpy(result.data, buffer, buffer_offset);

    result.length = buffer_offset;
    return result;
}

void free_png_data(png_data *data) {
    if (data->data) {
        free(data->data);
    }
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <path_to_png>\n", argv[0]);
        return 1;
    }

    png_size_data data = get_png_size_data(argv[1]);
    if (data.width > 0 && data.height > 0) {
        printf("Image width: %u\n", data.width);
        printf("Image height: %u\n", data.height);
    } else {
        printf("Failed to read PNG file\n");
    }
    png_data png_data = parse_png(argv[1], data.width * data.height);
    if (png_data.length) {
        printf("Parsed PNG data length: %zu\n", png_data.length);
        free_png_data(&png_data);
    } else {
        printf("Failed to parse PNG file\n");
    }
    return 0;
}
