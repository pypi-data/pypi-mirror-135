#include "attr.h"
#include "cobs.h"
#include "disco.h"
#include "protocol.h"
#include "command.h"

uint8_t encoded[1024] = {0};
uint8_t decoded[1024] = {0};
uint8_t scratchpad[1024] = {0};

/**
 *  @brief Respond to an entire validated packet.
 *  @param packet A packet to parse.
 */
size_t protocol_parse_packet(uint8_t *packet, size_t len, uint8_t *response) {
    cobs_decode(packet, len, decoded);   
    uint8_t cmd = decoded[CMD_INDEX];
    command_handle(cmd, &decoded[DATA_INDEX]);
    size_t response_length = 0;
    if (command_response_required(cmd)) {
        response_length = command_get_response(scratchpad);
        response_length = cobs_encode(scratchpad, response_length, encoded);
        memcpy(response, encoded, response_length);
        response[response_length++] = 0; // Add delimeter.
    }
    return response_length;
}
