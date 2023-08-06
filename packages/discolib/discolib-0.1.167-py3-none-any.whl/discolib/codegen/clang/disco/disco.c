#include "attr.h"
#include "disco.h"
#include "protocol.h"

void disco_init() { attr_init(); }
size_t disco_packet_handle(uint8_t *packet, size_t len, uint8_t *response) { return protocol_parse_packet(packet, len, response); }
