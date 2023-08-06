#include "attr.h"
#include "cobs.h"
#include "command.h"
#include "protocol.h"

uint8_t response_buffer[1024];
size_t response_length = 0;
disco_attr* attr;

static size_t command_complete_response(size_t length) {
    response_buffer[length++] = 0x10; // TODO: Checksum
    return length;
}

static bool attr_exists(uint8_t port) {
    bool exists;
    attr = attr_find(port, &exists);
    return exists;
}

void command_handle(uint8_t cmd, uint8_t* data) {
    uint8_t port;
    response_length = 0;  // Reset all response lengths for the new cmd.
    switch (cmd)
    {
    case CMD_GET_PORTS:
        for (size_t i = 0; i < (sizeof(disco_attrs) / sizeof(disco_attrs[0])); i++) {
            response_buffer[response_length++] = disco_attrs[i].port;
        }
        response_length = command_complete_response(response_length);
        break;
    case CMD_GET_PORT_NAME:
        port = data[0];
        if (attr_exists(port)) {
            memcpy(&response_buffer[response_length], &(attr->name), sizeof(attr->name));
            response_length += sizeof(attr->name);
            response_length = command_complete_response(response_length);
        }
        break;
    case CMD_GET_PORT_TYPE:
        port = data[0];
        if (attr_exists(port)) {
            memcpy(&response_buffer[response_length], &(attr->type), sizeof(attr->type));
            response_length += sizeof(attr->type);
            response_length = command_complete_response(response_length);
        }
        break;
    case CMD_GET_PORT_READBACK:
        port = data[0];
        if (attr_exists(port)) {
            memcpy(&response_buffer[response_length], attr->readback, attr->size);
            response_length += attr->size;
            response_length = command_complete_response(response_length);
        }
        break;
    case CMD_GET_PORT_SETPOINT:
        port = data[0];
        if (attr_exists(port)) {
            memcpy(&response_buffer[response_length], attr->setpoint, attr->size);
            response_length += attr->size;
            response_length = command_complete_response(response_length);
        }
        break;
    case CMD_SET_PORT_SETPOINT:
        port = data[0];
        if (attr_exists(port)) {
            memcpy(attr->setpoint, &data[1], attr->size);
        }
        break;
    default:
        break;
    }
}

bool command_response_required(uint8_t cmd) { return cmd < 0x25; }

size_t command_get_response(uint8_t *response) {
    memcpy(response, response_buffer, response_length);
    return response_length;
}
