#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define CMD_GET_PORTS 0x01
#define CMD_GET_PORT_NAME 0x02
#define CMD_GET_PORT_TYPE 0x03
#define CMD_GET_PORT_READBACK 0x04
#define CMD_GET_PORT_SETPOINT 0x05

#define CMD_SET_PORT_SETPOINT 0x25

void command_handle(uint8_t cmd, uint8_t* data);
bool command_response_required(uint8_t cmd);
size_t command_get_response(uint8_t *response);
