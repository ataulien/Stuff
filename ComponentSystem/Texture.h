#pragma once
#include "Handle.h"
#include "HandleDef.h"

namespace Textures
{
    template<typename THDL>
    struct _Texture : public Handle::HandleTypeDescriptor<Handle::TextureHandle>
    {
        THDL m_TextureHandle;
    };

    typedef _Texture<Handle::InternalTextureHandle> Texture;
}