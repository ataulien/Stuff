#pragma once

#include <cstddef>
#include "../../Entities.h"
#include "../../World.h"

namespace System
{
    class RenderSystem
    {
    public:
        RenderSystem();
        virtual ~RenderSystem();

        /**
         * Draws the entities with the given indices of the specified component-allocator
         */
        void drawEntities(size_t* indices, size_t numIndices, Components::ComponentAllocator::DataBundle& alloc);

    private:
        std::string m_Buffer; // TODO: Temporary, take out!
    };
}
