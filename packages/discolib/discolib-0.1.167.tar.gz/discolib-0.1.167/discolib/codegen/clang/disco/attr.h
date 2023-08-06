#pragma once
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "types.h"
#include "math.h"

#define ATTR_NAME_LEN 128

typedef uint8_t disco_port;

#pragma region Standard Attribute Types

/**
 *  @brief A single disco attribute.
 */
typedef struct {
    disco_port port;
    size_t size;
    uint8_t* setpoint;
    uint8_t* readback;
    uint8_t* setpoint_default;
    char name[ATTR_NAME_LEN];
    disco_type type;
} disco_attr;

/**
 *  @brief A byte-type attribute.
 */
typedef struct {
    uint8_t setpoint;
    uint8_t readback;
    uint8_t setpoint_default;
} byte_attr;

/**
 *  @brief An int-type attribute.
 */
typedef struct {
    int32_t setpoint;
    int32_t readback;
    int32_t setpoint_default;
} int_attr;

/**
 *  @brief An unsigned int-type attribute.
 */
typedef struct {
    uint32_t setpoint;
    uint32_t readback;
    uint32_t setpoint_default;
} uint_attr;

/**
 *  @brief A float-type attribute.
 */
typedef struct {
    float_t setpoint;
    float_t readback;
    float_t setpoint_default;
} float_attr;

#pragma endregion Standard Attribute Types

#pragma region Public Functions

void attr_init(void);
disco_attr* attr_find(disco_port port, bool *success);

#pragma endregion Public Functions

#pragma region DiscoGen
#define N_ATTR 0
#pragma endregion DiscoGen

/**
 *  @brief All attributes collected together.
 */
extern disco_attr disco_attrs[N_ATTR];
