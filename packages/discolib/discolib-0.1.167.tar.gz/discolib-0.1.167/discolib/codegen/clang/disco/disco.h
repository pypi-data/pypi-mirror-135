#pragma once
#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include "attr.h"

void disco_init(void);
size_t disco_packet_handle(uint8_t *packet, size_t len, uint8_t *response);
