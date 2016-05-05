#pragma once
#include "Utils.h"
#include "Handle.h"
#include "HandleDef.h"
#include "Utils.h"
#include "StaticLevelMesh.h"
#include "VertexTypes.h"
#include "AllocatorBundle.h"
#include "Config.h"

/**
 * List of all available components
 */
#define ALL_COMPONENTS EntityComponent, LogicComponent, PositionComponent, NBBoxComponent, BBoxComponent, StaticMeshComponent

namespace Components
{
    typedef uint32_t ComponentMask;

    /**
     * Component which can be expected to be valid on all entities.
     * This stores, which components are valid for that entity.
     * Since every entity creates all components in the background, a component being "valid"
     * only means, that it's flag was registered inside m_ComponentMask. The memory would be there in all cases,
     * however accessing a component without it being registered is not supported and could lead to undefined behavior
     * (or just 'nothing', in most cases really)
     */
    struct EntityComponent
    {
        ComponentMask m_ComponentMask;
    };

    struct Component : public Handle::HandleTypeDescriptor<Handle::EntityHandle>
    {

    };

    struct PositionComponent : public Component
    {
        enum { MASK = 1 << 1 };
        Math::Matrix m_WorldMatrix;
    };

    /**
     * Entity with one or more BBoxes.
     * Beware of the cache-miss when accessing these!
     */
    struct NBBoxComponent : public Component
    {
        enum { MASK = 1 << 2 };

        std::vector<Utils::BBox3D> m_BBox3D;
    };

    /**
     * Entitiy with only one BBox
     */
    struct BBoxComponent : public Component
    {
        enum { MASK = 1 << 3 };

        Utils::BBox3D m_BBox3D;
    };

    /**
     * Entity with a static mesh
     */
    struct StaticMeshComponent : public Component
    {
        enum { MASK = 1 << 4 };

        LevelMesh::StaticLevelMesh<Mesh::PositionVertex, uint32_t> ::HandleType m_StaticMeshVisual;
    };

    /**
     * Generic logic component, can execute scripts, etc
     */
    struct LogicComponent : public Component
    {
        // TODO: Implement
    };

    /**
     * Adds a component to the given Entity-Component
     */
    template<typename T>
    void addComponent(EntityComponent& e)
    {
        // See "EntityComponent" for further information
        e.m_ComponentMask |= T::Mask;
    }

    /**
     * Removes a component from the given Entity-Component
     */
    template<typename T>
    void removeComponent(EntityComponent& e)
    {
        // See "EntityComponent" for further information
        e.m_ComponentMask &= ~T::Mask;
    }

    /**
     * Creates a ComponentMask from uint32_t, for cleaner access
     */
    static ComponentMask makeEntityMask(uint32_t mask)
    {
        return static_cast<ComponentMask>(mask);
    }

    /**
     * Default allocator-type
     */
    typedef Memory::AllocatorBundle<Config::MAX_NUM_LEVEL_ENTITIES, ALL_COMPONENTS> ComponentAllocator;
}