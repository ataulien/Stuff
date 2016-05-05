#pragma once
#include <cstdint>

/**
 * Various handle-definitions
 */
namespace Handle
{
    typedef uint16_t MaterialHandle;
    typedef uint16_t TextureHandle;
    typedef uint16_t VBHandle;
    typedef uint16_t IBHandle;
    typedef uint16_t EntityHandle;
    typedef uint16_t MeshHandle;

    // Internal handle-types (API specific)
    typedef uint16_t InternalTextureHandle;
    typedef uint16_t InternalVBHandle;
    typedef uint16_t InternalIBHandle;
}