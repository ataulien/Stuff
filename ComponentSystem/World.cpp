#include <iostream>
#include "World.h"
#include <bitset>

using namespace World;

Components::ComponentAllocator::Handle WorldInstance::addEntity(Components::ComponentMask components)
{
    auto h = m_Allocators.m_Components.createObject();

    Components::EntityComponent& entity = m_Allocators.m_Components.getElement<Components::EntityComponent>(h);
    entity.m_ComponentMask = components;

    Components::BBoxComponent& bbox = m_Allocators.m_Components.getElement<Components::BBoxComponent>(h);
    bbox.m_BBox3D.min = Math::float3(rand() % 1000,rand() % 1000,rand() % 1000);
    bbox.m_BBox3D.max = bbox.m_BBox3D.min;


    // TODO: Make generic "on entity created"-method or something

    return h;
}

void WorldInstance::onFrameUpdate(double deltaTime)
{
    Components::EntityComponent* entities = m_Allocators.m_Components.getElements<Components::EntityComponent>();
    Components::PositionComponent* positions = m_Allocators.m_Components.getElements<Components::PositionComponent>();
    Components::BBoxComponent* bboxes = m_Allocators.m_Components.getElements<Components::BBoxComponent>();
    size_t range = m_Allocators.m_Components.getNumObtainedElements();

    m_TransientEntityFeatures.m_VisibleEntities.clear();

    for (size_t i = 0; i < range; i++)
    {
        // Try to cull the entities
        // TODO: Can do this in paralell! (Don't forget to aggregate m_VisibleEntities afterwards against cache-trashing)
        if((entities[i].m_ComponentMask & Components::BBoxComponent::MASK) != 0)
        {
            // TODO: Actually cull

            // Entity is visible, save that
            m_TransientEntityFeatures.m_VisibleEntities.push_back(i);
        }
    }
}



