#pragma once
#include "StaticReferencedAllocator.h"
#include <functional>

namespace Memory
{
    template<typename T, int NUM_OBJ>
    class ObjectManager
    {
    public:
        
    private:
        StaticReferencedAllocator<T, NUM_OBJ> m_Alloc;
        
        /**
         * 
        std::function<void(T*)> m_OnDelete;
    };
};