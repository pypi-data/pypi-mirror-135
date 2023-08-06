#include "cobs.h"

size_t cobs_encode(const uint8_t *packet, size_t length, uint8_t *encoded) {
    uint8_t *encode = encoded; // Encoded byte pointer
	uint8_t *codep = encode++; // Output code pointer
	uint8_t code = 1; // Code value

	for (const uint8_t *byte = (const uint8_t *)packet; length--; ++byte)
	{
		if (*byte) // Byte not zero, write it
			*encode++ = *byte, ++code;

		if (!*byte || code == 0xff) // Input is zero or block completed, restart
		{
			*codep = code, code = 1, codep = encode;
			if (!*byte || length)
				++encode;
		}
	}
	*codep = code; // Write final code value

	return (size_t)(encode - encoded);
}

size_t cobs_decode(const uint8_t *packet, size_t length, uint8_t *decoded) {
    const uint8_t *byte = packet; // Encoded input byte pointer
	uint8_t *decode = (uint8_t *)decoded; // Decoded output byte pointer

	for (uint8_t code = 0xff, block = 0; byte < packet + length; --block)
	{
		if (block) // Decode block byte
			*decode++ = *byte++;
		else
		{
			if (code != 0xff) // Encoded zero, write it
				*decode++ = 0;
			block = code = *byte++; // Next block length
			if (!code) // Delimiter code found
				break;
		}
	}

	return (size_t)(decode - (uint8_t *)decoded);
}
