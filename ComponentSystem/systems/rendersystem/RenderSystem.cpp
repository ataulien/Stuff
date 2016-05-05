//
// Created by andre on 03.05.16.
//

#include "RenderSystem.h"

using namespace System;

RenderSystem::RenderSystem()
{

}

RenderSystem::~RenderSystem()
{

}

void RenderSystem::drawEntities(size_t* indices, size_t numIndices, Components::ComponentAllocator::DataBundle& alloc)
{
    Components::EntityComponent* entities = std::get<Components::EntityComponent*>(alloc.m_Data);
    Components::PositionComponent* positions = std::get<Components::PositionComponent*>(alloc.m_Data);
    Components::BBoxComponent* bboxes = std::get<Components::BBoxComponent*>(alloc.m_Data);

    m_Buffer.clear();
    for(size_t i=0;i<numIndices;i++)
    {
        m_Buffer += "Entity: " + positions[i].m_WorldMatrix.Translation().toString() + "\n";
    }

    std::cout << m_Buffer;
}





