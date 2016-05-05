#include <iostream>
#include <vector>
#include "Utils.h"
#include "StaticReferencedAllocator.h"
#include "StaticMesh.h"
#include "VertexTypes.h"
#include "Materials.h"
#include "StaticLevelMesh.h"
#include "AllocatorBundle.h"
#include "World.h"
#include "utils/mathlib.h"
#include "systems/rendersystem/RenderSystem.h"
#include "EntityActions.h"

using namespace std;

struct Entity
{
    float position[3];
    int data[32];
    Math::float4 lolz;
};

typedef Memory::StaticReferencedAllocator<Entity, 4096> EntityAlloc;
typedef Memory::StaticReferencedAllocator<Materials::TexturedMaterial, 2048> MaterialAlloc;

struct RenderPacket
{
    uint16_t vb;
    uint16_t ib;
    uint32_t startIdx;
    uint32_t numIdx;
    uint16_t materialIdx;
};

std::vector<RenderPacket> RenderPackets;
std::vector<RenderPacket*> RenderPacketsPtr;

int main()
{
    cout << "Hello, World!" << endl;

    srand(time(NULL));

    /*EntityAlloc alloc;

    Memory::Handle h = alloc.createObject();
    Entity& e = alloc.getElement(h);
    e.position[0] = 123.0f;

    std::vector<Memory::Handle> handles;
    for(size_t i=0;i<10;i++)
    {
        handles.push_back(alloc.createObject());
        Entity& e = alloc.getElement(handles.back());
        e.position[0] = i;
    }

    for(size_t i=0;i<5;i++)
    {
        alloc.removeObject(handles[i]);
    }

    h = alloc.createObject();
    Entity& e2 = alloc.getElement(h);
    e2.position[0] = 999;

    LevelMesh::StaticLevelMeshFixed<Mesh::PositionVertex, uint32_t, 1> mesh;

    std::vector<Mesh::PositionVertex> vertices;
    std::vector<uint32_t> indices;

    for(size_t i=0;i<10000;i++) {
        vertices.push_back({1, 2, 3});
        indices.push_back(i);
    }

    LevelMesh::fromVertexData(mesh, vertices, indices, 0);

    Memory::AllocatorBundle<4096, int, float, Entity> allocBundle;
    //allocBundle.getAllocator<int>().createObject();

    allocBundle.createObject();
    allocBundle.createObject();
    allocBundle.createObject();
    allocBundle.createObject();*/

    World::WorldInstance world;

    cout << "Instanciated world!" << endl;

    long start = Utils::currentTimestamp();
    for(int i=0;i<20000;i++)
    {
        world.addEntity(Components::makeEntityMask(  Components::BBoxComponent::MASK
                                                   | Components::PositionComponent::MASK
                                                   | Components::StaticMeshComponent::MASK));


    }

    std::cout << "Object-creation took " << Utils::currentTimestamp() - start << "ms" << std::endl;

    int iterations = 1000;
    start = Utils::currentTimestamp();

    for(int i=0;i<iterations;i++)
    {
        world.onFrameUpdate(0.0f);
    }

    std::cout << "FrameUpdate took " << Utils::currentTimestamp() - start << "ms" << std::endl;
    std::cout << " - Single update: " << (Utils::currentTimestamp() - start) / (float)iterations << "ms" << std::endl;



    auto bundle = world.getComponentDataBundle();
    std::vector<size_t> checkIdx(bundle.m_NumElements);
    size_t numCheck=0;

    for(size_t i=0, j=0;j<bundle.m_NumElements;i++, j+=2)
    {
        checkIdx[i] = j;
        numCheck++;
    }

    size_t numVisible;
    std::vector<size_t> visibleIdx(numCheck);

    start = Utils::currentTimestamp();

    for(int i=0;i<iterations;i++)
    {
        for(int j=0;j<100;j++) {
            Components::Actions::BBox::frustumVisibilityCheck(std::get<Components::BBoxComponent*>(bundle.m_Data),
                                                              checkIdx.data(), numCheck, visibleIdx.data(), numVisible);
        }
    }

    std::cout << "FrustumCheck took " << Utils::currentTimestamp() - start << "ms" << std::endl;
    std::cout << " - Single run: " << (Utils::currentTimestamp() - start) / (float)iterations << "ms" << std::endl;
    std::cout << " - - fps: " << 1.0 / (0.001 * (Utils::currentTimestamp() - start) / (float)iterations) << std::endl;

    std::cout << "Visible: " << numVisible << std::endl;

    System::RenderSystem rndSys;

    //rndSys.drawEntities();

    std::cout << "Done!" << std::endl;

    return 0;
}