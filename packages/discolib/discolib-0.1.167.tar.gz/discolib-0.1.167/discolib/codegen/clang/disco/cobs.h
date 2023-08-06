#pragma once

#include <stdint.h>
#include <string.h>

size_t cobs_encode(const uint8_t *packet, size_t length, uint8_t *encoded);
size_t cobs_decode(const uint8_t *packet, size_t length, uint8_t *decoded);
