#include <iostream>
#include <vector>
#include "StaticReferencedAllocator.h"
#include "StaticMesh.h"
#include "VertexTypes.h"
#include "Materials.h"

using namespace std;

struct Entity
{
    float position[3];
    int data[32];
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

typedef Mesh::StaticMesh<Mesh::PositionVertex, uint32_t, uint32_t, uint16_t, uint16_t, 0> MyMeshDyn;

int main()
{
    cout << "Hello, World!" << endl;

    EntityAlloc alloc;

    EntityAlloc::Handle h = alloc.createObject();
    Entity& e = alloc.getElement(h);
    e.position[0] = 123.0f;

    std::vector<EntityAlloc::Handle> handles;
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
    
    return 0;
}