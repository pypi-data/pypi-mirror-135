#include "attr.h"

void attr_init() {
    const void* disco_ram_ptr = &disco_attrs;
    for (int i = 0; i < N_ATTR; i++) {
        disco_attr *attr = (disco_attr*) (disco_ram_ptr + (i * sizeof(disco_attr)));
        memcpy(attr->setpoint, attr->setpoint_default, attr->size);
    }
}

disco_attr* attr_find(disco_port port, bool *success) {
    size_t disco_attr_ptr = 0;
    disco_attr* attr;
    while (disco_attr_ptr < (sizeof(disco_attrs) / sizeof(disco_attr))) {
        attr = &(disco_attrs[disco_attr_ptr]);
        if (attr->port == port) {
            *success = true;
            return attr;
        }
        disco_attr_ptr++;
    }
    success = false;
    return attr;
}

#pragma region DiscoGen
#pragma endregion DiscoGen
