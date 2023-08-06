#pragma once

#include <stdint.h>
#include <string.h>

#define CMD_INDEX 0
#define DATA_INDEX 1


size_t protocol_parse_packet(uint8_t *packet, size_t len, uint8_t *response);
