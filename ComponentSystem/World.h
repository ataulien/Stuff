#pragma once

#include "AllocatorBundle.h"
#include "Config.h"
#include "Texture.h"
#include "Entities.h"
#include "StaticReferencedAllocator.h"

namespace World
{
    struct WorldAllocators
    {

        typedef Memory::StaticReferencedAllocator<Textures::Texture, Config::MAX_NUM_LEVEL_TEXTURES> TextureAllocator;
        Components::ComponentAllocator m_Components;
        TextureAllocator m_LevelTextures;
    };

    /**
     * All information inside this struct are only valid at a certain time of the frame, where no entities can be
     * (de)allocated or moved around in any way. The indices stored inside the vectors are a direct mapping to the
     * Elements inside the allocator, which are to be seen as invalid in the next frame!
     */
    struct TransientEntityFeatures
    {
        std::vector<size_t> m_VisibleEntities;
    };

    class WorldInstance
    {
    public:
        WorldInstance(){}
        /**
         * Creates an entity with the given components and returns its handle
         */
        Components::ComponentAllocator::Handle addEntity(Components::ComponentMask components);

        /**
         * Updates this world instances entities
         */
        void onFrameUpdate(double deltaTime);

        /**
         * Data access
         */
        Components::ComponentAllocator::DataBundle getComponentDataBundle()
        {
            return m_Allocators.m_Components.getDataBundle();
        }
    protected:
        WorldAllocators m_Allocators;
        TransientEntityFeatures m_TransientEntityFeatures;
    };
}