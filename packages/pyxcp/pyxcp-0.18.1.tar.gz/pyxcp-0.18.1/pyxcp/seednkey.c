
#include <assert.h>
#include <stdint.h>

#define XcpSkExtFncAck                      (0)
#define XcpSkExtFncErrPrivilegeNotAvailable (1)
#define XcpSkExtFncErrInvalidSeedLength     (2)
#define XcpSkExtFncErrUnsufficientKeyLength (3)

uint32_t XCP_GetAvailablePrivileges(uint8_t * availablePrivilege);

uint32_t XCP_ComputeKeyFromSeed(uint8_t requestedPrivilege, uint8_t byteLengthSeed, uint8_t * pointerToSeed,
        uint8_t * byteLengthKey,uint8_t * pointerToKey);


uint32_t XCP_GetAvailablePrivileges(uint8_t * availablePrivilege)
{

}

uint32_t XCP_ComputeKeyFromSeed(uint8_t requestedPrivilege, uint8_t lenSeed, uint8_t * seed, uint8_t * lenKey,uint8_t * key)
{
    assert(lenSeed == 5);

    key[0] = seed[0] ^ 0x55;
    key[1] = seed[1] ^ 0x11;
    key[2] = seed[2] ^ 0x22;
    key[3] = seed[3] ^ 0x33;
    key[4] = seed[4] ^ 0xaa;
    *lenKey = 5;
    return XcpSkExtFncAck;
}
