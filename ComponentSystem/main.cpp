#include <iostream>
#include <vector>
#include "StaticReferencedAllocator.h"

using namespace std;

struct Entity
{
    float position[3];
    int data[32];
};

typedef Memory::StaticReferencedAllocator<Entity, 4096> EntityAlloc;


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